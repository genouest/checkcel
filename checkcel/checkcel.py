from __future__ import division
from collections import defaultdict
import pandas
import warnings

from checkcel.exceptions import ValidationException
from checkcel.checkplate import Checkplate


class Checkcel(Checkplate):
    def __init__(
        self,
        source="",
        data=None,
        format="spreadsheet",
        delimiter=",",
        sheet=0,
        row=0,
        **kwargs
    ):
        super(Checkcel, self).__init__(**kwargs)
        self.failures = defaultdict(lambda: defaultdict(list))
        self.missing_validators = None
        self.missing_fields = None
        self.source = source
        self.data = data
        self.format = format
        self.delimiter = delimiter
        self.sheet = int(sheet)
        self.row = row
        # This value is used for display. Pandas skips the header row
        self.line_count = row + 1
        self.column_set = set()
        self.ignore_missing_validators = False

        if not (self.source or self.data is not None):
            raise Exception("Need to provide either a source or the data (as a pandas dataframe)")

        if format not in ["spreadsheet", "tabular"]:
            raise Exception("Type must be either spreadsheet or tabular")

    def _log_debug_failures(self):
        for field_name, field_failure in self.failures.items():
            self.debug('\nFailure on field: "{}":'.format(field_name))
            for i, (row, errors) in enumerate(field_failure.items()):
                self.debug("  {}:{}".format(self.source, row))
                for error in errors:
                    self.debug("    {}".format(error))

    def _log_validator_failures(self):
        for field_name, validator in self.validators.items():
            if validator.bad:
                self.error(
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
                    self.error(
                        "    Invalid fields: [{}] in rows: [{}]".format(wrong_terms, wrong_rows)
                    )
                except TypeError as e:
                    raise e

    def _log_missing_validators(self):
        self.error("  Missing validators for:")
        self._log_missing(self.missing_validators)

    def _log_missing_fields(self):
        self.error("  Missing expected fields:")
        self._log_missing(self.missing_fields)

    def _log_missing(self, missing_items):
        self.error(
            "{}".format(
                "\n".join(
                    ["    '{}': [],".format(field) for field in sorted(missing_items)]
                )
            )
        )

    def validate(self):
        self.info(
            "\nValidating {}{}".format(self.__class__.__name__, "(source={})".format(self.source) if self.source else "")
        )

        if self.source:
            if self.format == "spreadsheet":
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    df = pandas.read_excel(self.source, sheet_name=self.sheet, keep_default_na=False, skiprows=self.row)
            else:
                df = pandas.read_csv(self.source, sep=self.delimiter, skiprows=self.row)

            if len(df) == 0:
                self.info(
                    "\033[1;33m" + "Source file has no data" + "\033[0m"
                )
                return False

        else:
            df = self.data

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        self.column_set = set(df.columns)
        validator_set = set(self.validators)
        self.missing_validators = self.column_set - validator_set
        if self.missing_validators:
            self.info("\033[1;33m" + "Missing..." + "\033[0m")
            self._log_missing_validators()

            if not self.ignore_missing_validators:
                return False

        self.missing_fields = validator_set - self.column_set
        if self.missing_fields:
            self.info("\033[1;33m" + "Missing..." + "\033[0m")
            self._log_missing_fields()
            return False

        if self.expected_rows:
            if not self.expected_rows == len(df.index):
                self.error("Length issue: Expecting {} row(s), found {}".format(self.expected_rows, len(df.index)))
                return False

        # Might be a way to do it more efficiently..
        df.apply(lambda row: self._validate(row), axis=1)

        if self.failures:
            self.info("\033[0;31m" + "Failed" + "\033[0m")
            self._log_debug_failures()
            self._log_validator_failures()
            return False
        else:
            self.info("\033[0;32m" + "Passed" + "\033[0m")
            return True

    def _validate(self, row):
        for column in self.column_set:
            if column in self.validators:
                validator = self.validators[column]
                try:
                    validator.validate(row[column], self.line_count, row)
                except ValidationException as e:
                    self.failures[column][self.line_count].append(e)
                    validator.fail_count += 1
        self.line_count += 1
