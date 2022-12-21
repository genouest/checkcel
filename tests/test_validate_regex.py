import pandas as pd

from checkcel import Checkcel
from checkcel.validators import RegexValidator


class TestCheckcelValidateRegex():

    def test_invalid(self):
        data = {'my_column': ['ABC', 'AFX123']}
        validators = {'my_column': RegexValidator(regex="AFX.*")}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_empty(self):
        data = {'my_column': ['', 'AFX123']}
        validators = {'my_column': RegexValidator(regex="AFX.*")}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_na(self):
        data = {'my_column': ['na', 'AFX123']}
        validators = {'my_column': RegexValidator(regex="AFX.*")}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_unique(self):
        data = {'my_column': ['AFX123', 'AFX123']}
        validators = {'my_column': RegexValidator(unique=True, regex="AFX.*")}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_valid_empty(self):
        data = {'my_column': ['', 'AFX123', '']}
        validators = {'my_column': RegexValidator(unique=True, regex="AFX.*")}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid_na(self):
        data = {'my_column': ['na', 'AFX123', 'n/a']}
        validators = {'my_column': RegexValidator(na_ok=True, regex="AFX.*")}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid(self):
        data = {'my_column': ['AFX123', 'AFX456']}
        validators = {'my_column': RegexValidator(regex="AFX.*")}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()
