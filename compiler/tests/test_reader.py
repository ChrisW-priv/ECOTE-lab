import pytest
from unittest.mock import mock_open, patch

from compiler.reader import source_reader


@pytest.fixture
def empty_file():
    m = mock_open(read_data='')
    with patch('builtins.open', m):
        yield m


@pytest.fixture
def non_empty_file():
    m = mock_open(read_data='Hello, World!')
    with patch('builtins.open', m):
        yield m


def test_source_reader_empty(empty_file):
    filename = 'dummy.xml'
    result = list(source_reader(filename))
    assert result == []


def test_source_reader_with_text(non_empty_file):
    expected = list('Hello, World!')
    result = list(source_reader('dummy.xml'))
    assert result == expected
