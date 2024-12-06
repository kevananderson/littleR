import pytest
import os
import shutil

def delete_contents(path):
    if os.path.exists(path) and os.path.isdir(path):
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

@pytest.fixture
def scratch_path():
    path = os.path.join(os.path.dirname(__file__), "scratch")
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
    return os.path.join(
        os.path.dirname(__file__), "support", "file", "duplicate.yaml"
    )

@pytest.fixture
def yaml_file():
    return os.path.join(
        os.path.dirname(__file__), "support", "file", "yaml.yaml"
    )

@pytest.fixture
def support_directory():
    return os.path.join(
        os.path.dirname(__file__), "support"
    )
