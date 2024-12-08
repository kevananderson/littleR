from context import littleR
from littleR.folio import Folio
from littleR.validate import Validator
from littleR.requirement import Requirement
from littleR.standard import Standard

from context_requirement import *
from context_validate import *
from context_files import *

def compare_file_contents(test_files, output_directory):
    for file in test_files:
        with open(file, 'r', encoding="utf-8") as f:
            test_contents = f.read()
        with open(os.path.join(output_directory, os.path.basename(file)), 'r', encoding="utf-8") as f:
            output_contents = f.read()
        assert test_contents == output_contents

def test_standard(project_1_directory, scratch_path, project_1_output_directory):
    s = Standard("Project 1",scratch_path)
    s.read(project_1_directory)
    assert s.file_count() == 3
    s.write()
    folio_paths = s.get_folio_paths()
    compare_file_contents(folio_paths, project_1_output_directory)

