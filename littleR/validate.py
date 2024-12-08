"""Contains classes that deal with validation of the Standard."""

import os
from littleR.requirement import Requirement


class Validator:
    """The Validator class is responsible for validating the Standard.

    The class is responsible for validating the Standard, including the
    requirements and the folios. It is also responsible for creating a
    validation report.

    This class can be used to perform custom validation rules by creating
    extensions of the ValidatorTest class.

    Attributes:
        _path (str): The path to the directory where the validation report
            will be saved.
        _problem_count (int): The number of problems found during validation.
        notes (list): A list of notes for the validation report.
        file_notes (dict): A dictionary of notes for each file.
        index_notes (dict): A dictionary of notes for each index
    """

    def __init__(self, path=None):
        """Create a new Validator object.

        Args:
            path (str): The path to the directory where the validation report
                will be saved. If None, the default path is used.

        Raises:
            TypeError: If the path is not a string.
            ValueError: If the path is not a valid directory
        """
        # verify the input
        if path is None:
            path = os.path.join(os.getcwd(), "reports/verification")
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if not os.path.isdir(path):
            raise ValueError("path must be a valid directory")

        # set the path
        self._path = path

        # set the problem count to zero
        self._problem_count = 0

        # create store for notes and validators
        self.notes = []
        self.file_notes = {}
        self.index_notes = {}

    def note(self, message, problem=False):
        """Add a note to the validation report.

        Args:
            message (str): The message to add to the report.
            problem (bool): True if the note is a problem, False otherwise.

        Raises:
            TypeError: If the message is not a string or the problem is not a boolean
        """
        # verify input
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        if not isinstance(problem, bool):
            raise TypeError("problem must be a boolean")

        # add the message to the notes
        self.notes.append(message)

        # count the problem if it is one
        if problem:
            self._problem_count += 1

    def file_note(self, file_path, message, problem=False):
        """Add a note to the validation report for a specific file.

        Args:
            file_path (str): The file to add the note about.
            message (str): The message to add to the report.
            problem (bool): True if the note is a problem, False otherwise.

        Raises:
            TypeError: If the file_path is not a string, the message is not a string,
                or the problem is not a boolean.
        """
        # verify input
        if not isinstance(file_path, str) or not os.path.isfile(file_path):
            raise TypeError("file_path must be a valid file path")
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        if not isinstance(problem, bool):
            raise TypeError("problem must be a boolean")

        # get the file note, f
        if file_path in self.file_notes:
            f = self.file_notes[file_path]
        else:
            f = FileNote(file_path)
            self.file_notes[file_path] = f

        # add the message to the folio validator
        f.note(message)

        # count the problem if it is one
        if problem:
            self._problem_count += 1

    def index_note(self, requirement, message, problem=False):
        """Add a note to the validation report for a specific requirement.

        Args:
            requirement (Requirement): The requirement (index) to add the note about.
            message (str): The message to add to the report.
            problem (bool): True if the note is a problem, False otherwise.

        Raises:
            TypeError: If the requirement is not a valid instance of Requirement,
                the message is not a string, or the problem is not a boolean.
        """
        # verify input
        if not isinstance(requirement, Requirement):
            raise TypeError("requirement must be an instance of Requirement")
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        if not isinstance(problem, bool):
            raise TypeError("problem must be a boolean")

        # get the file note, f
        path = requirement.path()
        if path in self.file_notes:
            f = self.file_notes[path]
        else:
            f = FileNote(requirement.path())
            self.file_notes[path] = f

        # get the index note, i
        if requirement.index in self.index_notes:
            i = self.index_notes[requirement.index]
        else:
            i = IndexNote(requirement)
            self.index_notes[requirement.index] = i

        # add the message to the index note
        i.note(message)

        # ensure the index validator is linked to the folio validator
        f.add_index_note(i)

        # count the problem if it is one
        if problem:
            self._problem_count += 1

    def problem_count(self):
        """Get the number of problems found during validation.

        Returns:
            int: The number of problems found during validation.
        """
        return self._problem_count

    def report(self):
        """Create a validation report.

        Returns:
            str: The validation report.
        """
        report = "Validation Report\n"
        report += "Problems: " + str(self._problem_count) + "\n\n"
        for note in self.notes:
            report += note + "\n"
        if len(self.notes) > 0:
            report += "\n"
        for f in self.file_notes.values():
            report += f.report()
        return report.strip()

    def path(self):
        """Get the path to the directory where the validation report will be saved.

        Returns:
            str: The path to the directory where the validation report will be saved.
        """
        return self._path


class FileNote:
    """The FileNote class stores notes about a file (Folio).

    Attributes:
        _path (str): The file that the notes are about.
        notes (list): A list of notes for the file.
        index_notes (list): A list of index validators for the file.
    """

    def __init__(self, file_path):
        """Create a new FileNote object.

        Args:
            file_path (str): The file that the notes are about.

        Raises:
            TypeError: If the folio is not a valid instance of Folio.
        """
        # verify input
        if not isinstance(file_path, str) or not os.path.isfile(file_path):
            raise TypeError("file_path must be a valid file path.")

        self._path = file_path
        self.notes = []
        self.index_notes = []

    def note(self, message):
        """Add a note to the file notes.

        Args:
            message (str): The message to add to the notes.

        Raises:
            TypeError: If the message is not a string.
        """
        # verify input
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        # add the message to the notes
        self.notes.append(message)

    def add_index_note(self, index_note):
        """Add an index validator to the file.

        The FileNote object needs to keep track of all the IndexNote objects
        that are located in the same file so that the report can be generated
        in a useful format.

        Args:
            index_note (IndexNote): The index validator to add to the file.

        Raises:
            TypeError: If the index_note is not an instance of IndexValidator.
        """
        # verify input
        if not isinstance(index_note, IndexNote):
            raise TypeError("index_note must be an instance of IndexValidator")

        # add the index validator to the list
        if index_note not in self.index_notes:
            self.index_notes.append(index_note)

    def report(self):
        """Create a report for the file's portion.

        Returns:
            str: The report for the file's portion.
        """
        relative_path = os.path.relpath(self._path, os.getcwd()).replace("\\", "/")
        report = f"File: {relative_path}\n"
        for note in self.notes:
            report += "\t\t" + note + "\n"
        report += "\n"
        for index_note in self.index_notes:
            report += index_note.report()
        return report


class IndexNote:
    """The IndexNote class is stores notes about an index (Requirement).

    Attributes:
        _requirement (Requirement): The requirement object that the notes are about.
        notes (list): A list of notes for the index.
    """

    def __init__(self, requirement):
        """Create a new IndexNote object.

        Args:
            requirement (Requirement): The requirement object (index)
                that the notes are about.

        Raises:
            TypeError: If the requirement is not a valid instance of Requirement.
        """
        # verify input
        if not isinstance(requirement, Requirement):
            raise TypeError("requirement must be an instance of Requirement")

        self._requirement = requirement
        self.notes = []

    def note(self, message):
        """Add a note to the index notes.

        Args:
            message (str): The message to add to the notes.

        Raises:
            TypeError: If the message is not a string.
        """
        # verify input
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        self.notes.append(message)

    def report(self):
        """Create a report for the index's portion.

        Returns:
            str: The report for the index's portion.
        """
        index = self._requirement.index
        report = f"\tIndex: {index}\n"
        for note in self.notes:
            report += f"\t\t{note}\n"
        report += "\n"
        return report

    def __str__(self):
        return f"Validator({self.problem_count()} problems)"

    def __repr__(self):
        return f"Validator"

    def __eq__(self, other):
        if not isinstance(other, Validator):
            return False
        return self._path == other._path
