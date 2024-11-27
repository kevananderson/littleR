from context import littleR
from littleR.validate import Validator

from context_validate import *
from context_files import *


def test_validator_notes(reports_text):
    v = Validator()
    v.note("This is a note.")
    assert v.problem_count() == 0
    v.note("This is a problem.", problem=True)
    assert v.problem_count() == 1
    assert v.report() == reports_text["validator_notes"]


def test_validator_file_notes(customer_file, reports_text):
    v = Validator()
    v.file_note(customer_file, "This is a note.")
    assert v.problem_count() == 0
    v.file_note(customer_file, "This is a problem.", problem=True)
    assert v.problem_count() == 1
    assert v.report() == reports_text["validator_file_notes"]
