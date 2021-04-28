from checkcel import Checkplate
from checkcel.validators import SetValidator, NoValidator
from collections import OrderedDict


class MyTemplate(Checkplate):
    validators = OrderedDict([
        ("name@Population", NoValidator()),
        ("Picture", NoValidator()),
        ("Type", SetValidator(valid_values=["whole plant", "population"]))
    ])
