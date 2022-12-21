import pandas as pd

from checkcel import Checkcel
from checkcel.validators import GPSValidator


class TestCheckcelValidateGPS():

    def test_invalid_dd(self):
        data = {'my_column': ['invalidvalue', '46.174181N 14.801100E']}
        validators = {'my_column': GPSValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_dms(self):
        data = {'my_column': ['invalidvalue', '45°45\'32.4"N 09°23\'39.9"E']}
        validators = {'my_column': GPSValidator(format="DMS")}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        print(validation.failures['my_column'])
        assert len(validation.failures['my_column']) == 1

    def test_invalid_lat(self):
        data = {'my_column': ['46.174181N', '46.174181N 14.801100E']}
        validators = {'my_column': GPSValidator(only_lat=True)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_long(self):
        data = {'my_column': ['140.801100E', '46.174181N 14.801100E']}
        validators = {'my_column': GPSValidator(only_long=True)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        print(validation.failures['my_column'])
        assert len(validation.failures['my_column']) == 1

    def test_invalid_empty(self):
        data = {'my_column': ['46.174181N 14.801100E', '']}
        validators = {'my_column': GPSValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_na(self):
        data = {'my_column': ['46.174181N 14.801100E', 'na']}
        validators = {'my_column': GPSValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_unique(self):
        data = {'my_column': ['46.174181N 14.801100E', '46.174181N 14.801100E']}
        validators = {'my_column': GPSValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_valid_empty(self):
        data = {'my_column': ['', '46.174181N 14.801100E', '']}
        validators = {'my_column': GPSValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid_na(self):
        data = {'my_column': ['46.174181N 14.801100E', 'na', 'n/a']}
        validators = {'my_column': GPSValidator(na_ok=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid(self):
        data = {'my_column': ['46.174181N 14.801100E', '+87.174181 -140.801100E']}
        validators = {'my_column': GPSValidator()}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()
