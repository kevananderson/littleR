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

        # test directory, is None unless set by the the standard
        # this must be initialize before the file is read
        self._test_directory = None

        # read the file and store its contents, this is flat information
        self._raw_contents = self._read_file()

        # requirements are linked back here just before writing the file
        self._requirements = []

        # parse the file just to check if it is valid
        self.parse_file()

    def path(self):
        """Get the path to the .yaml file.

        This is usually the path that was read. When testing,
        this will return the path to the test directory.

        Returns:
            str: The path to the .yaml file.
        """
        if self._test_directory is not None:
            file_name = os.path.basename(self._path)
            return os.path.join(self._test_directory, file_name)
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
            # we want to read from the actual path of the file, self._path
            with open(self._path, "r", encoding="utf-8") as file:
                data = yaml.load(file)
        except Exception:
            self._validator.file_note(
                self.path(), "Error parsing .yaml file.", problem=True
            )
            self._valid = False
            return []

        # these checks make sure data was returned
        if data is None:
            self._validator.file_note(
                self.path(), "No data read from file file.", problem=True
            )
            return []

        if not isinstance(data, dict) and len(data) > 0:
            self._validator.file_note(
                self.path(), "No requirements found in file.", problem=True
            )
            self._valid = False
            return []

        # now we check the contents of the data by trying to make requirements out of it
        parsed_requirements = []
        for key, value in data.items():

            if not Requirement.valid_index(key):
                self._validator.file_note(
                    self.path(), f"Invalid index: {key}.", problem=True
                )
                # this does not make the file invalid, just skips the requirement
                continue

            value["index"] = key
            # regardless of the "test_directory" we want to create the requirement
            # from the path of the folio
            req = Requirement.factory(self._path, value)

            # change the path if there is a test folder
            if self._test_directory is not None:
                req_file_name = os.path.basename(req.path())
                req_path = os.path.join(self._test_directory, req_file_name)
                req.set_path(req_path)
            
            # we cannot get a duplicate index - we will not check for one.

            # now we add the requirement to the list of requirements
            parsed_requirements.append(req)

        # now check if we have any requirements
        if len(parsed_requirements) == 0:
            self._validator.file_note(
                self.path(),
                "No requirements were able to be created from file.",
                problem=True,
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

    def set_test_directory(self, test_directory):
        """Set the directory where output will be written to.

        Args:
            test_directory (str): The directory where output
                will be written to.

        Raises:
            ValueError: If the test directory is not a valid
                directory.
        """
        # verify the input
        if not isinstance(test_directory, str) or not os.path.isdir(test_directory):
            raise ValueError("The test directory must be a valid directory")
        self._test_directory = test_directory

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
            text += req_text + "\n\n"
        text = text.strip()

        #clear out the requirements after creating the text
        self._requirements = []

        # no need to write if nothing changed
        if text == self._raw_contents:
            return
        
        # write the file
        try:
            # we write with the "path" so that the test directory is used
            with open(self.path(), "w", encoding="utf-8") as file:
                file.write(text)
        except Exception:
            self._validator.file_note(self.path(), "Error writing file.", problem=True)

    def clear(self):
        """Clear the contents of the Folio.

        This is used in testing to reset the object.
        The requirements are cleared and the raw contents are cleared.
        The object is marked as valid for further use.
        """
        self._requirements = []
        self._raw_contents = ""
        self._valid = True

    def _read_file(self):
        try:
            with open(self._path, "r", encoding="utf-8") as file:
                data = file.read()
        except Exception:
            self._validator.file_note(self.path(), "Error reading file.", problem=True)
            self._valid = False
            return None
        return data

    def __str__(self):
        return f"Folio({self._path})"

    def __repr__(self):
        file_name = os.path.basename(self._path)
        return f"Folio({file_name})"

    def __eq__(self, other):
        if not isinstance(other, Folio):
            return False
        return self._path == other._path
