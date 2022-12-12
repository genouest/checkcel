import pandas as pd

from checkcel import Checkcel
from checkcel.validators import SetValidator, LinkedSetValidator


class TestCheckcelValidateSet():

    def test_invalid(self):
        data = {'my_column': ['invalid_value', 'valid_value']}
        validators = {'my_column': SetValidator(valid_values=["valid_value"])}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_empty(self):
        data = {'my_column': ['valid_value', '']}
        validators = {'my_column': SetValidator(valid_values=["valid_value"])}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_na(self):
        data = {'my_column': ['valid_value', 'na']}
        validators = {'my_column': SetValidator(valid_values=["valid_value"])}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_unique(self):
        data = {'my_column': ['valid_value', 'valid_value']}
        validators = {'my_column': SetValidator(unique=True, valid_values=["valid_value"])}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_valid_empty(self):
        data = {'my_column': ['', 'valid_value', '']}
        validators = {'my_column': SetValidator(unique=True, valid_values=["valid_value"])}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid_na(self):
        data = {'my_column': ['na', 'valid_value', 'n/a']}
        validators = {'my_column': SetValidator(na_ok=True, valid_values=["valid_value"])}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid(self):
        data = {'my_column': ["valid_value1", "valid_value2"]}
        validators = {'my_column': SetValidator(valid_values=["valid_value1", "valid_value2"])}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()


class TestCheckcelValidateLinkedSet():

    def test_invalid(self):
        data = {'my_column': ['value_1', 'value_2'], "another_column": ["valid_value", "invalid_value"]}
        validators = {
            'my_column': SetValidator(valid_values=['value_1', 'value_2']),
            'another_column': LinkedSetValidator(linked_column="my_column", valid_values={"value_1": ["valid_value"], "value_2": ["another_valid_value"]})
        }
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['another_column']) == 1

    def test_invalid_empty(self):
        data = {'my_column': ['value_1', 'value_2', 'value2'], "another_column": ["valid_value", "another_valid_value", ""]}
        validators = {
            'my_column': SetValidator(valid_values=['value_1', 'value_2']),
            'another_column': LinkedSetValidator(linked_column="my_column", valid_values={"value_1": ["valid_value"], "value_2": ["another_valid_value"]})
        }
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['another_column']) == 1

    def test_invalid_na(self):
        data = {'my_column': ['value_1', 'value_2', 'value2'], "another_column": ["valid_value", "another_valid_value", "na"]}
        validators = {
            'my_column': SetValidator(valid_values=['value_1', 'value_2']),
            'another_column': LinkedSetValidator(linked_column="my_column", valid_values={"value_1": ["valid_value"], "value_2": ["another_valid_value"]})
        }
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['another_column']) == 1

    def test_invalid_unique(self):
        data = {'my_column': ['value_1', 'value_2', 'value2'], "another_column": ["valid_value", "another_valid_value", "another_valid_value"]}
        validators = {
            'my_column': SetValidator(valid_values=['value_1', 'value_2']),
            'another_column': LinkedSetValidator(unique=True, linked_column="my_column", valid_values={"value_1": ["valid_value"], "value_2": ["another_valid_value"]})
        }
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['another_column']) == 1

    def test_valid_empty(self):
        data = {'my_column': ['value_1', 'value_2', 'value_2', 'value_2'], "another_column": ["valid_value", "another_valid_value", "", ""]}
        validators = {
            'my_column': SetValidator(valid_values=['value_1', 'value_2']),
            'another_column': LinkedSetValidator(unique=True, linked_column="my_column", valid_values={"value_1": ["valid_value"], "value_2": ["another_valid_value"]})
        }
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid_na(self):
        data = {'my_column': ['value_1', 'value_2', 'value_2', 'value_2'], "another_column": ["valid_value", "another_valid_value", "na", "n/a"]}
        validators = {
            'my_column': SetValidator(valid_values=['value_1', 'value_2']),
            'another_column': LinkedSetValidator(na_ok=True, linked_column="my_column", valid_values={"value_1": ["valid_value"], "value_2": ["another_valid_value"]})
        }
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid(self):
        data = {'my_column': ['value_1', 'value_2', 'value_2'], "another_column": ["valid_value", "another_valid_value", "another_valid_value"]}
        validators = {
            'my_column': SetValidator(valid_values=['value_1', 'value_2']),
            'another_column': LinkedSetValidator(linked_column="my_column", valid_values={"value_1": ["valid_value"], "value_2": ["another_valid_value"]})
        }
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()
