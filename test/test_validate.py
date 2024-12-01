from context import littleR
from littleR.validate import Validator
from littleR.requirement import Requirement

from context_requirement import *
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


def test_validator_index_note(software_file, requirement_data, reports_text):
    v = Validator()
    data = requirement_data["requirement"]
    req = Requirement.factory(software_file, data)
    v.index_note(req, "This is a note.")
    assert v.problem_count() == 0
    v.index_note(req, "This is a problem.", problem=True)
    assert v.problem_count() == 1
    print(f"[{v.report()}]")
    print(f"<{reports_text["validator_index_note"]}>")
    assert v.report() == reports_text["validator_index_note"]


def test_validator_problem_count():
    v = Validator()
    assert v.problem_count() == 0
    v.note("Problems = 0")
    for i in range(1, 11):
        v.note(f"Problems = {i}", problem=True)
        assert v.problem_count() == i


def test_validator_init(scratch_path):
    v = Validator()
    assert v.report() == "Validation Report\nProblems: 0"
    relative_path = os.path.relpath(v.path(), os.getcwd()).replace("\\", "/")
    assert relative_path == "reports/verification"

    v = Validator(scratch_path)
    relative_path = os.path.relpath(v.path(), os.getcwd()).replace("\\", "/")
    assert relative_path == "test/scratch"

    with pytest.raises(TypeError):
        v = Validator(42)
    with pytest.raises(TypeError):
        v = Validator((scratch_path, "test"))
    with pytest.raises(TypeError):
        v = Validator({"path": scratch_path})
    with pytest.raises(ValueError):
        v = Validator("p234dsf")
    with pytest.raises(ValueError):
        v = Validator("test/scratch/not_here")


def test_validator_negative_note():
    v = Validator()

    with pytest.raises(TypeError):
        v.note()
    with pytest.raises(TypeError):
        v.note(42)
    with pytest.raises(TypeError):
        v.note((42, 42))
    with pytest.raises(TypeError):
        v.note({"note": "This is a note."})
    with pytest.raises(TypeError):
        v.note("", problem=42)
    with pytest.raises(TypeError):
        v.note("", problem=(42, 42))


def test_validator_negative_file_note(customer_file):
    v = Validator()

    with pytest.raises(TypeError):
        v.file_note()
    with pytest.raises(TypeError):
        v.file_note(42, "")
    with pytest.raises(TypeError):
        v.file_note("test/scratch/not_here", "42")
    with pytest.raises(TypeError):
        v.file_note({"note": "This is a note."})
    with pytest.raises(TypeError):
        v.file_note(customer_file, 42)
    with pytest.raises(TypeError):
        v.file_note(customer_file, (42, "42"))
    with pytest.raises(TypeError):
        v.file_note(customer_file, "", problem=42)
    with pytest.raises(TypeError):
        v.file_note(customer_file, "This is a problem.", problem=(42, 42))


def test_validator_negative_index_note(software_file, requirement_data):
    v = Validator()
    data = requirement_data["requirement"]
    req = Requirement.factory(software_file, data)

    with pytest.raises(TypeError):
        v.index_note()
    with pytest.raises(TypeError):
        v.index_note(42, "")
    with pytest.raises(TypeError):
        v.index_note("req", "")
    with pytest.raises(TypeError):
        v.index_note(req, 42)
    with pytest.raises(TypeError):
        v.index_note(req, {"42": 42})
    with pytest.raises(TypeError):
        v.index_note(req, "", problem=42)
    with pytest.raises(TypeError):
        v.index_note(req, "This is a problem.", problem="True")
    with pytest.raises(TypeError):
        v.index_note(req, "This is a problem.", problem=42)
