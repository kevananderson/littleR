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
        label (set<str>): the labels of the requirement
            Labels are used to categorize and filter requirements.
        parent_idx (set<str>): the indexes of the parent requirements
        child_idx (set<str>): the indexes of the child requirements
        related_idx (set<str>): the indexes of the related requirements
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
        self.label = set()

        # lists of indexes
        self.parent_idx = set()
        self.child_idx = set()
        self.related_idx = set()

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

    def rel_path(self):
        """Returns the relative path where the requirement is defined.

        Returns:
            str: the path to the file defining the requirement
        """
        base_path = os.getcwd()
        return os.path.relpath(self._path, base_path)

    def set_path(self, file_path):
        """Sets the path where the requirement is defined.

        Args:
            file_path (str): the path to the file defining the requirement

        Raises:
            TypeError: if the file_path is not a string
            ValueError: if the file_path could not be created
        """
        # verify the input
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string.")
        if not os.path.isfile(file_path):
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("")
            except Exception as e:
                raise ValueError("file_path could not be created.") from e
        self._path = file_path

    def add_label(self, label):
        """Adds a label to the requirement.

        Label must be a string and fewer than 100 characters.
        Label is converted to lowercase.
        No duplicate labels are allowed.
        Fails Silently.

        Args:
            label (str): the label to add
        """
        # verify the input
        if not isinstance(label, str):
            return
        if len(label) > 40:
            return
        if len(label) == 0:
            return
        label_lower = label.lower()
        if label_lower not in self.label:
            self.label.add(label_lower)

    def labels(self):
        """Returns the sorted labels of the requirement.

        Returns:
            list: the labels of the requirement sorted.
        """
        return sorted(list(self.label))        

    def delete_label(self, label):
        """Deletes a label from the requirement.

        Label must match an existing label for deletion.
        Fails Silently.

        Args:
            label (str): the label to delete
        """
        # verify the input
        if not isinstance(label, str):
            return
        label_lower = label.lower()
        if label_lower in self.label:
            self.label.remove(label_lower)

    def has_relationship(self, index):
        """Checks if the requirement has a relationship with another requirement.

        Args:
            index (str): the index to check

        Returns:
            bool: True if the requirement has a relationship with the index, False otherwise
        """
        # verify the input
        if not isinstance(index, str):
            return False
        if not Requirement.valid_index(index):
            return False

        if index in self.parent_idx:
            return True
        if index in self.child_idx:
            return True
        if index in self.related_idx:
            return True
        return False

    def add_relationship(self, index, relation_type):
        """Adds a relationship to the requirement.

        The index must be a valid index.
        The relation_type must be a string.
        The relation_type must be either "parent", "child", or "related".
        No duplicate relationships are allowed.
        Fails Silently.

        Args:
            index (str): the index to add
            relation_type (str): the type of relationship to add

        Returns:
            list: the indexes of the relationship added. This can 
                be used to relink the standard.
        """
        # verify the input
        if not isinstance(index, str):
            return []
        if not Requirement.valid_index(index):
            return []
        if not isinstance(relation_type, str):
            return []
        
        relation = relation_type.lower()
        if relation not in ["parent", "child", "related"]:
            return []

        #cannot add an additional time
        if self.has_relationship(index):
            return []
        
        # add the index if you can't find it
        if relation == "parent":
            self.parent_idx.add(index)
        if relation == "child":
            self.child_idx.add(index)
        if relation == "related":
            self.related_idx.add(index)

        return [index, self.index]

    def delete_relationship(self, index):
        """Deletes a relationship from the requirement.

        The index must match an existing relationship for deletion.
        Fails Silently.

        Args:
            index (str): the index to delete

        Returns:
            list: the indexes of the relationship deleted. This can 
                be used to relink the standard.
        """
        # verify the input
        if not isinstance(index, str):
            return []

        #remove the index if you can find it
        self.parent_idx.discard(index)
        self.child_idx.discard(index)
        self.related_idx.discard(index)

        #find related requirements, save and remove
        related = []
        for req in self.parent:
            if req.index == index:
                related.append(req)
                self.parent.remove(req)
        for req in self.child:
            if req.index == index:
                related.append(req)
                self.child.remove(req)
        for req in self.related:
            if req.index == index:
                related.append(req)
                self.related.remove(req)
        
        #remove ourselves from the related requirements
        for req in related:
            req.delete_relationship(self.index)

        if len(related) > 0:
            return [index, self.index]
        
        return []
        
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

    def is_customer(self):
        """Checks if the requirement is a customer requirement.

        Returns:
            bool: True if the requirement is a customer requirement, False otherwise
        """
        return self.type == "customer"
    
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
            content["label"] = sorted(list(self.label))
        if len(self.parent_idx) > 0:
            content["parent_idx"] = sorted(list(self.parent_idx))
        if len(self.child_idx) > 0 or self.type == "customer":
            content["child_idx"] = sorted(list(self.child_idx))
        if len(self.related_idx) > 0:
            content["related_idx"] = sorted(list(self.related_idx))

        data = {self.index: content}

        # the method exists even though pylint cannot see it.
        text = yaml.dump_to_string(data)  # pylint: disable=no-member
        return text

    def to_dict(self):
        """Converts the requirement to a dictionary.

        Returns:
            dict: the requirement converted to a dictionary
        """
        content = {}

        content["path"] = self._path
        content["enabled"] = self.enabled
        content["index"] = self.index
        content["type"] = self.type
        content["title"] = self.title
        content["requirement"] = self.requirement
        content["description"] = self.description
        content["assumptions"] = self.assumptions
        content["component"] = self.component
        content["label"] = self.label
        content["parent_idx"] = self.parent_idx
        content["child_idx"] = self.child_idx
        content["related_idx"] = self.related_idx

        return content
    
    def update_from_dict(self, req_data):
        """Updates the requirement from a dictionary.

        Will try to update the requirement with the data in the dictionary.
        Fails Silently.

        Args:
            req_data (dict): the requirement data to update

        Raises:
            ValueError: if the req_data is not a dictionary
        """
        # verify the input
        if not isinstance(req_data, dict):
            raise ValueError("req_data must be a dictionary")

        # update the requirement
        if "path" in req_data:
            path = req_data["path"]
            if isinstance(path, str) and os.path.isfile(path):
                self._path = path

        if "enabled" in req_data:
            enabled = req_data["enabled"]
            if isinstance(enabled, bool):
                self.enabled = req_data["enabled"]

        if "type" in req_data:
            type = req_data["type"]
            if isinstance(type, str):
                type_lower = type.lower()
                self.type = type_lower

        if "title" in req_data:
            title = req_data["title"]
            if isinstance(title, str):
                self.title = title
        
        if "requirement" in req_data:
            requirement = req_data["requirement"]
            if isinstance(requirement, str):
                self.requirement = requirement
        
        if "description" in req_data:
            description = req_data["description"]
            if isinstance(description, str):
                self.description = description

        if "assumptions" in req_data:
            assumptions = req_data["assumptions"]
            if isinstance(assumptions, str):
                self.assumptions = assumptions

        if "component" in req_data:
            component = req_data["component"]
            if isinstance(component, str):
                self.component = component.lower()
        
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
            req.index = req_data["index"].lower()

        # type
        if "type" in req_data:
            req.type = req_data["type"].lower()

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
            req.component = req_data["component"].lower()

        # label
        if "label" in req_data:
            for label in req_data["label"]:
                req.add_label(label)

        # parent_idx
        if "parent_idx" in req_data:
            for parent_idx in req_data["parent_idx"]:
                if not req.has_relationship(parent_idx):
                    req.parent_idx.add(parent_idx)

        # child_idx
        if "child_idx" in req_data:
            for child_idx in req_data["child_idx"]:
                if not req.has_relationship(child_idx):
                    req.child_idx.add(child_idx)

        # related_idx
        if "related_idx" in req_data:
            for related_idx in req_data["related_idx"]:
                if not req.has_relationship(related_idx):
                    req.related_idx.add(related_idx)

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
