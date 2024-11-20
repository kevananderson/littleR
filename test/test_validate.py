from context import littleR

from littleR.validate import Validator

def test_validator_notes():
    v = Validator()
    v.note("This is a note.")
    assert v.problem_count() == 0
    v.note("This is a problem.", problem=True)
    assert v.problem_count() == 1
    