import pytest
from unittest import mock
from compiler.reader import source_reader

def test_source_reader_success():
    mock_file = mock.mock_open(read_data="abc")
    with mock.patch("builtins.open", mock_file):
        chars = list(source_reader("dummy.xml"))
        assert chars == ["a", "b", "c"]

def test_source_reader_file_not_found():
    with mock.patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            list(source_reader("nonexistent.xml"))
