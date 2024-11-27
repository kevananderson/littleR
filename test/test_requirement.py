from context import littleR
from littleR.requirement import Requirement

from context_requirement import *
from context_files import *


def test_new_requirement(customer_file, requirement_data, requirement_yaml):
    data = requirement_data["new_requirement"]
    yaml = requirement_yaml["new_requirement"]
    req = Requirement.factory(customer_file, data)
    relative_path = os.path.relpath(req.path(), os.getcwd()).replace("\\", "/")
    assert relative_path == "test/support/file/customer.yaml"
    assert req.index == "new1"
    assert req.enabled == True
    assert req.type == "Customer"
    assert req.title == "This is a title"
    assert req.requirement == "The requirement shall be this."
    assert req.is_new() == True
    assert req.int_index() == 1
    assert str(req) == "Requirement(new1)"
    assert req.to_yaml() == yaml


def test_requirement(software_file, requirement_data, requirement_yaml):
    data = requirement_data["requirement"]
    yaml = requirement_yaml["requirement"]
    req = Requirement.factory(software_file, data)
    relative_path = os.path.relpath(req.path(), os.getcwd()).replace("\\", "/")
    assert relative_path == "test/support/file/software.yaml"
    assert req.index == "r00000045"
    assert req.enabled == True
    assert req.type == "Software"
    assert req.title == "Software Title"
    assert req.requirement == "The software shall be this."
    assert req.description == "This is a description."
    assert req.assumptions == "These are the assumptions."
    assert req.component == "Software Component"
    assert req.label == ["label1", "label2"]
    assert req.parent_idx == ["r00000001"]
    assert req.child_idx == ["r00000002", "r00000003"]
    assert req.related_idx == ["r00000004", "r00000005"]
    assert req.is_new() == False
    assert req.int_index() == 45
    assert str(req) == "Requirement(r00000045)"
    print(f"<{req.to_yaml()}>")
    print(f"[{yaml}]")
    assert req.to_yaml() == yaml


valid_index_data = [
    # index, expected
    ("r00000000", True),
    ("r00000001", True),
    ("r00000020", True),
    ("r00000300", True),
    ("r00004000", True),
    ("r00050000", True),
    ("r00600000", True),
    ("r07000000", True),
    ("r80000000", True),
    ("r99999999", True),
    ("r0", False),
    ("r00", False),
    ("r000", False),
    ("r0000", False),
    ("r00000", False),
    ("r000000", False),
    ("r0000000", False),
    ("r000000000", False),
    ("r0000000000", False),
    ("r00000000000", False),
    ("r000000000000", False),
    ("q00000001", False),
    ("!00000001", False),
    ("r-0000001", False),
    ("r000-0001", False),
    ("00000001", False),
    ("r0x000001", False),
    ("r-0000001", False),
    ("r00000001x", False),
    ("r00000001!", False),
    ("r00000001 ", False),
    (" r00000001", False),
    ("", False),
    ("1", False),
    ("r", False),
]


@pytest.mark.parametrize("index, expected", valid_index_data)
def test_valid_index(index, expected):
    assert Requirement.valid_index(index) == expected


new_index_data = [
    # index, expected
    ("new0", True),
    ("new1", True),
    ("new20", True),
    ("new3000", True),
    ("r00000001", False),
    ("r001", False),
    ("newA", False),
    ("new-1", False),
    ("new", False),
    ("n", False),
    ("", False),
    ("1", False),
    ("neq1", False),
    (10, False),
    (("new1", "new2"), False),
    (["new1"], False),
    (["new1", "new2"], False),
    ({"new1", "new2"}, False),
    ({"new1": "new2"}, False),
]


@pytest.mark.parametrize("index, expected", new_index_data)
def test_is_new_index(index, expected):
    assert Requirement.is_new_index(index) == expected


get_int_index_data = [
    # index, expected
    ("new0", 0),
    ("new1", 1),
    ("new20", 20),
    ("new3000", 3000),
    ("new1234567890", 1234567890),
    ("r00000000", 0),
    ("r00000001", 1),
    ("r00000020", 20),
    ("r00000300", 300),
    ("r00004000", 4000),
    ("r00050000", 50000),
    ("r00600000", 600000),
    ("r07000000", 7000000),
    ("r80000000", 80000000),
    ("r99999999", 99999999),
    ("r25664875", 25664875),
    ("r66874963", 66874963),
    ("r45777852", 45777852),
]


@pytest.mark.parametrize("index, expected", get_int_index_data)
def test_get_int_index(index, expected):
    assert Requirement.get_int_index(index) == expected
