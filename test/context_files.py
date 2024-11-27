import pytest
import os
import shutil


@pytest.fixture
def scratch_path():
    path = os.path.join(os.path.dirname(__file__), "scratch")
    if os.path.exists(path):
        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    return path


@pytest.fixture
def customer_file():
    return os.path.join(os.path.dirname(__file__), "support", "file", "customer.yaml")


@pytest.fixture
def software_file():
    return os.path.join(os.path.dirname(__file__), "support", "file", "software.yaml")
