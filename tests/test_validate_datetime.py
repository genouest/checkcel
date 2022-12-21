import pandas as pd

from checkcel import Checkcel
from checkcel.validators import DateValidator, TimeValidator


class TestCheckcelValidateDate():

    def test_invalid(self):
        data = {'my_column': ['thisisnotadate', '1991/01/1991']}
        validators = {'my_column': DateValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 2

    def test_invalid_before(self):
        data = {'my_column': ['01/01/2000', '10/10/2010']}
        validators = {'my_column': DateValidator(before="05/05/2005")}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_after(self):
        data = {'my_column': ['01/01/2000', '10/10/2010']}
        validators = {'my_column': DateValidator(after="05/05/2005")}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_empty(self):
        data = {'my_column': ['01/01/1970', '']}
        validators = {'my_column': DateValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_na(self):
        data = {'my_column': ['01/01/1970', '']}
        validators = {'my_column': DateValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_unique(self):
        data = {'my_column': ['01/01/1970', '01/01/1970']}
        validators = {'my_column': DateValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_valid_empty(self):
        data = {'my_column': ['', '01/01/1970', '']}
        validators = {'my_column': DateValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid_na(self):
        data = {'my_column': ['01/01/1970', 'na', 'n/a']}
        validators = {'my_column': DateValidator(na_ok=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid(self):
        data = {'my_column': ['01/01/1970', '01-01-1970', '1970/01/01', '01 01 1970']}
        validators = {'my_column': DateValidator()}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()


class TestCheckcelValidateTime():

    def test_invalid(self):
        data = {'my_column': ['thisisnotatime', '248:26']}
        validators = {'my_column': TimeValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 2

    def test_invalid_before(self):
        data = {'my_column': ['14h23', '16h30']}
        validators = {'my_column': TimeValidator(before="15h00")}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_after(self):
        data = {'my_column': ['14h23', '16h30']}
        validators = {'my_column': TimeValidator(after="15h00")}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_empty(self):
        data = {'my_column': ['13h10', '']}
        validators = {'my_column': TimeValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_na(self):
        data = {'my_column': ['13h10', 'na']}
        validators = {'my_column': TimeValidator()}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_invalid_unique(self):
        data = {'my_column': ['13h10', '13h10']}
        validators = {'my_column': TimeValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        validation = Checkcel(data=df, empty_ok=False, validators=validators)
        val = validation.validate()
        assert val is False
        assert len(validation.failures['my_column']) == 1

    def test_valid_empty(self):
        data = {'my_column': ['', '13h10', '']}
        validators = {'my_column': TimeValidator(unique=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid_na(self):
        data = {'my_column': ['13h10', 'na', 'n/a']}
        validators = {'my_column': TimeValidator(na_ok=True)}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, empty_ok=True, validators=validators)
        assert val.validate()

    def test_valid(self):
        data = {'my_column': ['13h10', '2h36PM']}
        validators = {'my_column': TimeValidator()}
        df = pd.DataFrame.from_dict(data)
        val = Checkcel(data=df, validators=validators)
        assert val.validate()
