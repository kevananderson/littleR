import pytest


@pytest.fixture
def requirement_data():
    data = {
        "new_requirement": {
            "index": "new1",
            "type": "customer",
            "title": "This is a title",
            "requirement": "The requirement shall be this.",
        },
        "requirement": {
            "index": "r00000045",
            "type": "software",
            "title": "Software Title",
            "requirement": "The software shall be this.",
            "description": "This is a description.",
            "assumptions": "These are the assumptions.",
            "component": "Software Component",
            "label": ["label1", "label2"],
            "parent_idx": ["r00000001"],
            "child_idx": ["r00000002", "r00000003"],
            "related_idx": ["r00000004", "r00000005"],
        },
    }
    return data


@pytest.fixture
def requirement_yaml():
    yaml = {
        "new_requirement": "new1:\n"
        + "  enabled: true\n"
        + "  type: customer\n"
        + "  title: This is a title\n"
        + "  requirement: The requirement shall be this.\n"
        + "  child_idx: []",
        "requirement": "r00000045:\n"
        + "  enabled: true\n"
        + "  type: software\n"
        + "  title: Software Title\n"
        + "  requirement: The software shall be this.\n"
        + "  description: This is a description.\n"
        + "  assumptions: These are the assumptions.\n"
        + "  component: software component\n"
        + "  label:\n"
        + "  - label1\n"
        + "  - label2\n"
        + "  parent_idx:\n"
        + "  - r00000001\n"
        + "  child_idx:\n"
        + "  - r00000002\n"
        + "  - r00000003\n"
        + "  related_idx:\n"
        + "  - r00000004\n"
        + "  - r00000005",
    }
    return yaml
