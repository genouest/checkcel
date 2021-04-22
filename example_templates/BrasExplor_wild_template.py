from govalidator import Gotemplate
from govalidator.validators import UniqueValidator, SetValidator, DateValidator, NoValidator, IntValidator, FloatValidator

from collections import OrderedDict


class BrasExplor_wild(Gotemplate):
    validators = OrderedDict([
        ("Population name", UniqueValidator()),
        ("Sampling_date", DateValidator()),
        ("Collector", NoValidator()),
        ("Country", SetValidator(valid_values=["Algeria", "Egypt", "France", "Italy", "Slovenia", "Tunisia"])),
        ("Region", NoValidator()),
        ("Province", NoValidator()),
        ("Locality", NoValidator())
        ("Town", NoValidator()),
        ("GPS", NoValidator()),
        ("Altitude", FloatValidator(min=0))
        ("Area", FloatValidator(min=0)),
        ("Plant density", FloatValidator(min=0)),
        ("Pop organization", SetValidator(valid_values=["patchs", "continuous"])),
        ("Number of collected plants", IntValidator(min=0, max=30)),
        ("Type of land use", SetValidator(valid_values=["Not determined", "Wasteland", "Pasture", "Reaping", "Pasture/Reaping", "Annual crops", "Perennial crops", "Field border", "Undergrowth", "Others"])),
        ("Land use intensity", SetValidator(valid_values=["Not determined", "Not cultivated", "Cultivated"])),
        ("Animals", IntValidator(min=0, max=9)),
        ("Soil work", SetValidator(valid_values=["Not determined", "No soil work", "Cultivated field with plowing"])),
        ("Irrigation", SetValidator(valid_values=["No", "Yes"])),
        ("Weeding", SetValidator(valid_values=["No", "Chemical", "Mechanical"])),
        ("Artificiality", IntValidator(min=1, max=7)),
        ("Land use comments", NoValidator()),
        ("Station", SetValidator(valid_values=["Sheltered", "Protected", "Open"])),
        ("Exposure", SetValidator(valid_values=["undetermined", "N", "NE", "E", "SE", "S", "SW", "W", "NW"])),
        ("Macro-topography", SetValidator(valid_values=["Closed depression", "Open depression", "Plain", "Plateau", "Lower slope", "Mid slope", "Top of slope", "Summit/Escarpment", "Dunes"])),
        ("Slope", SetValidator(valid_values=["Zero", "from 1 to 10%", "from 11 to 30%", ">31%"])),
        ("Microrelief", SetValidator(valid_values=["Difficult to assess", "Plan", "Bumpy", "Logs", "Channel", "Ditch", "Bank"])),
        ("Drainage", SetValidator(valid_values=["Zero", "Low", "Mid", "Good"])),
        ("Humidity", SetValidator(valid_values=["Not determinable", "Very dry", "Dry", "Average", "Wet", "Very wet", "Open water"])),
        ("Type of source rock", NoValidator()),
        ("Soil depth", SetValidator(valid_values=["Skeletal", "Normal", "Deep"])),
        ("Soil surface", SetValidator(valid_values=["Not determinable", "With a smooth crust", "With lumpy structure", "With a gravelly structure"])),
        ("Soil compaction", IntValidator(min=1, max=5)),
        ("Source rock surface", IntValidator(min=0, max=100)),
        ("Pierraille surface", IntValidator(min=1, max=100)),
        ("Sand surface", IntValidator(min=1, max=100)),
        ("Vegetation surface", IntValidator(min=1, max=100)),
        ("Color", SetValidator(valid_values=["Black", "Red/Brown", "Brown", "Clear"])),
        ("Soil sampling", SetValidator(valid_values=["yes", "no"])),
        ("Soil remarks", NoValidator()),
        ("Plant formation type", NoValidator()),
        ("Plant formation name", NoValidator()),
        ("Recovery rate", IntValidator(min=1, max=100)),
        ("Plant formation remarks", NoValidator()),
        ("General remarks", NoValidator())
    ])
