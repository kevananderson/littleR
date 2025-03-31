from context import littleR
from littleR.folio import Folio
from littleR.validate import Validator
from littleR.requirement import Requirement

from context_requirement import *
from context_validate import *
from context_files import *


def test_folio_software_file(software_file, scratch_path):
    v = Validator(scratch_path)
    folio = Folio(software_file, v)
    relative_path = os.path.relpath(folio.path(), os.getcwd()).replace("\\", "/")
    assert relative_path == "test/support/file/software.yaml"
    assert folio.valid() == True
    folio_string = str(folio).replace("\\", "/")
    assert "Folio(" in folio_string
    assert "test/support/file/software.yaml)" in folio_string
    assert f"Folio({folio.path()})" == str(folio)


def test_folio_empty_file(empty_file, scratch_path, reports_text):
    v = Validator(scratch_path)
    folio = Folio(empty_file, v)
    relative_path = os.path.relpath(folio.path(), os.getcwd()).replace("\\", "/")
    assert relative_path == "test/support/file/empty.yaml"
    assert folio.valid() == True
    folio_string = str(folio).replace("\\", "/")
    assert "Folio(" in folio_string
    assert "test/support/file/empty.yaml)" in folio_string
    assert f"Folio({folio.path()})" == str(folio)
    assert v.report() == reports_text["folio_empty_file"]


def test_folio_text_file(text_file, scratch_path, reports_text):
    v = Validator(scratch_path)
    folio = Folio(text_file, v)
    relative_path = os.path.relpath(folio.path(), os.getcwd()).replace("\\", "/")
    assert relative_path == "test/support/file/text.yaml"
    assert folio.valid() == False
    folio_string = str(folio).replace("\\", "/")
    assert "Folio(" in folio_string
    assert "test/support/file/text.yaml)" in folio_string
    assert f"Folio({folio.path()})" == str(folio)
    assert v.report() == reports_text["folio_text_file"]


def test_folio_corrupt_file(corrupt_file, scratch_path, reports_text):
    v = Validator(scratch_path)
    folio = Folio(corrupt_file, v)
    assert folio.valid() == False
    assert f"Folio({folio.path()})" == str(folio)
    assert v.report() == reports_text["folio_corrupt_file_1"]
    folio.parse_file(True)
    assert v.report() == reports_text["folio_corrupt_file_2"]


def test_folio_invalid_index_file(invalid_index_file, scratch_path, reports_text):
    v = Validator(scratch_path)
    folio = Folio(invalid_index_file, v)
    assert folio.valid() == True
    assert f"Folio({folio.path()})" == str(folio)
    assert v.report() == reports_text["folio_invalid_index_file"]


def test_folio_duplicate_file(duplicate_file, scratch_path, reports_text):
    v = Validator(scratch_path)
    folio = Folio(duplicate_file, v)
    assert folio.valid() == False
    assert f"Folio({folio.path()})" == str(folio)
    assert v.report() == reports_text["folio_duplicate_file"]


def test_folio_yaml_file(yaml_file, scratch_path, reports_text):
    v = Validator(scratch_path)
    folio = Folio(yaml_file, v)
    assert folio.valid() == False
    assert f"Folio({folio.path()})" == str(folio)
    assert v.report() == reports_text["folio_yaml_file"]


def test_folio_invalid_file(invalid_file, scratch_path):
    v = Validator(scratch_path)
    with pytest.raises(ValueError):
        folio = Folio(invalid_file, v)


def test_folio_link_and_write(scratch_path, requirement_yaml):
    # create the file in scratch
    software_file = os.path.join(scratch_path, "software.yaml")
    software_yaml = requirement_yaml["requirement"]
    with open(software_file, "w", encoding="utf-8") as file:
        file.write(software_yaml)

    # create the folio and read the requirements
    v = Validator(scratch_path)
    folio = Folio(software_file, v)
    requirements = folio.parse_file()
    assert len(requirements) == 1

    # delete the file
    os.unlink(software_file)
    folio.clear()
    assert os.path.isfile(software_file) == False

    # link and write the file
    for req in requirements:
        folio.link_requirement(req)
    folio.write_file()

    # read the file in scratch
    with open(software_file, "r") as file:
        data = file.read()
    assert data == software_yaml
