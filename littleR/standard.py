"""Standard class for the littleR project."""

import os
from littleR.validate import Validator
from littleR.requirement import Requirement
from littleR.folio import Folio
from littleR.configuration import Configuration


class Standard:  # pylint: disable=too-many-instance-attributes
    """The Standard class collects all the requirements.

    The standard is the collection of all requirements for a project.
    The class is responsible for reading and writing the requirements.
    It also links the requirements together and validates the standard.

    Attributes:
        _name (str): The name of the standard.
        _requirements (dict): A dictionary of all requirements indexed by their index.
        _new_requirements (dict): A dictionary to translate new
            requirements into the correct format.
        _max_index (int): The maximum index of the requirements.
            The next requirement will be one higher than this.
        _folios (dict): A dictionary of folios indexed by their path.
        _config (dict): The configuration for the standard.
        _validator (Validator): The validator object to use for validation.
        _project_path (str): The path to the project folder.
        _customer_path (str): The path to the customer folder.
        _test_directory (str): The path to the test directory.
    """

    def __init__(self, name="Working", test_directory=None):
        """Create a new Standard object.

        Args:
            name (str): The name of the standard. Used when comparing
                two standards.
            test_directory (str): The path where the standard will output.
                Used for testing.

        Raises:
            TypeError: If the name is not a string.
            TypeError: If the test_directory is not a string.
            ValueError: If the test_directory is not a valid directory.
        """
        # verify the input
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if test_directory is not None:
            if not isinstance(test_directory, str):
                raise TypeError("test_directory must be a string")
            if not os.path.isdir(test_directory):
                raise ValueError("test_directory must be a valid directory")

        # the name of the standard
        self._name = name

        # the requirements in all their forms
        self._requirements = {}

        # keeping track of new requirements and the max index
        self._new_requirements = {}
        self._max_index = 0

        # folios stored by path
        self._folios = {}

        # the config for the standard
        self._config = None

        # test directory
        self._test_directory = test_directory

        # this is where we create the validator for the whole standard.
        validator_path = os.path.join(os.getcwd(), "reports/verification")
        if self._test_directory is not None:
            validator_path = self._test_directory
        self._validator = Validator(validator_path)

        # project and customer paths
        self._project_path = ""
        self._customer_path = ""

    def read(self, directory=None):
        """Read the requirements from the directory.

        This method reads the requirements from the directory,
        populating the requirements and the folios.

        Args:
            directory (str): The directory to read the requirements from.
                If None, the current working directory is used.

        Returns:
            Standard: The modified Standard object.

        Raises:
            ValueError: If the directory is not a valid directory.
        """
        # verify the input
        if directory is None:
            directory = os.getcwd()
        if not isinstance(directory, str):
            raise TypeError("The directory must be a string")
        if not os.path.isdir(directory):
            raise ValueError("The directory must be a valid directory")

        # get the config file
        self._get_config(directory)

        # get the paths to read from
        self._get_paths(directory)

        # get all requirement files in the paths
        self._get_folios()

        # get the raw requirements from the folios
        self._add_requirements()

        # update the new requirements to get valid indices
        self._update_new_requirements()

        # link the requirements together
        self._link_requirements()

        return self

    def write(self):
        """Write the requirements back to file after editing.

        This method writes the requirements back to the files after editing.

        Returns:
            Standard: The modified Standard object.
        """
        # link the requirements to their folios
        for req in self._requirements.values():
            req_folio = self._folios[req.path()]
            req_folio.link_requirement(req)

        # write the requirements to the directory
        for folio in self._folios.values():
            folio.write_file()

        # write the validator report
        self._validator.write_report()

        return self

    def file_count(self):
        """Return the number of requirement files found.

        Returns:
            int: The number of requirement files found.
        """
        return len(self._folios)

    def add_requirement(self, requirement):
        """Add a requirement to the standard.

        The requirement must be unique in the standard.

        Args:
            requirement (Requirement): The requirement to add.

        Raises:
            TypeError: If the requirement is not a Requirement object.
        """
        # verify the input
        if not isinstance(requirement, Requirement):
            raise TypeError("requirement must be an instance of Requirement")

        # check that the requirement is not already present
        if requirement.index in self._requirements:
            first_req = self._requirements[requirement.index]
            second_req = requirement
            second_file = os.path.basename(second_req.path())

            if first_req != second_req:
                self._validator.index_note(
                    first_req,
                    f"Requirement duplicated  file: {second_file}.",
                    problem=True,
                )
            return

        # add the requirement to the dictionary
        self._requirements[requirement.index] = requirement

        # we will also record some information about new and max index here.
        if requirement.is_new():
            self._new_requirements[requirement.index] = "Unknown"
        else:
            idx = requirement.int_index()
            self._max_index = max(self._max_index, idx)

    def get_folio_paths(self):
        """Return the paths to the folios.

        Returns:
            list: A list of the paths to the folios.
        """
        return list(self._folios.keys())

    def get_folio_relative_paths(self):
        """Return the relative paths to the folios.

        Returns:
            list: A list of the relative paths to the folios.
        """
        start_path = os.getcwd()
        return [os.path.relpath(path, start_path) for path in self._folios.keys()]

    def name(self):
        """Return the name of the standard.

        Returns:
            str: The name of the standard.
        """
        return self._name

    def validator(self):
        """Return the validator for the standard.

        Returns:
            Validator: The validator for the standard.
        """
        return self._validator

    def get_requirement(self, index):  # TODO: Test this method
        """Return the requirement with the given index.

        Args:
            index (str): The index of the requirement to return.

        Returns:
            Requirement: The requirement with the given index.
            None: If the requirement is not found.

        Raises:
            TypeError: If the index is not a string.
            ValueError: If the index is not a valid requirement index.
        """
        # verify the input
        if not isinstance(index, str):
            raise TypeError("The index must be a string")
        if not Requirement.valid_index(index):
            raise ValueError("The index must be a valid requirement index")

        return self._requirements.get(index)

    def requirements_iter(self):
        """Return an iterator over the requirements.

        Returns:
            iterator: An iterator over the requirements.
        """
        return iter(self._requirements.values())

    # read methods

    def _get_config(self, directory):
        # verify the input
        if not isinstance(directory, str):
            raise TypeError("The directory must be a string")
        if not os.path.isdir(directory):
            raise ValueError("The directory must be a valid directory")

        config_path = os.path.join(directory, "config.yaml")

        if not os.path.isfile(config_path):
            self._validator.note(
                "Config file not found. config.yaml should be at project root.",
                problem=True,
            )
            return

        self._config = Configuration(self._validator).read(config_path)

    def _get_paths(self, directory):
        # verify the input
        if not isinstance(directory, str):
            raise TypeError("The directory must be a string")
        if not os.path.isdir(directory):
            raise ValueError("The directory must be a valid directory")

        # project folder
        self._project_path = os.path.join(directory, "project")
        if not os.path.isdir(self._project_path):
            self._validator.note(
                "Project path not found at project root.", problem=True
            )
            self._project_path = ""

        # customer folder
        self._customer_path = os.path.join(directory, "customer")
        if not os.path.isdir(self._customer_path):
            self._validator.note("Customer path not found at project root.")
            self._customer_path = ""

    def _get_folios(self):
        # verify required input
        if self._project_path == "" and self._customer_path == "":
            self._validator.note("No project or customer path found.", problem=True)
            return

        # project path
        for root, _, files in os.walk(self._project_path):
            for file in files:
                if file.endswith(".yaml"):
                    folio = Folio(os.path.join(root, file), self._validator)
                    if folio.valid():
                        self._add_folio(folio)

        # customer path
        for root, _, files in os.walk(self._customer_path):
            for file in files:
                if file.endswith(".yaml"):
                    folio = Folio(os.path.join(root, file), self._validator)
                    if folio.valid():
                        self._add_folio(folio)

        if self.file_count() == 0:
            self._validator.note("No requirement files found.", problem=True)

    def _add_folio(self, folio):
        # verify input
        if not isinstance(folio, Folio) or not folio.valid():
            raise TypeError("folio must be a valid instance of Folio")

        if self._test_directory is not None:
            folio.set_test_directory(self._test_directory)

        # add the folio to the dictionary
        path = folio.path()
        if path not in self._folios:
            self._folios[path] = folio

    def _add_requirements(self):
        # verify required input
        if len(self._folios) == 0:
            self._validator.note(
                "Requirements cannot be added if there are no requirement files."
            )  # problem already reported
            return

        # get the requirements from each folio
        for folio in self._folios.values():
            raw_requirements = folio.parse_file()

            for req in raw_requirements:
                self.add_requirement(req)

    def _update_new_requirements(self):
        # for each new requirement, we will replace it with a valid index
        for new_index in self._new_requirements:
            # get the requirement with the new index
            req = self._requirements.pop(new_index)

            # get the next index
            self._max_index += 1
            index = f"r{self._max_index:08d}"

            # replace the index
            req.index = index
            self._new_requirements[new_index] = index

            # add the requirement back to the dictionary
            self._requirements[index] = req

    def _link_requirements(self):  # pylint: disable=too-many-branches
        """Link the requirements.

        for each requirement's parent_idx, child_idx, and related_idx, we will:
            * link requirements
            * replace "new" indices with the updated index
        """
        for req in self._requirements.values():

            # parent_idx
            for i, p_idx in enumerate(req.parent_idx):

                if p_idx in self._new_requirements:
                    p_idx = req.parent_idx[i] = self._new_requirements[p_idx]

                if p_idx not in self._requirements:
                    self._validator.index_note(
                        req,
                        f"Parent index not found: {p_idx}.",
                        problem=True,
                    )
                    # remove the invalid parent index
                    req.parent_idx.remove(p_idx)
                    continue

                parent_req = self._requirements[p_idx]

                if parent_req not in req.parent:
                    req.parent.append(parent_req)
                
                if req not in parent_req.child:
                    parent_req.child.append(req)


            # child_idx
            for i, c_idx in enumerate(req.child_idx):

                if c_idx in self._new_requirements:
                    c_idx = req.child_idx[i] = self._new_requirements[c_idx]

                if c_idx not in self._requirements:
                    self._validator.index_note(
                        req,
                        f"Child index not found: {c_idx}.",
                        problem=True,
                    )
                    # remove the invalid child index
                    req.child_idx.remove(c_idx)
                    continue

                child_req = self._requirements[c_idx]

                if child_req not in req.child:
                    req.child.append(child_req)

                if req not in child_req.parent:
                    child_req.parent.append(req)

            # related_idx
            for i, r_idx in enumerate(req.related_idx):
                if r_idx in self._new_requirements:
                    r_idx = req.related_idx[i] = self._new_requirements[r_idx]

                if r_idx not in self._requirements:
                    self._validator.index_note(
                        req,
                        f"Related index not found: {r_idx}.",
                        problem=True,
                    )
                    # remove the invalid related index
                    req.related_idx.remove(r_idx)
                    continue

                related_req = self._requirements[r_idx]

                if related_req not in req.related:
                    req.related.append(related_req)

                if req not in related_req.related:
                    related_req.related.append(req)
            
    # dunders

    def __str__(self):
        return f"Standard({self._name}): with {len(self._requirements)} requirements."

    def __repr__(self):
        return f"Standard({self._name})"

    def __eq__(self, other):
        if not isinstance(other, Standard):
            return False

        return (
            self._name == other._name
            and len(self._requirements) == len(other._requirements)
            and len(self._folios) == len(other._folios)
        )
