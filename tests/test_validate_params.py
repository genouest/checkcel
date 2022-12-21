import pandas as pd

from checkcel import Checkcel
from checkcel.validators import TextValidator


class TestCheckcelClass():

    def test_invalid_rows_below(self):
        data = {'my_column': ['myvalue', 'my_value2']}
        validators = {'my_column': TextValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, expected_rows=1, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.logs) == 2
        assert validation.logs[1] == "Error: Length issue: Expecting 1 row(s), found 2"

    def test_invalid_rows_above(self):
        data = {'my_column': ['myvalue']}
        validators = {'my_column': TextValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, expected_rows=2, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.logs) == 2
        assert validation.logs[1] == "Error: Length issue: Expecting 2 row(s), found 1"


class TestCheckcelValidateEmpty_if():

    def test_invalid_string(self):
        data = {'my_column': ["", "not_empty"], "another_column": ["", ""]}
        validators = {
            'my_column': TextValidator(empty_ok=True),
            'another_column': TextValidator(empty_ok_if="my_column")
        }
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['another_column']) == 1

    def test_invalid_list(self):
        data = {'my_column': ["", "", "not_empty", "not_empty"], 'my_column2': ["", "not_empty", "", "not_empty"], "another_column": ["", "", "", ""]}
        validators = {
            'my_column': TextValidator(empty_ok=True),
            'my_column2': TextValidator(empty_ok=True),
            'another_column': TextValidator(empty_ok_if=["my_column", "my_column2"])
        }
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['another_column']) == 3

    def test_invalid_dict(self):
        data = data = {'my_column': ["", "invalid_value", "valid_value"], "another_column": ["", "", ""]}
        validators = {
            'my_column': TextValidator(empty_ok=True),
            'another_column': TextValidator(empty_ok_if={"my_column": ["valid_value"]})
        }
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['another_column']) == 2


class TestCheckcelValidateEmpty_unless():

    def test_invalid_string(self):
        data = {'my_column': ["", "not_empty"], "another_column": ["", ""]}
        validators = {
            'my_column': TextValidator(empty_ok=True),
            'another_column': TextValidator(empty_ok_unless="my_column")
        }
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['another_column']) == 1

    def test_invalid_list(self):
        data = {'my_column': ["", "", "not_empty", "not_empty"], 'my_column2': ["", "not_empty", "", "not_empty"], "another_column": ["", "", "", ""]}
        validators = {
            'my_column': TextValidator(empty_ok=True),
            'my_column2': TextValidator(empty_ok=True),
            'another_column': TextValidator(empty_ok_unless=["my_column", "my_column2"])
        }
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['another_column']) == 3

    def test_invalid_dict(self):
        data = data = {'my_column': ["", "invalid_value", "valid_value"], "another_column": ["", "", ""]}
        validators = {
            'my_column': TextValidator(empty_ok=True),
            'another_column': TextValidator(empty_ok_unless={"my_column": ["invalid_value"]})
        }
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['another_column']) == 1
