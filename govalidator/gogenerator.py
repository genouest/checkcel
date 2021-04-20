from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation

class Govalidator(object):
    def __init__(
        self,
        output,
        output_type,
        validators={},
    ):
        self.logger = logs.logger
        self.output = output
        self.output_type
        self.type = type
        self.validators = validators or getattr(self, "validators", {})

        if not type in ["spreadsheet", "tabular"]:
            raise Exception("Type must be either spreadsheet or tabular")

        self.validators.update(
            {
                field: [default_validator()]
                for field, value in self.validators.items()
                if not value
            }
        )


    def generate(self):
        wb = Workbook()
        ws = wb.active
