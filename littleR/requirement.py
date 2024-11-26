class Requirement:

    def __init__(self, req_dict=None, file=None):
        # set default values for all fields
        self.file = file

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

        # we are done if no dictionary is provided
        if req_dict is None:
            return

        # fill in values from the dictionary

        # index
        if "index" in req_dict:
            self.index = req_dict["index"]

        # type
        if "type" in req_dict:
            self.type = req_dict["type"]

        # title
        if "title" in req_dict:
            self.title = req_dict["title"]

        # requirement
        if "requirement" in req_dict:
            self.requirement = req_dict["requirement"]

        # description
        if "description" in req_dict:
            self.description = req_dict["description"]

        # assumptions
        if "assumptions" in req_dict:
            self.assumptions = req_dict["assumptions"]

        # component
        if "component" in req_dict:
            self.component = req_dict["component"]

        # label
        if "label" in req_dict:
            for label in req_dict["label"]:
                if label not in self.label:
                    self.label.append(label)

        # parent_idx
        if "parent_idx" in req_dict:
            for parent_idx in req_dict["parent_idx"]:
                if parent_idx not in self.parent_idx:
                    self.parent_idx.append(parent_idx)

        # child_idx
        if "child_idx" in req_dict:
            for child_idx in req_dict["child_idx"]:
                if child_idx not in self.child_idx:
                    self.child_idx.append(child_idx)

        # related_idx
        if "related_idx" in req_dict:
            for related_idx in req_dict["related_idx"]:
                if related_idx not in self.related_idx:
                    self.related_idx.append(related_idx)

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
        except:
            return 0

    def __str__(self):
        return f"Requirement({self.index})"

    def __repr__(self):
        return f"{self.index}"
