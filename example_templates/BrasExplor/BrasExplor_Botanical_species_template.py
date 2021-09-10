from checkcel import Checkplate
from checkcel.validators import FloatValidator, NoValidator
from collections import OrderedDict


class MyTemplate(Checkplate):
    validators = OrderedDict([
        ("Botanical name", NoValidator()),
        ("Name@Population", NoValidator()),
        ("frequency", FloatValidator(min=0, max=100)),
        ("remarks", NoValidator()),
    ])
