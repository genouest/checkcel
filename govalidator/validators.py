from email-validator import validate_email, EmailNotValidError
import requests

from openpyxl.worksheet.datavalidation import DataValidation

from govalidator.exceptions import ValidationException, BadValidatorException

class Validator(object):
    """ Generic Validator class """

    def __init__(self, empty_ok=False, valid_values=set()):
        self.fail_count = 0
        self.empty_ok = empty_ok
        self.valid_values  = valid_values

    @property
    def bad(self):
        raise NotImplementedError

    def validate(self, field, row):
        """ Validate the given field. Also is given the row context """
        raise NotImplementedError

    def generate(self, column, ontology_column=None, ontology_worksheet=None):
        """ Generate an openpyxl Datavalidation entity. Pass the column for custom formulas"""
        raise NotImplementedError

    def describe(self, column_name):
        """ Return a line of text describing allowed values"""
        raise NotImplementedError


class CastValidator(Validator):
    """ Validates that a field can be cast to a float """

    def __init__(self, min=None, max=None, **kwargs):
        super(CastValidator, self).__init__(**kwargs)
        self.invalid_set = set()
        self.min = min
        self.max = max

    def validate(self, field, row={}):
        try:
            if field or not self.empty_ok:
                self.cast(field)
                if min and field <= min:
                    self.invalid_set.add(field)
                    raise ValidationException("{} is below min value {}".format(field, max))
                if max and field >= max:
                    self.invalid_set.add(field)
                    raise ValidationException("{} is above max value {}".format(field, max))

        except ValueError as e:
            self.invalid_set.add(field)
            raise ValidationException(e)

    @property
    def bad(self):
        return self.invalid_set

    def generate(self, column, ontology_column=None, ontology_worksheet=None):
        params = {"type": self.type}
        if (min and max):
            params["formula1"] = min
            params["formula2"] = max
            operator = "between"
        elif min:
            params["formula1"] = min
            operator = "greaterThanOrEqual"
        elif max:
            params["formula1"] = max
            operator = "lessThanOrEqual"
        dv = DataValidation(**params)
        dv.add("{}2:{}1048576").format(column, column)
        return dv

    def describe(self, column_name):
        text = "{} : {} number.".format(column_name, self.type)
        if min:
            text += " Minimum : {}.".format(min)
        if max:
            text += " Maximum : {}.".format(max)
        return text

class FloatValidator(CastValidator):
    """ Validates that a field can be cast to a float """

    def __init__(self, **kwargs):
        super(FloatValidator, self).__init__(**kwargs)
        self.cast = float
        self.type = "decimal"


class IntValidator(CastValidator):
    """ Validates that a field can be cast to an int """

    def __init__(self, **kwargs):
        super(IntValidator, self).__init__(**kwargs)
        self.cast = int
        self.type = "whole"


class ListValidator(Validator):
    """ Validates that a field is in the given list of values """

    def __init__(self, **kwargs):
        super(SetValidator, self).__init__(**kwargs)
        self.invalid_set = set()
        if self.empty_ok:
            self.valid_values.add("")

    def validate(self, field, row={}):
        if field not in self.valid_values:
            self.invalid_set.add(field)
            raise ValidationException(
                "'{}' is invalid".format(field)
            )

    @property
    def bad(self):
        return self.invalid_set

    def generate(self, column, ontology_column=None, ontology_worksheet=None):
        params = {"type": "list"}
        values = ",".join(self.valid_values)
        params["formula1"] = ' + values + '
        dv = DataValidation(**params)
        dv.add("{}2:{}1048576").format(column, column)
        return dv

    def describe(self, column_name):
        return "{} : ({})".format(column_name, ", ".join(self.valid_values))


class EmailValidator(Validator):
    """ Validates that a field is in the given set """

    def __init__(self, **kwargs):
        super(SetValidator, self).__init__(**kwargs)
        self.invalid_set = set()

    def validate(self, field, row={}):
        if field or not self.empty_ok:
            try:
                validate_email(field)
            except EmailNotValidError as e:
                self.invalid_set.add(field)
                raise ValidationException(e)

    @property
    def bad(self):
        return self.invalid_set

    def generate(self, column, ontology_column=None):
        params = {"type": "custom"}
        params["formula1"] = "=ISNUMBER(MATCH("*@*.?*",{}2,0))".format(column)
        dv = DataValidation(**params)
        dv.error ='Value must be an email'
        dv.add("{}2:{}1048576").format(column, column)
        return dv

    def describe(self, column_name):
        return "{} : Email".format(column_name)

