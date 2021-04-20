from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation

from govalidator.validators import TextValidator, OntologyValidator
from openpyxl.utils import get_column_letter

class Gogenerator(object):
    def __init__(
        self,
        output,
        output_type,
        validators={},
    ):
        self.logger = logs.logger
        self.output = output
        self.output_type
        self.validators = validators or getattr(self, "validators", {})

        self.validators.update(
            {
                field: [TextValidator()]
                for field, value in self.validators.items()
                if not value
            }
        )


    def generate(self):
        wb = Workbook()
        ws = wb.active
        current_data_column = 0
        current_ontology_column = 0
        current_readme_row = 0
        readme_sheet = ws.create_sheet(title="README")
        data_sheet = ws.create_sheet(title="Data")
        ontology_sheet = None
        for column_name, validator in self.validators.items():
            readme_sheet.cell(column=0, row=current_readme_row, value=validator.describe(column_name))
            current_readme_row += 1
            data_sheet.cell(column=current_data_column, row=0, value=column_name)
            if isinstance(validator, OntologyValidator):
                if not ontology_sheet:
                    ontology_sheet = ws.create_sheet(title="Ontologies")
                data_validation = validator.generate(get_column_letter(current_data_column), get_column_letter(current_ontology_column), ontology_sheet)
                current_ontology_column +=1
            else:
                data_validation = validator.generate(get_column_letter(current_data_column))
            if data_validation:
                data_sheet.add_data_validation(data_validation)
            current_data_column += 1
        wb.save(filename = self.output)
