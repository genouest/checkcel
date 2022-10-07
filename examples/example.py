from checkcel import Checkplate
from checkcel.validators import DateValidator, LinkedSetValidator, NoValidator, UniqueValidator, SetValidator, IntValidator, GPSValidator, OntologyValidator
from collections import OrderedDict


class MyTemplate(Checkplate):
    empty_ok = True
    ignore_case = False
    ignore_space = False
    metadata = ['Submitter', 'Institute', 'Version']
    validators = OrderedDict([
        ("Name", UniqueValidator()),
        ("Sampling date", DateValidator(empty_ok=False)),
        ("Collector", NoValidator()),
        ("Altitude", IntValidator(min=0)),
        ("Country", SetValidator(empty_ok=False, valid_values=["France", "Italy"])),
        ('City', LinkedSetValidator(linked_column="Country", valid_values={'France': ['Paris', 'Rennes'], 'Italy': ['Milan', 'Roma']})),
        ("GPS", GPSValidator()),
        ('Brassica type', OntologyValidator('ncbitaxon', root_term='brassica'))
    ])
