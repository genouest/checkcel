import pandas as pd

from checkcel import Checkcel
from checkcel.validators import IntValidator, FloatValidator


class TestCheckcelValidateFloat():

    def test_invalid_string(self):
        data = {'my_column': ['notanumber']}
        validators = {'my_column': FloatValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_empty(self):
        data = {'my_column': ['', 6]}
        validators = {'my_column': FloatValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_na(self):
        data = {'my_column': ['na', 6]}
        validators = {'my_column': FloatValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_unique(self):
        data = {'my_column': [1, 1]}
        validators = {'my_column': FloatValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def invalid_min(self):
        data = {'my_column': [6, 4]}
        validators = {'my_column': FloatValidator(min=5)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def invalid_max(self):
        data = {'my_column': [6, 4]}
        validators = {'my_column': FloatValidator(max=5)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def invalid_both(self):
        data = {'my_column': [8, 6.1, 5]}
        validators = {'my_column': FloatValidator(max=7.5, min=5.5)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 2

    def test_valid_empty(self):
        data = {'my_column': ['', 6, '']}
        validators = {'my_column': FloatValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid_na(self):
        data = {'my_column': ['na', 6, 'n/a']}
        validators = {'my_column': FloatValidator(na_ok=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid(self):
        data = {'my_column': [6, 4, "9.0"]}
        validators = {'my_column': FloatValidator()}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()


class TestCheckcelValidateInt():

    def test_invalid_string(self):
        data = {'my_column': ['notanumber']}
        validators = {'my_column': IntValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_float(self):
        data = {'my_column': ['4.8']}
        validators = {'my_column': IntValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_unique(self):
        data = {'my_column': [1, 1]}
        validators = {'my_column': IntValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_empty(self):
        data = {'my_column': ['', 6]}
        validators = {'my_column': IntValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_na(self):
        data = {'my_column': ['na', 6]}
        validators = {'my_column': IntValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def invalid_min(self):
        data = {'my_column': [6, 4]}
        validators = {'my_column': IntValidator(min=5)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def invalid_max(self):
        data = {'my_column': [6, 4]}
        validators = {'my_column': IntValidator(max=5)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def invalid_both(self):
        data = {'my_column': [8, 6, 4]}
        validators = {'my_column': IntValidator(max=7, min=5)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 2

    def test_valid_empty(self):
        data = {'my_column': ['', 6, '']}
        validators = {'my_column': IntValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid_na(self):
        data = {'my_column': ['na', 6, 'n/a']}
        validators = {'my_column': IntValidator(na_ok=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid(self):
        data = {'my_column': [6, 4, "9"]}
        validators = {'my_column': IntValidator()}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()
