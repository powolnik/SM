import pytest
import os
import shutil
import tempfile

@pytest.fixture
def temp_character_dir():
    """Creates a temporary directory structure for character plans."""
    tmp_dir = tempfile.mkdtemp()
    plans_dir = os.path.join(tmp_dir, "plans")
    os.makedirs(plans_dir)
    yield tmp_dir
    shutil.rmtree(tmp_dir)
