import pytest
from unittest.mock import patch, Mock
from compiler.default import compiler

def test_compiler_success():
    with patch('compiler.default.pipe') as mock_pipe, \
         patch('compiler.default.writer') as mock_writer:
        
        mock_pipe.return_value.return_value = {"Main.cs": "// C# code"}
        
        compiler("input.xml", "output_dir")
        
        mock_pipe.assert_called()
        mock_writer.assert_called_with({"Main.cs": "// C# code"}, "output_dir")

def test_compiler_exception():
    with patch('compiler.default.pipe', side_effect=Exception("Test Exception")), \
         patch('builtins.print') as mock_print:
        
        compiler("input.xml", "output_dir")
        
        mock_print.assert_called_with("Exception occurred: Exception - Test Exception")
