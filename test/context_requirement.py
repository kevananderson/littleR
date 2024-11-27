import pytest


@pytest.fixture
def requirement_data():
    data = {
        "new_requirement": {
            "index": "new1",
            "type": "Customer",
            "title": "This is a title",
            "requirement": "The requirement shall be this.",
        },
    }
    return data
