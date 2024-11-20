import os

class Validator:
    def __init__(self, path=None):
        self.path = path
        if path is None:
            self.path = os.path.join( os.getcwd(), "reports/verification")

        self._problem_count = 0

        self.notes = []
        self.FileValidators = {}

    def note(self, message, problem=False):
        self.notes.append( str(message) )
        if problem:
            self._problem_count += 1
    
    def file_note(self, message, path, problem=False):
        if path not in self.FileValidators:
            self.FileValidators[path] = FileValidator(path)
        
        self.FileValidators[path].note(message)

        if problem:
            self._problem_count += 1

    def index_note(self, message, path, index, problem=False):
        if path not in self.FileValidators:
            self.FileValidators[path] = FileValidator(path)
        
        self.FileValidators[path].index_note(message, index)

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
        for file_validator in self.FileValidators.values():        
            report += file_validator.report()
        return report

class FileValidator():
    def __init__(self, path=""):
        self.path = path
        self.notes = []
        self.IndexValidators = {}
    
    def note(self, message):
        self.notes.append( str(message) )

    def index_note(self, message, index):
        if index not in self.IndexValidators:
            self.IndexValidators[index] = IndexValidator(index)
        self.IndexValidators[index].note(message)

    def report(self):
        report = f"File: {self.path}\n"
        for note in self.notes:
            report += note + "\n"
        report += "\n"
        for index_validator in self.IndexValidators.values():
            report += index_validator.report()
        return report
    
class IndexValidator():
    def __init__(self, index):
        self.index = index
        self.notes = []

    def note(self, message):
        self.notes.append( str(message) )

    def report(self):
        report = f"Index: {self.index}\n"
        for note in self.notes:
            report += f"\t{note}\n"
        report += "\n"
        return report
    
class ValidatorTest:
    
    def unique_index(data):
        pass

