from checkcel import logs
from checkcel import exits

import os
import tempfile
import shutil
import sys
import inspect
from copy import deepcopy


class Checkplate(object):
    """ Base class for templates """
    def __init__(self, validators={}, empty_ok=False, ignore_case=False, ignore_space=False):
        self.logger = logs.logger
        self.validators = validators or getattr(self, "validators", {})
        # Will be overriden by validators config
        self.empty_ok = empty_ok
        self.ignore_case = ignore_case
        self.ignore_space = ignore_space
        # self.trim_values = False
        for validator in self.validators:
            validator._set_attributes(self.empty_ok, self.ignore_case, self.ignore_space)

    def load_from_file(self, file_path):
        # Limit conflicts in file name
        with tempfile.TemporaryDirectory() as dirpath:
            shutil.copy2(file_path, dirpath)
            directory, template = os.path.split(file_path)
            sys.path.insert(0, dirpath)

            file = template.split(".")[0]
            mod = __import__(file)
            custom_class = None

            filtered_classes = dict(filter(self._is_valid_template, vars(mod).items()))
            # Get the first one
            if filtered_classes:
                custom_class = list(filtered_classes.values())[0]

        if not custom_class:
            self.logger.error(
                "Could not find a subclass of Checkplate in the provided file."
            )
            return exits.UNAVAILABLE
        self.validators = deepcopy(custom_class.validators)
        self.empty_ok = getattr(custom_class, 'empty_ok', False)
        for key, validator in self.validators.items():
            validator._set_attributes(self.empty_ok, self.ignore_case, self.ignore_space)
        return self

    def validate(self):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError

    def _is_valid_template(self, tup):
        """
        Takes (name, object) tuple, returns True if it's a public Checkplate subclass.
        """
        name, item = tup
        return bool(
            inspect.isclass(item) and issubclass(item, Checkplate) and hasattr(item, "validators") and not name.startswith("_")
        )
