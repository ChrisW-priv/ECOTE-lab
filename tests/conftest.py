import sys
import pytest

@pytest.fixture
def set_sys_argv():
    sys.argv = ['input.xml', '--output_dir', 'output']
