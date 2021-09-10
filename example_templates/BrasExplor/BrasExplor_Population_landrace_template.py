from checkcel import Checkplate
from checkcel.validators import DateValidator, NoValidator, SetValidator, IntValidator
from collections import OrderedDict


class MyTemplate(Checkplate):
    validators = OrderedDict([
        ("Population name", NoValidator()),
        ("Sampling date", DateValidator()),
        ("Collector", NoValidator()),
        ("Country", SetValidator(valid_values=["Algeria", "Egypt", "France", "Italy", "Slovenia", "Tunisia", "Spain"])),
        ("Region", NoValidator()),
        ("Province", NoValidator()),
        ("Locality", NoValidator()),
        ("Town", NoValidator()),
        ("GPS", NoValidator()),
        ("Altitude", IntValidator(empty_ok=True)),
        ("Place (#1)", SetValidator(empty_ok=True, valid_values=["Family garden", "market", "field", "private collection", "other"])),
        ("Origin (#2)", NoValidator()),
        ("Source (#3)", SetValidator(empty_ok=True, valid_values=["Friends", "neighbors", "parents", "exchange", "purchase", "market", "seed merchant", "other"])),
        ("Purchased (#4)", SetValidator(empty_ok=True, valid_values=["Never", "Regurlaly", "Occasionally", ""])),
        ("Purchased where [#4)", NoValidator()),
        ("Exchanged (#5)", SetValidator(empty_ok=True, valid_values=["Never", "Regularly", "Occasionally", ""])),
        ("Exchanged with whom (#5)", NoValidator()),
        ("Propagation (#6)", NoValidator()),
        ("Similarity (#7)", SetValidator(empty_ok=True, valid_values=["no", "yes"])),
        ("Isolation precaution (#7)", NoValidator()),
        ("Conservation duration (#8)", IntValidator(empty_ok=True, min=1, max=7)),
        ("storage conditions (#8)", NoValidator()),
        ("Importance (#9)", SetValidator(empty_ok=True, valid_values=["rare", "infrequent", "frequent", "abundant"])),
        ("Sowing date (#10)", DateValidator(empty_ok=True)),
        ("Harvest date (#11)", DateValidator(empty_ok=True)),
        ("Irrigation (#12)", NoValidator()),
        ("Informant (#13)", NoValidator()),
        ("Human food (#14)", SetValidator(empty_ok=True, valid_values=["no", "yes", ""])),
        ("Forage (#14)", SetValidator(empty_ok=True, valid_values=["no", "yes", ""])),
        ("Part used (#15)", SetValidator(empty_ok=True, valid_values=["Root", "Leaves", "Roots + leaves", "other"])),
        ("Number of recipes (#16)", IntValidator(empty_ok=True, min=0)),
        ("Destination (#17)", SetValidator(empty_ok=True, valid_values=["Family", "Local market", "Elsewhere market", ""])),
        ("Destination where (#17)", NoValidator()),
        ("Destination how (#17)", NoValidator()),
        ("Taste qualities (#18)", NoValidator()),
        ("Why kept (#19)", NoValidator()),
        ("When abandoned (#20)", NoValidator()),
        ("Why abandoned (#20)", NoValidator()),
        ("Grown duration (#21)", NoValidator()),
        ("Cultivated (#22)", NoValidator()),
        ("Comments (#23)", NoValidator())
    ])
