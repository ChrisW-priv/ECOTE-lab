import pytest
import os
from unittest import mock
from compiler.writer import writer

def test_writer_creates_output_dir():
    with mock.patch("os.makedirs") as mock_makedirs, \
         mock.patch("builtins.open", mock.mock_open()):
        
        file_map = {"Main.cs": "// C# code"}
        writer(file_map, "output_dir")
        
        mock_makedirs.assert_called_with("output_dir", exist_ok=True)

def test_writer_writes_files_correctly():
    with mock.patch("os.makedirs"), \
         mock.patch("builtins.open", mock.mock_open()) as mock_file:
        
        file_map = {"Main.cs": "// C# code", "Utils.cs": "// Utils code"}
        writer(file_map, "output_dir")
        
        assert mock_file.call_count == 2
        mock_file.assert_any_call(os.path.join("output_dir", "Main.cs"), "w")
        mock_file.assert_any_call(os.path.join("output_dir", "Utils.cs"), "w")
