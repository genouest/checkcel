from checkcel import Checkplate
from checkcel.validators import NoValidator, FloatValidator
from collections import OrderedDict


class BrasExplor_Botanical_species(Checkplate):
    validators = OrderedDict([
        ("Botanical name", NoValidator()),
        ("Name@Population", NoValidator()),
        ("frequency", FloatValidator()),
        ("remarks", NoValidator())
    ])
