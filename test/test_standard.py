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
    assert s.name() == "Project 1"
    assert s.file_count() == 0
    assert s.get_folio_paths() == []
    assert str(s) == "Standard(Project 1): with 0 requirements."    
    s.read(project_1_directory)
    assert s.file_count() == 3
    assert str(s) == "Standard(Project 1): with 6 requirements."    
    s.write()
    folio_paths = s.get_folio_paths()
    compare_file_contents(folio_paths, project_1_output_directory)

def test_standard_init(scratch_path):
    s = Standard("Project 1",scratch_path)
    assert s.name() == "Project 1"
    
    # test invalid names
    with pytest.raises(TypeError):
        s = Standard(1)
    with pytest.raises(TypeError):
        s = Standard({"name":"Project 1"})
    with pytest.raises(TypeError):        
        s = Standard(["Project 1"])

    # test invalid test paths
    with pytest.raises(TypeError):
        s = Standard("Project 1",1)
    with pytest.raises(TypeError):
        s = Standard("Project 1",Validator())
    with pytest.raises(ValueError):
        s = Standard("Project 1","")
    with pytest.raises(ValueError):
        path = os.path.join(scratch_path, "project_none")
        s = Standard("Project 1",path)
    
def test_standard_read(project_1_directory, scratch_path, reports_text):
    s = Standard("Project 1",scratch_path)
    with pytest.raises(ValueError):
        s.read("")
    with pytest.raises(TypeError):
        s.read(1)
    with pytest.raises(TypeError):
        s.read(Requirement())

    s.read(project_1_directory)
    assert s.validator().report() == reports_text["standard_read"]