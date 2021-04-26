# Checkcel

Checkcel is a generation & validation tool for CSV/ODS/XLSX/XLS files.
Basic validations (sets, whole, decimals, unicity, emails, dates) are included, but also ontologies validation.
(Using the [OLS API](https://www.ebi.ac.uk/ols/index))

Checkcel (tmp) works with python templates to for the generation and validation.  
Examples are available in the *example_templates* folder.  

Three commands are available:

## Checkcel extract

The `extract` command will try to extract a Python template (with validation setup) from an existing **.xlsx** file. (For now, due to the lack of python libraries for interacting with .ods files, they are not supported.)

Syntax:
`Checkcel extract myinputfile.xlsx myoutfile.py --sheet mysheetnumber`

The `myoutfile.py` can then be used for validation.
Since Checkcel has to make some assumptions regarding validations (and cannot detect non-null/unicity formulas), **make sure to check and correct the file**.  

## Checkcel generate

The `generate` command will generate an .xlsx with validation already set-up. A README sheet will also be created, showing expected values for all columns. (For now, due to the lack of python libraries for interacting with .ods files, they cannot be generated. However, converting the xlsx to ods manually should work without breaking validation.)

Syntax:
`checkcel generate mytemplate.py myoutput.xlsx`


## Checkcel validate
Based on https://github.com/di/vladiate for the syntax. Relies on `pandas` for reading csv/ods/xls/xlsx files.
The `validate` command will check the validity of a file against a template.

Syntax:
```bash
Checkcel validate BrasExplor_wild_template.py Population_description_BR_F_W.ods --sheet 2
Validating Checkcel(source=Population_description_BR_F_W.ods)                                                        Failed                                                                                                                    SetValidator failed 1 time(s) (20.0%) on field: 'Pop organization (3)'                                                    Invalid fields: [''] in rows: [4]                                                                                     SetValidator failed 1 time(s) (20.0%) on field: 'Exposure (14)'                                                           Invalid fields: [''] in rows: [0]                                                                                     IntValidator failed 1 time(s) (20.0%) on field: 'Source rock surface (24)'                                                Invalid fields: [''] in rows: [3]                                                                                     IntValidator failed 5 time(s) (100.0%) on field: 'Pierraille surface (25)'
```

# Templates
A template needs to contain a class inheriting the Checkplate class.
This class must implement a `validators` attribute, which must be a dictionary where the keys are the column names, and the values the validator. If you plan on generating a file with the template, it might be better to use an `OrderedDict`. See the example for more information.

## Validators
* NoValidator (always True)
* TextValidator(empty_ok=False)
* IntValidator(min="", max="", empty_ok=False)
* FloatValidator(min="", max="", empty_ok=False)
* SetValidator(valid_values=[], empty_ok=False)
* EmailValidator(empty_ok=False)
* DateValidator(empty_ok=False)
* UniqueValidator(empty_ok=False)
* OntologyValidator(ontology, root_term="", empty_ok=False)
