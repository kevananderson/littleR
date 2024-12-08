import pytest


@pytest.fixture
def reports_text():
    text = {
        # validator_notes
        "validator_notes": "Validation Report\n"
        + "Problems: 1\n\n"
        + "This is a note.\n"
        + "This is a problem.",
        # validator_file_notes
        "validator_file_notes": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/customer.yaml\n"
        + "\t\tThis is a note.\n"
        + "\t\tThis is a problem.",
        # validator_index_note
        "validator_index_note": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/software.yaml\n\n"
        + "\tIndex: r00000045\n"
        + "\t\tThis is a note.\n"
        + "\t\tThis is a problem.",
        # folio_empty_file
        "folio_empty_file": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/empty.yaml\n"
        + "\t\tNo data read from file file.",
        # folio_text_file
        "folio_text_file": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/text.yaml\n"
        + "\t\tNo requirements found in file.",
        # folio_corrupt_file_1
        "folio_corrupt_file_1": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/corrupt.yaml\n"
        + "\t\tError reading file.",
        # folio_corrupt_file_2
        "folio_corrupt_file_2": "Validation Report\n"
        + "Problems: 2\n\n"
        + "File: test/support/file/corrupt.yaml\n"
        + "\t\tError reading file.\n"
        + "\t\tError parsing .yaml file.",
        # folio_invalid_index_file
        "folio_invalid_index_file": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/invalid_index.yaml\n"
        + "\t\tInvalid index: r0000A045.",
        # folio_duplicate_file
        "folio_duplicate_file": "Validation Report\n"
        + "Problems: 1\n\n"
        + "File: test/support/file/duplicate.yaml\n"
        + "\t\tError parsing .yaml file.",
        # folio_yaml_file
        "folio_yaml_file": "Validation Report\n"
        + "Problems: 3\n\n"
        + "File: test/support/file/yaml.yaml\n"
        + "\t\tInvalid index: test.\n"
        + "\t\tInvalid index: stuff.\n"
        + "\t\tNo requirements were able to be created from file.",
        # standard_read_project_1
        "standard_read_project_1": "Validation Report\n"
        + "Problems: 1\n\n"
        + "Config file not found. config.yaml should be at project root.",
        # standard_read_project_2
        "standard_read_project_2": "Validation Report\n"
        + "Problems: 2\n\n"
        + "Project path not found at project root.\n"
        + "Customer path not found at project root.\n"
        + "No project or customer path found.\n"
        + "Requirements cannot be added if there are no requirement files.",
        # standard_read_project_3
        "standard_read_project_3": "Validation Report\n"
        + "Problems: 2\n\n"
        + "Config file not found. config.yaml should be at project root.\n"
        + "No requirement files found.\n"
        + "Requirements cannot be added if there are no requirement files.",
        # standard_read_project_4
        "standard_read_project_4": "Validation Report\n"
        + "Problems: 3\n\n"
        + "File: test/scratch/service.yaml\n\n"
        + "\tIndex: r00000001\n"
        + "\t\tParent index not found: r00000015.\n\n"
        + "File: test/scratch/software.yaml\n\n"
        + "\tIndex: r00000004\n"
        + "\t\tRelated index not found: r00000014.\n\n"
        + "File: test/scratch/Acme.yaml\n\n"
        + "\tIndex: r00000003\n"
        + "\t\tChild index not found: r00000013.",
        # standard_read_project_5
        "standard_read_project_5": "Validation Report\n"
        + "Problems: 1\n\n"
        + "Customer path not found at project root.\n\n"
        + "File: test/scratch/first_file.yaml\n\n"
        + "\tIndex: r00000001\n"
        + "\t\tRequirement duplicated  file: second_file.yaml.",
    }
    return text
