from compiler.code_gen import code_gen
from compiler.models import TypedTree


def test_code_gen_returns_correct_structure():
    typed_ast = TypedTree(types=[], declarations=[])
    result = code_gen(typed_ast)
    assert isinstance(result, dict)
    assert "Main.cs" in result
    assert result["Main.cs"] == ""


def test_code_gen_with_data():
    # Assuming code_gen will process typed_ast and generate code,
    # here we mock a simple TypedTree.
    typed_ast = TypedTree(
        types=[...],  # Populate as needed
        declarations=[...]
    )
    result = code_gen(typed_ast)
    # Add assertions based on expected output
    # Example:
    # assert result["Main.cs"] == "expected C# code"
