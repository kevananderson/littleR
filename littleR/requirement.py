import ruamel.yaml
from folio import Folio


class Requirement:

    def __init__(self):
        # set default values for all fields
        self._folio = None

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
        return self.folio.path()

    def folio(self):
        return self._folio

    def int_index(self):
        """converts the index as an integer value

        Returns:
            int: the integer value of the index
            0: if the index is not valid
        """
        return Requirement.get_int_index(self.index)

    def is_new(self):
        """checks if the requirement is new

        Returns:
            bool: True if the requirement is new, False otherwise
        """
        return Requirement.is_new_index(self.index)

    def to_yaml(self):
        yaml = ruamel.yaml.YAML()
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

        text = yaml.dump_to_string(data)
        return text

    def factory(folio, req_data=None):
        # verify the input
        if not isinstance(folio, Folio) or not folio.valid():
            raise TypeError("folio must be a valid instance of Folio")
        if req_data is None:
            raise ValueError("req_dict must be a dictionary")

        # fill in values from the dictionary
        req = Requirement()

        # folio
        req.folio = folio

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

    def valid_index(index):
        """checks if the index is valid

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
        if index[0] != "r":
            return False
        if not index[1:].isdigit():
            return False
        idx = Requirement.get_int_index(index)
        if idx == 0:
            return False
        return True

    def is_new_index(index):
        """checks if the index is new

        Returns:
            bool: True if the requirement is new, False otherwise
        """
        if index[0:3] != "new":
            return False
        if not index[3:].isdigit():
            return False
        idx = Requirement.get_int_index(index)
        if idx == 0:
            return False
        return True

    def get_int_index(index):
        """converts the index to an integer value

        Args:
            index (str): the index to convert to an integer
                         index is a string in the format r00000000

        Returns:
            int: the integer value of the index
            0: if the index is not valid
        """
        try:
            if Requirement.is_new_index(index):
                return int(index[3:])
            return int(index[1:])
        except Exception:
            return 0

    def __str__(self):
        return f"Requirement({self.index})"

    def __repr__(self):
        return f"{self.index}"

    def __eq__(self, other):
        if not isinstance(other, Requirement):
            return False
        return self.index == other.index and self._folio == other._folio
