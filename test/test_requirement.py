from context import littleR
from littleR.requirement import Requirement

from context_requirement import *
from context_files import *


def test_new_requirement(customer_file, requirement_data):
    data = requirement_data["new_requirement"]
    req = Requirement.factory(customer_file, data)
    relative_path = os.path.relpath(req.path(), os.getcwd()).replace("\\", "/")
    assert relative_path == "test/support/validate/customer.yaml"
    assert req.index == "new1"
    assert req.type == "Customer"
    assert req.title == "This is a title"
    assert req.requirement == "The requirement shall be this."
    assert req.is_new() == True


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
]


@pytest.mark.parametrize("index, expected", new_index_data)
def test_is_new_index(index, expected):
    assert Requirement.is_new_index(index) == expected
