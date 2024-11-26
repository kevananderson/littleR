import os
import ruamel.yaml
from validate import Validator
from requirement import Requirement
from folio import Folio
from standard import Standard


class RequireIO:
    def __init__(self, path=None):

        # this is the start of the validator object, all validation starts with reading the requirements
        validator_path = os.path.join(os.getcwd(), "reports/verification")
        self.validator = Validator(validator_path)

        # project base path
        if path is None:
            path = os.getcwd()
        self.path = path

        # project folder
        try:
            self.project_path = os.path.join(self.path, "project")
            if not os.path.isdir(self.project_path):
                self.validator.note(
                    f"Project path not found: {self.project_path}", problem=True
                )
                self.project_path = ""
        except Exception:
            self.validator.note(f"Error finding project path.", problem=True)
            self.project_path = ""

        # customer folder
        if self.customer is not None:
            try:
                self.customer_path = os.path.join(self.path, "customer")
                if not os.path.isdir(self.customer_path):
                    self.validator.note(
                        f"Customer path not found: {self.customer_path}", problem=True
                    )
                    self.customer_path = ""
            except Exception:
                self.validator.note(f"Error finding customer path.", problem=True)
                self.customer_path = ""

        self.standard = Standard(self.validator)

    def read(self):
        # get all requirement files in the path
        req_files = self._get_folios()

        # use the raw requirements to add to the standard
        self._read_requirement_files(req_files)

        # replace new requirements in the standard with the valid indices
        self.standard.update_new_requirements()

        # link the requirements together
        self.standard.link_requirements()

        # find the tree
        self.standard.build_tree()

    def write(self, data):
        with open(self.path, "w") as f:
            f.write(data)

    def _get_folios(self):
        # project path
        if os.path.isdir(self.project_path):
            for root, _, files in os.walk(self.project_path):
                for file in files:
                    if file.endswith(".yaml"):
                        folio = Folio(os.path.join(root, file), self.validator)
                        if folio.valid():
                            self.standard.add_folio(folio)

        # customer path
        if os.path.isdir(self.customer_path):
            for root, _, files in os.walk(self.customer_path):
                for file in files:
                    if file.endswith(".yaml"):
                        folio = Folio(os.path.join(root, file), self.validator)
                        if folio.valid():
                            self.standard.add_folio(folio)

        if self.standard.file_count() == 0:
            self.validator.note("No requirement files found.", problem=True)

    def _read_requirement_files(self):
        # initialize yaml parser
        yaml = ruamel.yaml.YAML()

        # for each file, read it and parse it into requirements, storing them in the list
        for req_file in self.req_files:
            data = None
            try:
                with open(req_file, "r") as file:
                    data = yaml.load(file)
            except Exception:
                self.validator.file_note(f"Error reading file.", req_file, problem=True)

            if data is None:
                self.validator.file_note(
                    f"No data read from file file.", req_file, problem=True
                )

            if len(data) == 0:
                self.validator.file_note(
                    f"No requirements found in file.", req_file, problem=True
                )

            for key, value in data.items():
                if not Requirement.valid_index(key):
                    self.validator.file_note(
                        f"Invalid index: {key}.", req_file, problem=True
                    )
                    continue

                value["index"] = key
                requirement = Requirement(value, req_file)

                if requirement is None:
                    self.validator.index_note(
                        f"Error creating requirement from file.",
                        req_file,
                        key,
                        problem=True,
                    )

                # now we add the requirement to the list of requirements
                self.standard.add_requirement(requirement)

    def _get_config(self):
        """returns a dictionary of the config file

        Returns:
            dict: the config file as a dictionary

        Raises:
            FileNotFoundError: if the config file does not exist
        """
        config_path = os.path.join(self.path, "config.yaml")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"LittleR config file not found at {config_path}")

        yaml = ruamel.yaml.YAML()
        with open(config_path, "r") as file:
            config = yaml.load(file)

        return config

    def __str__(self):
        return f"RequireIO({self.path})"

    def __repr__(self):
        return f"RequireIO({self.path})"
