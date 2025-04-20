import pytest
from compiler.semantic_analyzer import semantic_analyzer, verify_and_build_typed_ast
from compiler.models import (
    XmlElement,
    ElementAttribute,
)
from compiler.errors import SemanticError


@pytest.mark.skip('this is not stable enough yet')
@pytest.mark.parametrize(
    'input_ast, expected_typed_ast',
    [],
)
def test_semantic_analyzer_success(input_ast, expected_typed_ast):
    """
    Test the semantic_analyzer with valid XmlElement trees.
    """
    result = verify_and_build_typed_ast(input_ast)
    assert result == expected_typed_ast


@pytest.mark.parametrize(
    'input_ast, expected_exception, expected_message',
    [
        # Test Case 1: Root Element Not a ROOT
        (
            XmlElement(
                element_name='var',
            ),
            SemanticError,
            ('The tree must start with a root node.',),
        ),
        # Test Case 2: missing declaration under variable_node
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='kitten',
                    )
                ],
            ),
            SemanticError,
            ('"variable" node has no children',),
        ),
        # Test Case 3: Variable Element Having Variable Children
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='variable_node',
                        children=[
                            XmlElement(
                                element_name='variable_node',
                                children=[XmlElement('declaration_node', attributes=[ElementAttribute('name', 'foo')])],
                            )
                        ],
                    )
                ],
            ),
            SemanticError,
            ("identified_role='variable' cannot have children of role children_role='variable'",),
        ),
        # Test Case 4: declaration followed by declaration
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(  # declaration
                        element_name='kitten',
                        attributes=[ElementAttribute(name='Name', value='Whiskers')],
                        children=[
                            XmlElement(  # declaration
                                element_name='parent',
                                attributes=[ElementAttribute(name='Role', value='Director')],
                            )
                        ],
                    )
                ],
            ),
            SemanticError,
            ("identified_role='declaration' cannot have children of role children_role='declaration'",),
        ),
        # Test Case 5: Variable with Mixed Children Types
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='parents',
                        children=[
                            XmlElement(  # Declaration
                                element_name='pauls_father',
                                attributes=[ElementAttribute(name='Name', value='Duke Leto Atreides I')],
                            ),
                            XmlElement(  # Variable
                                element_name='pauls_mother',
                                children=[
                                    XmlElement(
                                        element_name='pauls_father',
                                        attributes=[ElementAttribute(name='Name', value='Duke Leto Atreides I')],
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            SemanticError,
            (
                "identified_role='variable' has mixed children roles={'declaration', 'variable'}",
                "identified_role='variable' has mixed children roles={'variable', 'declaration'}",
            ),
        ),
    ],
)
def test_semantic_analyzer_failure(input_ast, expected_exception, expected_message):
    """
    Test the semantic_analyzer with invalid XmlElement trees expecting SemanticError.
    """
    with pytest.raises(expected_exception) as exc_info:
        semantic_analyzer(input_ast)
    assert str(exc_info.value) in expected_message
