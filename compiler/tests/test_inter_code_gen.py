import pytest
from compiler.inter_code_gen import inter_code_gen


@pytest.mark.parametrize(
    'input_typed_ast, expected_inter_code',
    [],
)
def test_inter_code_gen_success(input_typed_ast, expected_inter_code):
    """
    Test the inter_code_gen function with valid and invalid TypedXmlElement trees.
    """
    if isinstance(expected_inter_code, str):
        # Expecting an exception
        with pytest.raises(ValueError) as exc_info:
            inter_code_gen(input_typed_ast)
        assert str(exc_info.value) == expected_inter_code
    else:
        # Expecting a valid IntermediateCode
        result = inter_code_gen(input_typed_ast)
        assert result == expected_inter_code
