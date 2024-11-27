import pytest


@pytest.fixture
def reports_text():
    text = {
        "validator_notes": "Validation Report\n"
        + "Problems: 1\n\n"
        + "This is a note.\n"
        + "This is a problem.",
        "validator_file_notes": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/validate/customer.yaml\n"
        + "\t\tThis is a note.\n"
        + "\t\tThis is a problem.",
    }
    return text
