from Checkcel import logs


class Checkplate(object):
    """ Base class for templates """
    def __init__(self, validators={}):
        self.logger = logs.logger
        self.validators = validators or getattr(self, "validators", {})

    def validate(self):
        raise NotImplementedError

    def generate(self):
        raise NotImplementedError
