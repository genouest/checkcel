from checkcel import Checkplate
from checkcel.validators import UniqueValidator, SetValidator, DateValidator, NoValidator, IntValidator, FloatValidator
from collections import OrderedDict


class BrasExplor_Population_wild(Checkplate):
    empty_ok = True
    validators = OrderedDict([
        ("Population name", UniqueValidator()),
        ("Sampling date", DateValidator()),
        ("Collector", NoValidator()),
        ("Country", SetValidator(empty_ok=False, valid_values=["Algeria", "Egypt", "France", "Italy", "Slovenia", "Tunisia", "Spain"])),
        ("Region", NoValidator()),
        ("Province", NoValidator()),
        ("Locality", NoValidator()),
        ("Town", NoValidator()),
        ("GPS", NoValidator()),
        ("Altitude", IntValidator(min=0)),
        ("Area (1)", IntValidator(min=0)),
        ("Plant density (2)", FloatValidator(min=0)),
        ("Pop organization (3)", SetValidator(valid_values=["patchs", "continuous"])),
        ("Number of collected plants (4)", IntValidator(min=0, max=30)),
        ("Type of land use (6)", SetValidator(valid_values=["Not determined", "Wasteland or fallow", "Pasture", "Reaping", "Pasture/Reaping", "Annual crops", "Perennial crops", "Field border", "Undergrowth", "Others"])),
        ("Land use intensity (7)", SetValidator(valid_values=["Not determined", "Not cultivated", "Cultivated"])),
        ("Animals (8)", IntValidator(min=0, max=9)),
        ("Soil work (9)", SetValidator(valid_values=["Not determined", "No soil work", "Cultivated field with plowing"])),
        ("Irrigation (10)", SetValidator(valid_values=["no", "yes"])),
        ("Weeding (11)", SetValidator(valid_values=["No", "Chemical", "Mechanical"])),
        ("Artificiality (12)", IntValidator(min=1, max=7)),
        ("Land use comments", NoValidator()),
        ("Station (13)", SetValidator(valid_values=["Sheltered", "Protected", "Open"])),
        ("Exposure (14)", SetValidator(valid_values=["undetermined", "N", "NE", "E", "SE", "S", "SW", "W", "NW"])),
        ("Macro-topography (15)", SetValidator(valid_values=["Closed depression", "Open depression", "Plain", "Plateau", "Lower slope", "Mid slope", "Top of slope", "Summit/Escarpment", "Dunes"])),
        ("Slope (16)", SetValidator(valid_values=["Zero", "from 1 to 10%", "from 11 to 30%", ">31%"])),
        ("Microrelief (17)", SetValidator(valid_values=["Difficult to assess", "Plan", "Bumpy", "Logs", "Channel", "Ditch", "Bank"])),
        ("Drainage (18)", SetValidator(valid_values=["Zero", "Low", "Mid", "Good"])),
        ("Humidity (19)", SetValidator(valid_values=["Not determinable", "Very dry", "Dry", "Average", "Wet", "Very wet", "Open water"])),
        ("Type of source rock (20)", NoValidator()),
        ("Soil depth (21)", SetValidator(valid_values=["Skeletal", "Normal", "Deep"])),
        ("Soil surface (22)", SetValidator(valid_values=["Not determinable", "With a smooth crust", "With lumpy structure", "With a gravelly structure"])),
        ("Soil compaction (23)", IntValidator(min=1, max=5)),
        ("Source rock surface (24)", IntValidator(min=0, max=100)),
        ("Pierraille surface (25)", IntValidator(min=0, max=100)),
        ("Sand surface (26)", IntValidator(min=0, max=100)),
        ("Vegetation surface (27)", IntValidator(min=1, max=100)),
        ("Color (28)", SetValidator(valid_values=["Black", "Red/Brown", "Brown", "clear"])),
        ("Soil sampling (29)", SetValidator(valid_values=["yes", "no"])),
        ("Soil remarks (30)", NoValidator()),
        ("Plant formation type (31)", NoValidator()),
        ("Plant formation name", NoValidator()),
        ("Recovery rate (32)", IntValidator(min=1, max=100)),
        ("Plant formation remarks", NoValidator()),
        ("General remarks (34)", NoValidator())
    ])
