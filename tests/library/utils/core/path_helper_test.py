import os
from main.library.utils.core.path_helper import get_root_dir

def test_should_get_root_dir():
    root_dir = get_root_dir()
    assert os.path.isfile(os.path.join(root_dir, 'requirements.txt'))