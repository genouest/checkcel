from checkcel import logs
from checkcel import exits
from checkcel import validators

import inspect
import json
import os
import tempfile
import shutil
import sys
import yaml
from collections import OrderedDict
from copy import deepcopy


class Checkplate(object):
    """ Base class for templates """
    def __init__(self, validators={}, empty_ok=False, ignore_case=False, ignore_space=False, metadata=[], expected_rows=None, na_ok=False):
        self.metadata = metadata
        self.logger = logs.logger
        self.validators = validators or getattr(self, "validators", {})
        self.logs = []
        # Will be overriden by validators config
        self.empty_ok = empty_ok
        self.na_ok = na_ok
        self.ignore_case = ignore_case
        self.ignore_space = ignore_space
        self.expected_rows = expected_rows
        # self.trim_values = False
        for validator in self.validators.values():
            validator._set_attributes(self.empty_ok, self.ignore_case, self.ignore_space)

    def debug(self, message):
        self.logger.debug(message)
        self.logs.append("Debug: {}".format(message))

    def info(self, message):
        self.logger.info(message)
        self.logs.append("Info: {}".format(message))

    def warn(self, message):
        self.logger.warn(message)
        self.logs.append("Warning: {}".format(message))

    def error(self, message):
        self.logger.error(message)
        self.logs.append("Error: {}".format(message))

    def load_from_python_file(self, file_path):
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
            self.error(
                "Could not find a subclass of Checkplate in the provided file."
            )
            return exits.UNAVAILABLE
        self.metadata = getattr(custom_class, 'metadata', [])
        self.validators = deepcopy(custom_class.validators)
        self.empty_ok = getattr(custom_class, 'empty_ok', False)
        self.na_ok = getattr(custom_class, 'na_ok', False)
        self.ignore_case = getattr(custom_class, 'ignore_case', False)
        self.ignore_space = getattr(custom_class, 'ignore_space', False)
        self.expected_rows = getattr(custom_class, 'expected_rows', 0)
        try:
            self.expected_rows = int(self.expected_rows)
        except ValueError:
            self.error(
                "Malformed Checkcel template: expected_rows is not an integer"
            )

        for key, validator in self.validators.items():
            validator._set_attributes(self.empty_ok, self.ignore_case, self.ignore_space, self.na_ok)
        return self

    def load_from_json_file(self, file_path):
        if not os.path.isfile(file_path):
            self.error(
                "Could not find a file at path {}".format(file_path)
            )
            return exits.NOINPUT

        with open(file_path, "r") as f:
            data = json.load(f)

        return self._load_from_dict(data)

    def load_from_yaml_file(self, file_path):
        if not os.path.isfile(file_path):
            self.error(
                "Could not find a file at path {}".format(file_path)
            )
            return exits.NOINPUT

        with open(file_path, "r") as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError:
                self.error(
                    "File {} is not a valid yaml file".format(file_path)
                )
                return exits.UNAVAILABLE

        return self._load_from_dict(data)

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

    def _load_from_dict(self, data):
        if 'validators' not in data or not isinstance(data['validators'], list):
            self.error(
                "Could not find a list of validators in data"
            )
            return exits.UNAVAILABLE

        self.empty_ok = data.get("empty_ok", False)
        self.na_ok = data.get("na_ok", False)
        self.ignore_case = data.get('ignore_case', False)
        self.ignore_space = data.get('ignore_space', False)
        self.expected_rows = data.get('expected_rows', 0)
        try:
            self.expected_rows = int(self.expected_rows)
        except ValueError:
            self.error(
                "Malformed Checkcel template: expected_rows is not an integer"
            )

        validators_list = []
        self.validators = {}
        self.metadata = data.get('metadata', [])

        for validator in data['validators']:
            if 'type' not in validator or 'name' not in validator:
                self.error(
                    "Malformed Checkcel Validator. Require both 'type' and 'name' key"
                )
                return exits.UNAVAILABLE
            options = validator.get('options', {})
            name = validator.get('name')
            try:
                validator_class = getattr(validators, validator['type'])
                val = validator_class(**options)
                val._set_attributes(self.empty_ok, self.ignore_case, self.ignore_space)
            except AttributeError:
                self.error(
                    "{} is not a valid Checkcel Validator".format(validator['type'])
                )
                return exits.UNAVAILABLE

            validators_list.append((name, val))

        self.validators = OrderedDict(validators_list)

        return self
