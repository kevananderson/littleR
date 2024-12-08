import pytest
import os
import shutil
import itertools


def delete_contents(path):
    if os.path.exists(path) and os.path.isdir(path):
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)


def compare_text(text, expected):
    # verify the input
    if not isinstance(text, str) and not isinstance(expected, str):
        raise TypeError("The text must be strings")

    # this prints the reports next to each other to help compare them
    print(f"\nText Length: {len(text)} vs Expected: {len(expected)}")
    text_lines = text.split("\n")
    expected_lines = expected.split("\n")
    print(f"Text Lines: {len(text_lines)} vs Expected: {len(expected_lines)}")
    for t, e in itertools.zip_longest(text_lines, expected_lines, fillvalue=""):
        print(f"T:{t}")
        print(f"E:{e}\n")


@pytest.fixture
def scratch_path():
    path = os.path.join(os.path.dirname(__file__), "scratch")
    os.makedirs(path, exist_ok=True)
    delete_contents(path)
    yield path
    delete_contents(path)


@pytest.fixture
def customer_file():
    return os.path.join(os.path.dirname(__file__), "support", "file", "customer.yaml")


@pytest.fixture
def software_file():
    return os.path.join(os.path.dirname(__file__), "support", "file", "software.yaml")


@pytest.fixture
def empty_file():
    return os.path.join(os.path.dirname(__file__), "support", "file", "empty.yaml")


@pytest.fixture
def corrupt_file():
    return os.path.join(os.path.dirname(__file__), "support", "file", "corrupt.yaml")


@pytest.fixture
def text_file():
    return os.path.join(os.path.dirname(__file__), "support", "file", "text.yaml")


@pytest.fixture
def invalid_file():
    return os.path.join(os.path.dirname(__file__), "support", "file", "folder.yaml")


@pytest.fixture
def invalid_index_file():
    return os.path.join(
        os.path.dirname(__file__), "support", "file", "invalid_index.yaml"
    )


@pytest.fixture
def duplicate_file():
    return os.path.join(os.path.dirname(__file__), "support", "file", "duplicate.yaml")


@pytest.fixture
def yaml_file():
    return os.path.join(os.path.dirname(__file__), "support", "file", "yaml.yaml")


@pytest.fixture
def support_directory():
    return os.path.join(os.path.dirname(__file__), "support")


@pytest.fixture
def project_1_directory():
    return os.path.join(os.path.dirname(__file__), "support", "project_1")


@pytest.fixture
def project_1_output_directory():
    return os.path.join(os.path.dirname(__file__), "support", "output", "project_1")


@pytest.fixture
def project_2_directory():
    return os.path.join(os.path.dirname(__file__), "support", "project_2")


@pytest.fixture
def project_3_directory():
    return os.path.join(os.path.dirname(__file__), "support", "project_3")


@pytest.fixture
def project_4_directory():
    return os.path.join(os.path.dirname(__file__), "support", "project_4")

@pytest.fixture
def project_5_directory():
    return os.path.join(os.path.dirname(__file__), "support", "project_5")
