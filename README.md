# Checkcel

Checkcel is a generation & validation tool for CSV/ODS/XLSX/XLS files.
Basic validations (sets, whole, decimals, unicity, emails, dates, regex) are included, but also ontologies validation.
(Using the [OLS API](https://www.ebi.ac.uk/ols/index), and the [INRAE thesaurus](https://consultation.vocabulaires-ouverts.inrae.fr))

Checkcel works with either python templates or json/yml files for the generation and validation.  
Examples are available [here](https://github.com/mboudet/checkcel_templates) or in the [example folder](examples/).  

Three commands are available:

# Command line

## Checkcel extract

The `extract` command will try to extract a Python template (with validation setup) from an existing **.xlsx** file. (For now, due to the lack of python libraries for interacting with .ods files, they are not supported.)

Optional parameters :
* --sheet for the sheet to validate (First sheet is number 0. Default to 0)
* --template Type of template "python", "json" or "yml" (default to python)

Syntax:
`Checkcel extract myinputfile.xlsx myoutfile.py --sheet mysheetnumber`

The `myoutfile.py` template can then be used for validation.  
Since Checkcel has to make some assumptions regarding validations (and cannot detect non-null/unicity formulas), **make sure to check and correct the file**.

*Ontologies will be detected as a set validator*

## Checkcel generate

The `generate` command will generate an .xlsx with validation already set-up. A README sheet will also be created, showing expected values for all columns.
An optional 'Metadata' sheet can also be generated if needed
(For now, due to the lack of python libraries for interacting with .ods files, they cannot be generated. However, converting the xlsx to ods manually should work without breaking validation.)  

Optional parameter :
* --template Type of template "python", "json" or "yml" (default to python)

Syntax:
`checkcel generate mytemplate.py myoutput.xlsx`


## Checkcel validate
Based on https://github.com/di/vladiate for the syntax. Relies on `pandas` for reading csv/ods/xls/xlsx files.
The `validate` command will check the validity of a file against a template.

Optional parameters :
* --sheet for the sheet to validate (First sheet is number 0. Default to 0)
* --format "spreadsheet" or "tabular" (default to spreadsheet)
* --delimiter Tabular file delimiter (default to ",")
* --template Type of template "python", "json" or "yml" (default to python)

Syntax:
```bash
Checkcel validate BrasExplor_wild_template.py Population_description_BR_F_W.ods --sheet 2  
Validating Checkcel(source=Population_description_BR_F_W.ods)
Failed
SetValidator failed 1 time(s) (20.0%) on field: 'Pop organization (3)'
Invalid fields: [''] in rows: [4]
SetValidator failed 1 time(s) (20.0%) on field: 'Exposure (14)'
Invalid fields: [''] in rows: [0]
IntValidator failed 1 time(s) (20.0%) on field: 'Source rock surface (24)'
Invalid fields: [''] in rows: [3]
IntValidator failed 5 time(s) (100.0%) on field: 'Pierraille surface (25)'
```

When calling validate() (from python), you can access a list of logs with the 'logs' parameter of the Checkcel/Checkxtractor/Checkerator class

# Python library

```python
from checkcel import Checkcel, Checkxtractor, Checkerator

Checkxtractor(source=your_xlsx_file, output=your_output_file, sheet=input_sheet_number).extract()

Checkcel(
    source=your_xlsx_file,
    type="spreadsheet | tabular",
    delimiter=",",
    sheet="0"
).load_from_python_file(your_python_template_file).validate()

Checkerator(
    output=your_output_file,
).load_from_python_file(your_python_template_file).generate()

Checkcel(
    source=your_xlsx_file,
    type="spreadsheet | tabular",
    delimiter=",",
    sheet="0"
).load_from_yaml_file(your_yaml_template_file).validate()

Checkcel(
    source=your_xlsx_file,
    type="spreadsheet | tabular",
    delimiter=",",
    sheet="0"
).load_from_json_file(your_json_template_file).validate()

# You can access the logs from python with the 'logs' key of the Checkcel class
```

# Templates

Validation templates can use three formats: json/yaml, and python files.
In all cases, you will need to at least include a list of validators and associated column names. Several optional parameters are also available :

* *metadata*: A list of column names. This will create a metadata sheet with these columns, without validation on them
* *expected_rows*: (Default 0): Number of *data* rows expected
* *empty_ok* (Default False): Whether to accept empty values as valid
* *na_ok* (Default False): whether to allow NA (or n/a) values as valid
* *ignore_space* (Default False): whether to trim the values for spaces before checking validity in python
* *ignore_case* (Default False): whether to ignore the case (when relevant)before checking validity in python
* *skip_generation* (Default False): whether to skip the excel validation generation (for file generation) for all validators
* *skip_validation* (Default False): whether to skip the python validation for all validators
* *unique* (Default False): whether to require unicity for all validators

The last 3 parameters will affect all the validators (when relevant), but can be overriden at the validator level (eg, you can set 'empty_ok' to True for all, but set it to False for a specific validator).

## Python format

A template needs to contain a class inheriting the Checkplate class.  
This class must implement a `validators` attribute, which must be a dictionary where the keys are the column names, and the values the validator. This class can also implement the 4 optional attributes described previously.

If you plan on generating a file with the template, it might be better to use an `OrderedDict`, to make sure the columns are in the correct order.  See the examples for more information.

## JSON/YAML format

Templates in json/yaml simply need to be a dictionnary.
The 4 previous optional parameters can be set as keys if needed.

There must be a 'validators' key, which will contain a list of dictionaries containing the column name and the associated validators.

These dicts must have the following key/values

```
{
  "name": "The Column name",
  "type": "TheValidatorName (ie: NoValidator, or Stringvalidator"
}

```

If needed, these dictionnaries can include an 'options' key, containing a dictionary of options matching the validator parameters (ie: {'max': 10} for a FloatValidator). Please check the example templates for more information.


## Validators

### Global options

All validators (except NoValidator) have these options available. If relevant, these options will override the ones set at the template-level

* *empty_ok* (Default False): Whether to accept empty values as valid (Not enforced in excel)
* *empty_ok_if* (Default None): Accept empty value as valid if **another column** value is set
    * Accept either a string (column name), a list (list of column names), or a dict (Not enforced in excel)
      * The dict keys must be column names, and the values lists of 'accepted values'. The current column will accept empty values if the related column's value is in the list of accepted values
* *empty_ok_unless* (Default None): Accept empty value as valid *unless* **another column** value is set. (Not enforced in excel)
    * Accept either a string (column name), a list (list of column names), or a dict
      * The dict keys must be column names, and the values lists of 'rejected values'. The current column will accept empty values if the related column's value is **not** in the list of reject values
* *ignore_space* (Default False): whether to trim the values for spaces before checking validity
* *ignore_case* (Default False): whether to ignore the case
* *unique* (Default False): whether to enforce unicity for this column. (Not enforced in excel for 'Set-type' validators (set, linked-set, ontology, vocabulaireOuvert))
* *na_ok* (Default False): whether to allow NA (or n/a) values as valid.
* *skip_generation* (Default False): whether to skip the excel validation for this validator (for file generation)
* *skip_validation* (Default False): whether to skip the python validation for this validator

*As excel validation for non-empty values is unreliable, the non-emptiness cannot be properly enforced in excel files*

### Validator-specific options

* NoValidator (always True)
  * **No in-file validation generated**
* TextValidator(**kwargs)
  * **No in-file validation generated** (unless *unique* is set)
* IntValidator(min="", max="", **kwargs)
  * Validate that a value is an integer
  * *min*: Minimal value allowed
  * *max*: Maximal value allowed
* FloatValidator(min="", max="", **kwargs)
  * Validate that a value is an float
  * *min*: Minimal value allowed
  * *max*: Maximal value allowed
* SetValidator(valid_values=[], **kwargs)
  * Validate that a value is part of a set of allowed values
  * *valid_values*: list of valid values
* LinkedSetValidator(linked_column="", valid_values={}, **kwargs)
  * Validate that a value is part of a set of allowed values, in relation to another column value.
    * Eg: Valid values for column C will be '1' or '2' if column B value is 'Test', else '3' or '4'
  * *linked_column*: Linked column name
  * *valid_values*: Dict with the *linked_column* values as keys, and list of valid values as values
    * Ex: {"Test": ['1', '2'], "Test2": ['3', '4']}
* EmailValidator(**kwargs)
* DateValidator(day_first=True, before=None, after=None, **kwargs)
  * Validate that a value is a date.
  * *day_first* (Default True): Whether to consider the day as the first part of the date for ambiguous values.
  * *before* Latest date allowed
  * *after*: Earliest date allowed
* TimeValidator(before=None, after=None, **kwargs)
  * Validate that a value is a time of the day
  * *before* Latest value allowed
  * *after*: Earliest value allowed
* UniqueValidator(unique_with=[], **kwargs)
  * Validate that a column has only unique values.
  * *unique_with*: List of column names if you need a tuple of column values to be unique.
    * Ex: *I want the tuple (value of column A, value of column B) to be unique*
* OntologyValidator(ontology, root_term="", **kwargs)
  * Validate that a term is part of an ontology, using the [OLS API](https://www.ebi.ac.uk/ols/index) for validation
  * *ontology* needs to be a short-form ontology name (ex: ncbitaxon)
  * *root_term* can be used if you want to make sure your terms are *descendants* of a specific term
    * (Should be used when generating validated files using big ontologies)
* VocabulaireOuvertValidator(root_term="", lang="en", labellang="en", vocab="thesaurus-inrae", **kwargs)
  * Validate that a term is part of the INRAE(default) or IRSTEA thesaurus
  * **No in-file validation generated** *unless using root_term*
  * *root_term*: Same as OntologyValidator.
  * *lang*: Language for the queried terms *(en or fr)*
  * *labellang*: Language for the queries returns (ie, the generated validation in files). Default to *lang* values.
  * *vocab*: Vocabulary used. Either 'thesaurus-inrae' or 'thesaurus-irstea'.
* GPSValidator(format="DD", only_long=False, only_lat=False, **kwargs)
  * Validate that a term is a valid GPS cordinate
  * **No in-file validation generated**
  * *format*: Expected GPS format. Valid values are *dd* (decimal degrees, default value) or *dms* (degree minutes seconds)
  * *only_long*: Expect only a longitude
  * *only_lat*: Expect only a latitude
* RegexValidator(regex, excel_formulat="", **kwargs)
  * Validate that a term match a specific regex
  * **No in-file validation generated** *unless using excel_formula*
  * *excel_formula*: Custom rules for in-file validation. [Examples here](http://www.contextures.com/xlDataVal07.html).
    * "{CNAME}" will be replaced by the appropriate column name
