from checkcel import Checkplate
from checkcel.validators import NoValidator, SetValidator
from collections import OrderedDict


class MyTemplate(Checkplate):
    validators = OrderedDict([
        ("*sample_name", NoValidator()),
        ("sample_title", NoValidator()),
        ("bioproject_accession", NoValidator()),
        ("*organism", NoValidator()),
        ("strain", NoValidator()),
        ("isolate", NoValidator()),
        ("breed", NoValidator()),
        ("cultivar", NoValidator()),
        ("ecotype", NoValidator()),
        ("age", NoValidator()),
        ("dev_stage", NoValidator()),
        ("*sex", SetValidator(valid_values=["male", "female", "pooled male and female", "neuter", "hermaphrodite", "intersex", "not determined", "missing", "not applicable", "not collected"])),
        ("*tissue", NoValidator()),
        ("biomaterial_provider", NoValidator()),
        ("birth_date", NoValidator()),
        ("birth_location", NoValidator()),
        ("breeding_history", NoValidator()),
        ("breeding_method", NoValidator()),
        ("cell_line", NoValidator()),
        ("cell_subtype", NoValidator()),
        ("cell_type", NoValidator()),
        ("collected_by", NoValidator()),
        ("collection_date", NoValidator()),
        ("culture_collection", NoValidator()),
        ("death_date", NoValidator()),
        ("disease", NoValidator()),
        ("disease_stage", NoValidator()),
        ("genotype", NoValidator()),
        ("geo_loc_name", NoValidator()),
        ("growth_protocol", NoValidator()),
        ("health_state", NoValidator()),
        ("isolation_source", NoValidator()),
        ("lat_lon", NoValidator()),
        ("phenotype", NoValidator()),
        ("sample_type", NoValidator()),
        ("specimen_voucher", NoValidator()),
        ("store_cond", NoValidator()),
        ("stud_book_number", NoValidator()),
        ("treatment", NoValidator()),
        ("description", NoValidator())
    ])
