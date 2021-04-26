from __future__ import division
from collections import defaultdict
import pandas

from Checkcel.exceptions import ValidationException
from Checkcel.checkplate import Checkplate


class Checkcel(Checkplate):
    def __init__(
        self,
        source,
        type="spreadsheet",
        delimiter=",",
        sheet=0,
        **kwargs
    ):
        super(Checkcel, self).__init__(**kwargs)
        self.failures = defaultdict(lambda: defaultdict(list))
        self.missing_validators = None
        self.missing_fields = None
        self.source = source
        self.type = type
        self.delimiter = delimiter
        self.sheet = int(sheet)
        self.line_count = 0
        self.column_set = set()
        self.ignore_missing_validators = False

        if type not in ["spreadsheet", "tabular"]:
            raise Exception("Type must be either spreadsheet or tabular")

    def _log_debug_failures(self):
        for field_name, field_failure in self.failures.items():
            self.logger.debug('\nFailure on field: "{}":'.format(field_name))
            for i, (row, errors) in enumerate(field_failure.items()):
                self.logger.debug("  {}:{}".format(self.source, row))
                for error in errors:
                    self.logger.debug("    {}".format(error))

    def _log_validator_failures(self):
        for field_name, validator in self.validators.items():
            if validator.bad["invalid_set"]:
                self.logger.error(
                    "  {} failed {} time(s) ({:.1%}) on field: '{}'".format(
                        validator.__class__.__name__,
                        validator.fail_count,
                        validator.fail_count / self.line_count,
                        field_name,
                    )
                )
                try:
                    # If self.bad is iterable, it contains the fields which
                    # caused it to fail
                    data = validator.bad
                    wrong_terms = ", ".join(["'{}'".format(val) for val in data["invalid_set"]])
                    wrong_rows = ", ".join([str(val) for val in data["invalid_rows"]])
                    self.logger.error(
                        "    Invalid fields: [{}] in rows: [{}]".format(wrong_terms, wrong_rows)
                    )
                except TypeError as e:
                    raise e

    def _log_missing_validators(self):
        self.logger.error("  Missing validators for:")
        self._log_missing(self.missing_validators)

    def _log_missing_fields(self):
        self.logger.error("  Missing expected fields:")
        self._log_missing(self.missing_fields)

    def _log_missing(self, missing_items):
        self.logger.error(
            "{}".format(
                "\n".join(
                    ["    '{}': [],".format(field) for field in sorted(missing_items)]
                )
            )
        )

    def validate(self):
        self.logger.info(
            "\nValidating {}(source={})".format(self.__class__.__name__, self.source)
        )

        if self.type == "spreadsheet":
            df = pandas.read_excel(self.source, sheet_name=self.sheet, convert_float=False, keep_default_na=False)
        else:
            df = pandas.read_csv(self.source, sep=self.delimiter)

        if len(df) == 0:
            self.logger.info(
                "\033[1;33m" + "Source file has no data" + "\033[0m"
            )
            return False

        self.column_set = set(df.columns)
        validator_set = set(self.validators)
        self.missing_validators = self.column_set - validator_set
        if self.missing_validators:
            self.logger.info("\033[1;33m" + "Missing..." + "\033[0m")
            self._log_missing_validators()

            if not self.ignore_missing_validators:
                return False

        self.missing_fields = validator_set - self.column_set
        if self.missing_fields:
            self.logger.info("\033[1;33m" + "Missing..." + "\033[0m")
            self._log_missing_fields()
            return False

        # Might be a way to do it more efficiently..
        df.apply(lambda row: self._validate(row), axis=1)

        if self.failures:
            self.logger.info("\033[0;31m" + "Failed" + "\033[0m")
            self._log_debug_failures()
            self._log_validator_failures()
            return False
        else:
            self.logger.info("\033[0;32m" + "Passed" + "\033[0m")
            return True

    def _validate(self, row):
        for column in self.column_set:
            if column in self.validators:
                validator = self.validators[column]
                try:
                    validator.validate(row[column], self.line_count, row=row)
                except ValidationException as e:
                    self.failures[column][self.line_count].append(e)
                    validator.fail_count += 1
        self.line_count += 1
