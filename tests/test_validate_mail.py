import pandas as pd

from checkcel import Checkcel
from checkcel.validators import EmailValidator


class TestCheckcelValidateMail():

    def test_invalid(self):
        data = {'my_column': ['invalidemail.emailprovider.com', 'invalidemail@emailprovidercom']}
        validators = {'my_column': EmailValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 2

    def test_invalid_empty(self):
        data = {'my_column': ['', 'validemail@emailprovider.com']}
        validators = {'my_column': EmailValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_na(self):
        data = {'my_column': ['na', 'validemail@emailprovider.com']}
        validators = {'my_column': EmailValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_unique(self):
        data = {'my_column': ['validemail@emailprovider.com', 'validemail@emailprovider.com']}
        validators = {'my_column': EmailValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_valid_empty(self):
        data = {'my_column': ['', 'validemail@emailprovider.com', '']}
        validators = {'my_column': EmailValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid_na(self):
        data = {'my_column': ['validemail@emailprovider.com', 'na', 'n/a']}
        validators = {'my_column': EmailValidator(na_ok=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid(self):
        data = {'my_column': ['validemail@emailprovider.com', 'valid2email@emailprovider.com']}
        validators = {'my_column': EmailValidator()}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()
