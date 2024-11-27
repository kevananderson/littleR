"""This module contains the Folio class."""

import os
import ruamel.yaml
from littleR.validate import Validator
from littleR.requirement import Requirement


class Folio:
    """The Folio class represents a .yaml file containing requirements.

    The class is responsible for reading and writing the file, as well
    as parsing the contents to create Requirement objects.

    Attributes:
        _path (str): The path to the .yaml file.
        _validator (Validator): The validator object to use for validation.
        _valid (bool): True if the Folio is linked to a valid file, False otherwise.
        _raw_contents (str): The raw contents of the file.
        _requirements (list): The list of Requirement objects created from the file.
            This list is only populated just before writing the file.
    """

    def __init__(self, path, validator):
        """Create a new Folio object.

        File is read at object creation and parsed to check for validity.

        Args:
            path (str): The path to the .yaml file.
            validator (Validator): The validator object to use for validation.

        Raises:
            TypeError: If the path is not a string or the validator is not a
                Validator object.
            ValueError: If the path does not end with .yaml or the file does not exist.
        """
        # verify the input
        if not isinstance(path, str):
            raise TypeError("The path must be a string")
        if not path.endswith(".yaml") or not os.path.isfile(path):
            raise ValueError("The path must be a file ending in .yaml")
        if not isinstance(validator, Validator):
            raise ValueError("The validator must be an instance of the Validator class")

        # store the path
        self._path = path

        # store the validator
        self._validator = validator
        self._valid = True

        # read the file and store its contents, this is flat information
        self._raw_contents = self._read_file()

        # requirements are linked back here just before writing the file
        self._requirements = []

        # parse the file just to check if it is valid
        self.parse_file()

    def path(self):
        """Get the path to the .yaml file.

        Returns:
            str: The path to the .yaml file.
        """
        return self._path

    def valid(self):
        """Check if the Folio is linked to a valid file.

        Returns:
            bool: True if the Folio is linked to a valid file, False otherwise.
        """
        return self._valid

    def parse_file(self, force=False):
        """Parse the contents of the file to create Requirement objects.

        This process also validates the contents of the file.
        If the file is not valid, an empty list is returned.
        If the file has already been parsed and marked invalid,
        the file is not re-parsed unless force is True.

        Args:
            force (bool): If True, the file is re-parsed even if
                it has been marked invalid.

        Returns:
            list: A list of Requirement objects created from the file.
        """
        # verify input
        if not isinstance(force, bool):
            raise TypeError("force must be a boolean")

        # we don't need to parse an invalid file
        if not self.valid() and not force:
            return []

        # clear the requirements and status
        self._requirements = []
        self._valid = True

        # initialize yaml parser
        yaml = ruamel.yaml.YAML()

        # read the file and parse it to verify the contents
        data = None
        try:
            with open(self._path, "r", encoding="utf-8") as file:
                data = yaml.load(file)
        except Exception:
            self._validator.file_note(self, "Error parsing .yaml file.", problem=True)
            self._valid = False

        # these checks make sure data was returned
        if data is None:
            self._validator.file_note(
                self, "No data read from file file.", problem=True
            )
            self._valid = False
            return []

        if len(data) == 0:
            self._validator.file_note(
                self, "No requirements found in file.", problem=True
            )
            self._valid = False
            return []

        # now we check the contents of the data by trying to make requirements out of it
        parsed_requirements = []
        for key, value in data.items():

            if not Requirement.valid_index(key):
                self._validator.file_note(self, f"Invalid index: {key}.", problem=True)
                # this does not make the file invalid, just skips the requirement
                continue

            value["index"] = key
            requirement = Requirement.factory(self, value)

            if requirement is None:
                self._validator.file_note(
                    self,
                    f"Error creating requirement with key <{key}> from file.",
                    problem=True,
                )
                # this does not make the file invalid, just skips the requirement
                continue

            if requirement in parsed_requirements:
                self._validator.file_note(
                    self,
                    f"Duplicate requirement with index <{key}> found in file. "
                    + "Second instance deleted.",
                    problem=True,
                )
                # this does not make the file invalid, just skips the requirement
                continue

            # now we add the requirement to the list of requirements

            parsed_requirements.append(requirement)

        # now check if we have any requirements
        if len(parsed_requirements) == 0:
            self._validator.file_note(
                self, "No requirements were able to be created from file.", problem=True
            )
            self._valid = False
            return []

        # return the list of requirements
        return parsed_requirements

    def link_requirement(self, requirement):
        """Link a Requirement object to the Folio.

        This is only called just before the file is written.
        With the requirements linked, the file can be written.

        Args:
            requirement (Requirement): The Requirement object to link.

        Raises:
            TypeError: If the requirement is not a Requirement object.
        """
        # verify the input
        if not isinstance(requirement, Requirement):
            raise TypeError("requirement must be an instance of Requirement")
        if requirement not in self._requirements:
            self._requirements.append(requirement)

    def write_file(self):
        """Write the contents of the Folio to the .yaml file.

        Before calling this, ensure that requirement objects are
        linked to the Folio by calling link_requirement().

        If the Folio is not valid, the file is not written.
        """
        # we don't need to write an invalid file
        if not self.valid():
            return

        # create the text to write
        text = ""
        for req in self._requirements:
            try:
                req_text = req.to_yaml()
            except Exception:
                self._validator.index_note(
                    req, "Error creating .yaml text from requirement.", problem=True
                )
                continue
            text += req_text + "\n"
        text = text.strip()

        # write the file
        try:
            with open(self._path, "w", encoding="utf-8") as file:
                file.write(text)
        except Exception:
            self._validator.file_note(self, "Error writing file.", problem=True)

    def _read_file(self):
        try:
            with open(self._path, "r", encoding="utf-8") as file:
                data = file.read()
        except Exception:
            self._validator.file_note(self, "Error reading file.", problem=True)
            self._valid = False
            return None
        return data

    def __str__(self):
        return f"Folio({self._path})"

    def __repr__(self):
        return f"Folio({self._path})"

    def __eq__(self, other):
        if not isinstance(other, Folio):
            return False
        return self._path == other._path