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
        + "File: test/support/file/customer.yaml\n"
        + "\t\tThis is a note.\n"
        + "\t\tThis is a problem.",
        "validator_index_note": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/software.yaml\n\n"
        + "\tIndex: r00000045\n"
        + "\t\tThis is a note.\n"
        + "\t\tThis is a problem.",
        "folio_empty_file": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/empty.yaml\n"
        + "\t\tNo data read from file file.",
        "folio_text_file": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/text.yaml\n"
        + "\t\tNo requirements found in file.",
        "folio_corrupt_file_1": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/corrupt.yaml\n"
        + "\t\tError reading file.",
        "folio_corrupt_file_2": "Validation Report\n"
        + "Problems: 2\n\n"
        + "File: test/support/file/corrupt.yaml\n"
        + "\t\tError reading file.\n"
        + "\t\tError parsing .yaml file.",
        "folio_invalid_index_file": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/invalid_index.yaml\n"
        + "\t\tInvalid index: r0000A045.",
        "folio_duplicate_file": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/duplicate.yaml\n"
        + "\t\tError parsing .yaml file.",
        "folio_yaml_file": "Validation Report\n"
        + "Problems: 3\n\n"
        + "File: test/support/file/yaml.yaml\n"
        + "\t\tInvalid index: test.\n" 
        + "\t\tInvalid index: stuff.\n"
        + "\t\tNo requirements were able to be created from file.",
        "standard_read": "Validation Report\n"
        + "Problems: 1\n\n"
        + "Config file not found. config.yaml should be at project root.",
    }
    return text
