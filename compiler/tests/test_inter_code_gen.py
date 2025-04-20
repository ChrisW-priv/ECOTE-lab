import pytest
from compiler.inter_code_gen import inter_code_gen


@pytest.mark.skip('Intermediate code generation is not yet implemented')
@pytest.mark.parametrize(
    'input_typed_ast, expected_inter_code',
    [],
)
def test_inter_code_gen_success(input_typed_ast, expected_inter_code):
    """
    Test the inter_code_gen function with valid TypedXmlElement trees.
    """
    result = inter_code_gen(input_typed_ast)
    assert result == expected_inter_code
