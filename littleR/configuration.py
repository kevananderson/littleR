"""The Configuration class."""

import os
import ruamel.yaml
from littleR.validate import Validator


class Configuration:
    """The Configuration class.
    Read, write, and manage the configuration of the project.
    """

    def __init__(self, validator):
        # verify the input
        if not isinstance(validator, Validator):
            raise TypeError("validator must be an instance of Validator")
        self._path = None
        self._validator = validator

    def read(self, file_path):
        # verify the input
        if not isinstance(file_path, str) or not os.path.isfile(file_path):
            raise ValueError("file_path must be a string to an existing configuration.")

        self._path = file_path

        yaml = ruamel.yaml.YAML()

        config = None
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                config = yaml.load(file)
        except Exception:
            self._validator.note("Error parsing config file.", problem=True)
            return

        # perform checks to verify the config. look at the folio for
        # inspiration on the checks to perform

        # store the config
        self._config = config

    def write(self):
        pass

    def __str__(self):
        return "Configuration"
