import pytest
from compiler.settings import Settings
from pydantic import ValidationError

def test_settings_initialization(set_sys_argv):
    settings = Settings(input_file="input.xml", output_dir="output")
    assert settings.input_file == "input.xml"
    assert settings.output_dir == "output"

def test_settings_missing_input_file(set_sys_argv):
    with pytest.raises(ValidationError) as exc_info:
        Settings(output_dir="output")
    assert "input_file" in str(exc_info.value)

def test_settings_default_output_dir(set_sys_argv):
    settings = Settings(input_file="input.xml")
    assert settings.output_dir == "generated"
