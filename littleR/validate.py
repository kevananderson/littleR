import os
from folio import Folio
from requirement import Requirement


class Validator:
    def __init__(self, path=None):
        # set the path
        self.path = path
        if path is None:
            self.path = os.path.join(os.getcwd(), "reports/verification")

        # set the problem count to zero
        self._problem_count = 0

        # create store for notes and validators
        self.notes = []
        self.file_notes = {}
        self.index_notes = {}

    def note(self, message, problem=False):
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

    def file_note(self, folio, message, problem=False):
        # verify input
        if not isinstance(folio, Folio) or not folio.valid():
            raise TypeError("folio must be a valid instance of Folio")
        if not isinstance(message, str):
            raise TypeError("message must be a string")
        if not isinstance(problem, bool):
            raise TypeError("problem must be a boolean")

        # get the file note, f
        path = folio.path()
        if path in self.file_notes:
            f = self.file_notes[path]
        else:
            f = FileNote(folio)
            self.file_notes[path] = f

        # add the message to the folio validator
        f.note(message)

        # count the problem if it is one
        if problem:
            self._problem_count += 1

    def index_note(self, requirement, message, problem=False):
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
            f = FileNote(requirement.folio())
            self.file_notes[path] = f

        # get the index note, i
        index = requirement.index
        if index in self.index_notes:
            i = self.index_notes[index]
        else:
            i = IndexNote(requirement)
            self.index_notes[index] = i

        # add the message to the index note
        i.note(message)

        # ensure the index validator is linked to the folio validator
        f.add_index_validator(i)

        # count the problem if it is one
        if problem:
            self._problem_count += 1

    def problem_count(self):
        return self._problem_count

    def report(self):
        report = "Validation Report\n"
        report += "Problems: " + str(self._problem_count) + "\n\n"
        for note in self.notes:
            report += note + "\n"
        report += "\n"
        for f in self.file_notes.values():
            report += f.report()
        return report


class FileNote:
    def __init__(self, folio):
        # verify input
        if not isinstance(folio, Folio):
            raise TypeError("folio must be an instance of Folio")

        self._folio = folio
        self.notes = []
        self.index_validators = []

    def note(self, message):
        # verify input
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        # add the message to the notes
        self.notes.append(message)

    def add_index_validator(self, index_validator):
        # verify input
        if not isinstance(index_validator, IndexNote):
            raise TypeError("index_validator must be an instance of IndexValidator")

        # add the index validator to the list
        if index_validator not in self.index_validators:
            self.index_validators.append(index_validator)

    def report(self):
        path = self._folio.path()
        report = f"File: {path}\n"
        for note in self.notes:
            report += "\t\t" + note + "\n"
        report += "\n"
        for index_validator in self.IndexValidators.values():
            report += index_validator.report()
        return report


class IndexNote:
    def __init__(self, requirement):
        # verify input
        if not isinstance(requirement, Requirement):
            raise TypeError("requirement must be an instance of Requirement")

        self._requirement = requirement
        self.notes = []

    def note(self, message):
        # verify input
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        self.notes.append(message)

    def report(self):
        index = self._requirement.index
        report = f"\tIndex: {index}\n"
        for note in self.notes:
            report += f"\t\t{note}\n"
        report += "\n"
        return report


class ValidatorTest:

    def unique_index(data):
        pass
