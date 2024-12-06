from context import littleR
from littleR.folio import Folio
from littleR.validate import Validator
from littleR.requirement import Requirement
from littleR.standard import Standard

from context_requirement import *
from context_validate import *
from context_files import *


def test_standard(support_directory, scratch_path):
    s = Standard("Test Standard",scratch_path)
    s.read(support_directory)
    assert s.file_count() == 2
