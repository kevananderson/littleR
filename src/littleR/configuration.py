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
        self._config = {}

    def read(self, file_path):
        # verify the input
        if not isinstance(file_path, str) or not os.path.isfile(file_path):
            raise ValueError("file_path must be a string to an existing configuration.")

        self._path = file_path

        yaml = ruamel.yaml.YAML()

        config = {}
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

        return self

    def write(self):
        # verify the input
        if self._path is None:
            raise ValueError("The configuration file path must be set.")

        yaml = ruamel.yaml.YAML()

        # write the config
        try:
            with open(self._path, "w", encoding="utf-8") as file:
                yaml.dump(self._config, file)
        except Exception:
            self._validator.note("Error writing config file.", problem=True)
            return False
        
        return True

    def get_logo(self):
        # verify the input
        success, value = self._get_value(["project","logo"])
        
        # did we not get a value
        if not success:
            return ""
        
        #find the file described in the config
        try:
            if not os.path.isabs(value):
                value = os.path.join(os.path.dirname(self._path), value).replace("\\","/")
            if not os.path.isfile(value):
                return ""
        except Exception:
            return ""

        return value        

    def _get_value(self, keys):

        # verify the input
        if not isinstance(keys, list):
            raise TypeError("keys must be a list of strings.")
        for key in keys:
            if not isinstance(key, str):
                raise TypeError("keys in list must be strings.")
        if len(keys) == 0:
            raise ValueError("keys must have at least one element.")
        
        # get the value
        value = self._config
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return (False, None)
            value = value[key]

        return (True, value)
    
    def _set_value(self, keys, value):
        
        # verify the input
        if not isinstance(keys, list):
            raise TypeError("keys must be a list of strings.")
        for key in keys:
            if not isinstance(key, str):
                raise TypeError("keys in list must be strings.")
        if len(keys) == 0:
            raise ValueError("keys must have at least one element.")
        
        # set the value
        config = self._config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
    
    def __str__(self):
        return "Configuration"
    
    def __repr__(self):
        return "Configuration"