class OntologyValidator(Validator):
    """ Validates that a field is in the given set """

    def __init__(self, ontology, root_term="", **kwargs):
        super(SetValidator, self).__init__(**kwargs)
        self.invalid_set = set()
        self.validated_terms = set()
        self.ontology = ontology
        self.root_term = root_term
        self.root_term_iri = ""

        is_ontology, self.root_term_iri = _validate_ontology(ontology, self.root_term)
        if not is_ontology:
            raise BadValidatorException("'{}' is not a valid ontology".format({}))

    def validate(self, field, row={}):
        if field == "" and self.empty_ok:
            return

        if not (field in validated_terms or field in invalid_set):
            ontological_term = _validate_ontological_term(field, ontology, self.root_term)
            if not ontological_term:
                self.invalid_set.add(field)
                raise ValidationException(e)
            self.validated_terms.add(field)

    @property
    def bad(self):
        return self.invalid_set

    def generate(self, column, ontology_column=None, ontology_worksheet=None):
        params = {"type": "custom"}
        params["formula1"] = "=ISNUMBER(MATCH("*@*.?*",{}2,0))".format(column)
        dv = DataValidation(**params)
        dv.error ='Value must be an email'
        dv.add("{}2:{}1048576").format(column, column)
        return dv

    def describe(self, column_name):
        text = "{} : Ontological term from {} ontology.".format(column_name, self.ontology)
        if self.root_term:
            text += " Root term is : {}".format(self.root_term)


class UniqueValidator(Validator):
    """ Validates that a field is unique within the file """

    def __init__(self, unique_with=[], **kwargs):
        super(UniqueValidator, self).__init__(**kwargs)
        self.unique_values = set()
        self.duplicates = set()
        self.unique_with = unique_with
        self.unique_check = False

    def _precheck_unique_with(self, row):
        extra = set(self.unique_with) - set(row.keys())
        if extra:
            raise BadValidatorException(extra)
        self.unique_check = True

    def validate(self, field, row={}):
        if field == "" and self.empty_ok:
            return
        if self.unique_with and not self.unique_check:
            self._precheck_unique_with(row)

        key = tuple([field] + [row[k] for k in self.unique_with])
        if key not in self.unique_values:
            self.unique_values.add(key)
        else:
            self.duplicates.add(key)
            if self.unique_with:
                raise ValidationException(
                    "'{}' is already in the column (unique with: {})".format(
                        field, key[1:]
                    )
                )
            else:
                raise ValidationException("'{}' is already in the column".format(field))

    @property
    def bad(self):
        return self.duplicates

    def generate(self, column, ontology_column=None):
        params = {"type": "custom"}
        params["formula1"] = "=COUNTIF(${}:${},{}2)<2".format(column, column, column)
        dv = DataValidation(**params)
        dv.error ='Value must be unique'
        dv.add("{}2:{}1048576").format(column, column)
        return dv

    def describe(self, column_name):
        text = "{} : Unique value.".format(column_name)
        if self.unique_with:
            text += " Must be unique with column(s) {}".format(", ".join(self.unique_with))
        return text

class Ignore(Validator):
    """ Ignore a given field. Never fails """

    def validate(self, field, row={}):
        pass

    @property
    def bad(self):
        pass


def _validate_ontology(ontology, root_term=""):
    root_term_iri = ""
    if not ontology:
        return False
    base_path = "http://www.ebi.ac.uk/ols/api"
    sub_path = "/ontologies/{}".format(ontology.lower())
    r = requests.get(base_path + sub_path)
    if not r.status_code == 200:
        return False, root_term_iri
    if root_term:
        root_term_iri = _validate_ontological_term(root_term, ontology, return_uri=True)
    return True, root_term_iri

def _validate_ontological_term(term, ontology, root_term_iri="", return_uri=False):
    base_path = "http://www.ebi.ac.uk/ols/api/search"
    body = {
        "q": term,
        "ontology": ontology.lower(),
        "type": "class",
        "exact": True,
        "queryFields": ["label", "synonym"]
    }
    if root_term_iri:
        body["childrenOf"] = root_term_iri
    r = requests.get(base_path, params=body)
    res = r.json()
    if not res["response"]["numFound"] == 1:
        return False
    if return_uri:
        return res["response"]["docs"][0]["iri"]
    return True
