"""Requirement class for the littleR project."""

import os
import ruamel.yaml


class Requirement:  # pylint: disable=too-many-instance-attributes
    """Requirement class describing a requirement.

    Attributes:
        _path (str): the file containing the requirement.
        enabled (bool): True if the requirement is enabled, False otherwise.
            Used to hide a requirement without deleting it.
        index (str): the index of the requirement.
            Looks like r00000000 or new1.
        type (str): the type of the requirement.
            The list of types is defined in the configuration file.
        title (str): the title of the requirement
            The title is a short description of the requirement.
        requirement (str): the requirement itself.
            The requirement is a statement of what the system must do.
        description (str): the description of the requirement
            Provides additional information about the requirement.
        assumptions (str): the assumptions of the requirement
            Provides assumptions made when defining the requirement.
        component (str): the component of the requirement
            The component of the system that the requirement defines.
        label (list<str>): the labels of the requirement
            Labels are used to categorize and filter requirements.
        parent_idx (list<str>): the indexes of the parent requirements
        child_idx (list<str>): the indexes of the child requirements
        related_idx (list<str>): the indexes of the related requirements
        parent (list<Requirement>): the parent requirements
        child (list<Requirement>): the child requirements
        related (list<Requirement>): the related requirements
    """

    def __init__(self):
        """Create a new Requirement object."""
        # set default values for all fields
        self._path = None

        self.enabled = True

        self.index = ""
        self.type = ""
        self.title = ""
        self.requirement = ""
        self.description = ""
        self.assumptions = ""

        self.component = ""
        self.label = []

        # lists of indexes
        self.parent_idx = []
        self.child_idx = []
        self.related_idx = []

        # lists of requirements, linked later
        self.parent = []
        self.child = []
        self.related = []

    def path(self):
        """Returns the path where the requirement is defined.

        Returns:
            str: the path to the file defining the requirement
        """
        return self._path

    def int_index(self):
        """Returns the index as an integer value.

        Returns:
            int: the integer value of the index
            0: if the index is not valid
        """
        return Requirement.get_int_index(self.index)

    def is_new(self):
        """Checks if the requirement is new.

        Returns:
            bool: True if the requirement is new, False otherwise
        """
        return Requirement.is_new_index(self.index)

    def to_yaml(self):
        """Converts the requirement to a .yaml string.

        Returns:
            str: the requirement converted to a .yaml string
        """
        yaml = ruamel.yaml.YAML(typ=["rt", "string"])
        content = {}

        content["enabled"] = self.enabled
        content["type"] = self.type
        content["title"] = self.title
        content["requirement"] = self.requirement
        if self.description != "":
            content["description"] = self.description
        if self.assumptions != "":
            content["assumptions"] = self.assumptions
        if self.component != "":
            content["component"] = self.component
        if len(self.label) > 0:
            content["label"] = self.label
        if len(self.parent_idx) > 0:
            content["parent_idx"] = self.parent_idx
        if len(self.child_idx) > 0 or self.type == "customer":
            content["child_idx"] = self.child_idx
        if len(self.related_idx) > 0:
            content["related_idx"] = self.related_idx

        data = {self.index: content}

        # the method exists even though pylint cannot see it.
        text = yaml.dump_to_string(data)  # pylint: disable=no-member
        return text

    @staticmethod
    def factory(file_path, req_data=None):  # pylint: disable=too-many-branches
        """Creates a new Requirement object.

        The req_data (requirement data) comes from reading a .yaml file.

        Args:
            file_path (str): the file containing the requirement.
            req_data (dict): a dictionary containing the requirement data.

        Returns:
            Requirement: the new Requirement object
            None: if the requirement could not be created

        Raises:
            TypeError: if the folio is not a valid instance of Folio
            ValueError: if the req_data is not a dictionary
        """
        # verify the input
        if not isinstance(file_path, str) and os.path.isfile(file_path):
            raise TypeError("file_path must be a valid file name")
        if req_data is None:
            raise ValueError("req_dict must be a dictionary")

        # fill in values from the dictionary
        req = Requirement()

        # folio
        req._path = file_path  # pylint: disable=protected-access

        # index
        if "index" in req_data:
            req.index = req_data["index"]

        # type
        if "type" in req_data:
            req.type = req_data["type"]

        # title
        if "title" in req_data:
            req.title = req_data["title"]

        # requirement
        if "requirement" in req_data:
            req.requirement = req_data["requirement"]

        # description
        if "description" in req_data:
            req.description = req_data["description"]

        # assumptions
        if "assumptions" in req_data:
            req.assumptions = req_data["assumptions"]

        # component
        if "component" in req_data:
            req.component = req_data["component"]

        # label
        if "label" in req_data:
            for label in req_data["label"]:
                if label not in req.label:
                    req.label.append(label)

        # parent_idx
        if "parent_idx" in req_data:
            for parent_idx in req_data["parent_idx"]:
                if parent_idx not in req.parent_idx:
                    req.parent_idx.append(parent_idx)

        # child_idx
        if "child_idx" in req_data:
            for child_idx in req_data["child_idx"]:
                if child_idx not in req.child_idx:
                    req.child_idx.append(child_idx)

        # related_idx
        if "related_idx" in req_data:
            for related_idx in req_data["related_idx"]:
                if related_idx not in req.related_idx:
                    req.related_idx.append(related_idx)

        # return the new requirement
        return req

    @staticmethod
    def valid_index(index):
        """Checks if the index is valid.

        Args:
            index (str): the index to check
                         index is a string in the format r00000000

        Returns:
            bool: True if the index is valid, False otherwise
        """
        if not isinstance(index, str):
            return False
        if Requirement.is_new_index(index):
            return True
        if len(index) != 9:
            return False
        if index[0] != "r":  # pylint: disable=unsubscriptable-object
            return False
        if not index[1:].isdigit():  # pylint: disable=unsubscriptable-object
            return False
        return True

    @staticmethod
    def is_new_index(index):
        """Checks if the index is new.

        Args:
            index (str): the index to check

        Returns:
            bool: True if the requirement is new, False otherwise
        """
        # verify the input
        if not isinstance(index, str):
            return False
        if len(index) < 4:
            return False
        if index[0:3] != "new":  # pylint: disable=unsubscriptable-object
            return False
        if not index[3:].isdigit():  # pylint: disable=unsubscriptable-object
            return False
        return True

    @staticmethod
    def get_int_index(index):
        """Converts the index to an integer value.

        Args:
            index (str): the index to convert to an integer
                         index is a string in the format r00000000

        Returns:
            int: the integer value of the index
            0: if the index is not valid
        """
        if Requirement.is_new_index(index):
            return int(index[3:])  # pylint: disable=unsubscriptable-object
        if Requirement.valid_index(index):
            return int(index[1:])  # pylint: disable=unsubscriptable-object
        return 0

    def __str__(self):
        return f"Requirement({self.index})"

    def __repr__(self):
        return f"{self.index}"

    def __eq__(self, other):
        if not isinstance(other, Requirement):
            return False
        return self.index == other.index and self._path == other._path
