import pandas as pd

from checkcel import Checkcel
from checkcel.validators import UniqueValidator, NoValidator


class TestCheckcelValidateUnique():

    def test_invalid(self):
        data = {'my_column': ['notunique', 'notunique']}
        validators = {'my_column': UniqueValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_empty(self):
        data = {'my_column': ['unique', '']}
        validators = {'my_column': UniqueValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_na(self):
        data = {'my_column': ['unique', 'na', 'na']}
        validators = {'my_column': UniqueValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_multiple(self):
        data = {'my_column': ['unique1', 'unique1'], 'another_column': ['val2', 'val2']}
        validators = {'my_column': UniqueValidator(unique_with=["another_column"]), 'another_column': NoValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_valid_empty(self):
        data = {'my_column': ['', 'unique']}
        validators = {'my_column': UniqueValidator()}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid_na(self):
        data = {'my_column': ['na', 'unique', 'na']}
        validators = {'my_column': UniqueValidator(na_ok=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid(self):
        data = {'my_column': ['unique1', 'unique2']}
        validators = {'my_column': UniqueValidator()}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()

    def test_valid_multiple(self):
        data = {'my_column': ['unique1', 'unique1'], 'another_column': ['val1', 'val2']}
        validators = {'my_column': UniqueValidator(unique_with=["another_column"]), 'another_column': NoValidator()}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()
