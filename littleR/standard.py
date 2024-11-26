import os
from validate import Validator
from requirement import Requirement


class Standard:
    def __init__(self, validator=None):
        self.req_dict = {}
        self.tree = []

        self.new_requirements = {}
        self.max_index = 0

        self.validator = validator
        if validator is None:
            validator_path = os.path.join(os.getcwd(), "reports/verification")
            self.validator = Validator(validator_path)

    def add_requirement(self, requirement):
        if requirement is None:
            return
        if not isinstance(requirement, Requirement):
            return
        if not Requirement.valid_index(requirement.index):
            return
        if requirement.index in self.req_dict:
            self.validator.file_note(
                f"Duplicate index: {requirement.index}.", requirement.file, problem=True
            )
            return

        self.req_dict[requirement.index] = requirement

        # we will also record some information about the requirements (new and max index) here.
        if requirement.is_new():
            self.new_requirements[requirement.index] = "Unknown"
        else:
            idx = requirement.int_index()
            if idx > self.max_index:
                self.max_index = idx

    def update_new_requirements(self):
        # for each new requirement, we will replace it with a valid index
        for new_index in self.new_requirements.keys():
            # get the requirement with the new index
            req = self.req_dict.pop(new_index)

            # get the next index
            self.max_index += 1
            index = f"r{self.max_index:08d}"

            # replace the index
            req.index = index
            self.new_requirements[new_index] = index

            # add the requirement back to the dictionary
            self.req_dict[index] = req

    def link_requirements(self):
        """link the requirements

        for each requirement's parent_idx, child_idx, and related_idx, we will:
            * link requirements
            * replace "new" indices with the updated index
        """
        for req in self.req_dict.values():

            # parent_idx
            for i, parent_idx in enumerate(req.parent_idx):
                if parent_idx in self.new_requirements:
                    parent_idx = req.parent_idx[i] = self.new_requirements[parent_idx]

                if parent_idx not in self.req_dict:
                    self.validator.index_note(
                        f"Parent index not found: {parent_idx}.",
                        req.file,
                        req.index,
                        problem=True,
                    )

                parent_req = self.req_dict[parent_idx]

                if parent_req not in req.parents:
                    req.parents.append(parent_req)

            # child_idx
            for i, child_idx in enumerate(req.child_idx):
                if child_idx in self.new_requirements:
                    child_idx = req.child_idx[i] = self.new_requirements[child_idx]

                if child_idx not in self.req_dict:
                    self.validator.index_note(
                        f"Child index not found: {child_idx}.",
                        req.file,
                        req.index,
                        problem=True,
                    )

                child_req = self.req_dict[child_idx]

                if child_req not in req.children:
                    req.children.append(child_req)

            # related_idx
            for i, related_idx in enumerate(req.related_idx):
                if related_idx in self.new_requirements:
                    related_idx = req.related_idx[i] = self.new_requirements[
                        related_idx
                    ]

                if related_idx not in self.req_dict:
                    self.validator.index_note(
                        f"Related index not found: {related_idx}.",
                        req.file,
                        req.index,
                        problem=True,
                    )

                related_req = self.req_dict[related_idx]

                if related_req not in req.related:
                    req.related.append(related_req)

    def build_tree(self):
        """build the tree of requirements

        A requirement is in the tree if it has no parents.
        """
        self.tree = []
        for req in self.req_dict.values():
            if len(req.parents) == 0:
                self.tree.append(req)
        self.tree.sort(key=lambda req: req.int_index())
