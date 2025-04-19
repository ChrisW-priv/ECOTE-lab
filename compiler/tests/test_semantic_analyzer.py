import pytest
from compiler.semantic_analyzer import semantic_analyzer
from compiler.models import (
    XmlElement,
    ElementAttribute,
    TypedXmlElement,
)
from compiler.errors import SemanticError


@pytest.mark.parametrize(
    'input_ast, expected_typed_ast',
    [
        # Test Case 1: Simple Valid Tree
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='kitten',
                        attributes=[ElementAttribute(name='Name', value='Whiskers')],
                        children=[
                            XmlElement(
                                element_name='parent',
                                children=[
                                    XmlElement(
                                        element_name='cat',
                                        attributes=[ElementAttribute(name='Name', value='The Garfield')],
                                        children=None,
                                    )
                                ],
                            )
                        ],
                    )
                ],
            ),
            TypedXmlElement(
                element_name='root',
                identified_type='variable',
                identified_role=None,
                attributes=None,
                children=[
                    TypedXmlElement(
                        element_name='kitten',
                        identified_type='declaration',
                        identified_role=None,
                        attributes=[ElementAttribute(name='Name', value='Whiskers')],
                        children=[
                            TypedXmlElement(
                                element_name='parent',
                                identified_type='variable',
                                identified_role='attribute_of_parent',
                                attributes=None,
                                children=[
                                    TypedXmlElement(
                                        element_name='cat',
                                        identified_type='declaration',
                                        identified_role='value_of_an_attribute',
                                        attributes=[ElementAttribute(name='Name', value='The Garfield')],
                                        children=None,
                                    )
                                ],
                            )
                        ],
                    )
                ],
            ),
        ),
        # Test Case 2: Self-Closing Root Element
        (
            XmlElement(
                element_name='root',
                children=None,
                attributes=None,
            ),
            TypedXmlElement(
                element_name='root',
                identified_type='variable',
                identified_role=None,
                attributes=None,
                children=None,
            ),
        ),
        # Test Case 3: Nested Elements with Multiple Attributes
        (
            XmlElement(
                element_name='library',
                children=[
                    XmlElement(
                        element_name='book',
                        attributes=[
                            ElementAttribute(name='title', value='1984'),
                            ElementAttribute(name='author', value='George Orwell'),
                        ],
                        children=[
                            XmlElement(
                                element_name='chapter',
                                attributes=[ElementAttribute(name='title', value='Chapter 1')],
                                children=None,
                            ),
                            XmlElement(
                                element_name='chapter',
                                attributes=[ElementAttribute(name='title', value='Chapter 2')],
                                children=None,
                            ),
                        ],
                    )
                ],
            ),
            TypedXmlElement(
                element_name='library',
                identified_type='variable',
                identified_role=None,
                attributes=None,
                children=[
                    TypedXmlElement(
                        element_name='book',
                        identified_type='declaration',
                        identified_role=None,
                        attributes=[
                            ElementAttribute(name='title', value='1984'),
                            ElementAttribute(name='author', value='George Orwell'),
                        ],
                        children=[
                            TypedXmlElement(
                                element_name='chapter',
                                identified_type='declaration',
                                identified_role='value_of_an_attribute',
                                attributes=[ElementAttribute(name='title', value='Chapter 1')],
                                children=None,
                            ),
                            TypedXmlElement(
                                element_name='chapter',
                                identified_type='declaration',
                                identified_role='value_of_an_attribute',
                                attributes=[ElementAttribute(name='title', value='Chapter 2')],
                                children=None,
                            ),
                        ],
                    )
                ],
            ),
        ),
        # Test Case 4: Complex Tree with Multiple Levels
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='kitten',
                        attributes=[ElementAttribute(name='Name', value='Whiskers')],
                        children=[
                            XmlElement(
                                element_name='Parents',
                                children=[
                                    XmlElement(
                                        element_name='cat',
                                        attributes=[ElementAttribute(name='Name', value='The Garfield')],
                                        children=None,
                                    )
                                ],
                            ),
                            XmlElement(
                                element_name='BestFriend',
                                children=[
                                    XmlElement(
                                        element_name='scout',
                                        attributes=[ElementAttribute(name='Name', value='Scout')],
                                        children=None,
                                    )
                                ],
                            ),
                        ],
                    ),
                    XmlElement(
                        element_name='ppl',
                        children=[
                            XmlElement(
                                element_name='john',
                                attributes=[ElementAttribute(name='Name', value='John')],
                                children=None,
                            )
                        ],
                    ),
                    XmlElement(
                        element_name='cars',
                        children=[
                            XmlElement(
                                element_name='car1',
                                attributes=[ElementAttribute(name='Name', value='Lightning')],
                                children=None,
                            ),
                            XmlElement(
                                element_name='car2',
                                attributes=[ElementAttribute(name='Name', value='Sally')],
                                children=None,
                            ),
                        ],
                    ),
                    XmlElement(
                        element_name='newman',
                        attributes=[ElementAttribute(name='Name', value='Joseph')],
                        children=None,
                    ),
                    XmlElement(
                        element_name='paul',
                        attributes=[ElementAttribute(name='Name', value='Paul Atreides')],
                        children=[
                            XmlElement(
                                element_name='Parents',
                                children=[
                                    XmlElement(
                                        element_name='pauls_father',
                                        attributes=[ElementAttribute(name='Name', value='Duke Leto Atreides I')],
                                        children=None,
                                    ),
                                    XmlElement(
                                        element_name='pauls_mother',
                                        attributes=[ElementAttribute(name='Name', value='Lady Jessica')],
                                        children=None,
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
            ),
            TypedXmlElement(
                element_name='root',
                identified_type='variable',
                identified_role=None,
                attributes=None,
                children=[
                    TypedXmlElement(
                        element_name='kitten',
                        identified_type='declaration',
                        identified_role=None,
                        attributes=[ElementAttribute(name='Name', value='Whiskers')],
                        children=[
                            TypedXmlElement(
                                element_name='Parents',
                                identified_type='variable',
                                identified_role='attribute_of_parent',
                                attributes=None,
                                children=[
                                    TypedXmlElement(
                                        element_name='cat',
                                        identified_type='declaration',
                                        identified_role='value_of_an_attribute',
                                        attributes=[ElementAttribute(name='Name', value='The Garfield')],
                                        children=None,
                                    )
                                ],
                            ),
                            TypedXmlElement(
                                element_name='BestFriend',
                                identified_type='variable',
                                identified_role='attribute_of_parent',
                                attributes=None,
                                children=[
                                    TypedXmlElement(
                                        element_name='scout',
                                        identified_type='declaration',
                                        identified_role='value_of_an_attribute',
                                        attributes=[ElementAttribute(name='Name', value='Scout')],
                                        children=None,
                                    )
                                ],
                            ),
                        ],
                    ),
                    TypedXmlElement(
                        element_name='ppl',
                        identified_type='variable',
                        identified_role=None,
                        attributes=None,
                        children=[
                            TypedXmlElement(
                                element_name='john',
                                identified_type='declaration',
                                identified_role='value_of_an_attribute',
                                attributes=[ElementAttribute(name='Name', value='John')],
                                children=None,
                            )
                        ],
                    ),
                    TypedXmlElement(
                        element_name='cars',
                        identified_type='variable',
                        identified_role=None,
                        attributes=None,
                        children=[
                            TypedXmlElement(
                                element_name='car1',
                                identified_type='declaration',
                                identified_role='value_of_an_attribute',
                                attributes=[ElementAttribute(name='Name', value='Lightning')],
                                children=None,
                            ),
                            TypedXmlElement(
                                element_name='car2',
                                identified_type='declaration',
                                identified_role='value_of_an_attribute',
                                attributes=[ElementAttribute(name='Name', value='Sally')],
                                children=None,
                            ),
                        ],
                    ),
                    TypedXmlElement(
                        element_name='newman',
                        identified_type='declaration',
                        identified_role=None,
                        attributes=[ElementAttribute(name='Name', value='Joseph')],
                        children=None,
                    ),
                    TypedXmlElement(
                        element_name='paul',
                        identified_type='declaration',
                        identified_role=None,
                        attributes=[ElementAttribute(name='Name', value='Paul Atreides')],
                        children=[
                            TypedXmlElement(
                                element_name='Parents',
                                identified_type='variable',
                                identified_role='attribute_of_parent',
                                attributes=None,
                                children=[
                                    TypedXmlElement(
                                        element_name='pauls_father',
                                        identified_type='declaration',
                                        identified_role='value_of_an_attribute',
                                        attributes=[ElementAttribute(name='Name', value='Duke Leto Atreides I')],
                                        children=None,
                                    ),
                                    TypedXmlElement(
                                        element_name='pauls_mother',
                                        identified_type='declaration',
                                        identified_role='value_of_an_attribute',
                                        attributes=[ElementAttribute(name='Name', value='Lady Jessica')],
                                        children=None,
                                    ),
                                ],
                            )
                        ],
                    ),
                ],
            ),
        ),
    ],
)
def test_semantic_analyzer_success(input_ast, expected_typed_ast):
    """
    Test the semantic_analyzer with valid XmlElement trees.
    """
    result = semantic_analyzer(input_ast)
    assert result == expected_typed_ast


@pytest.mark.parametrize(
    'input_ast, expected_exception, expected_message',
    [
        # Test Case 1: Root Element Not a Variable
        (
            XmlElement(
                element_name='root',
                attributes=[ElementAttribute(name='Name', value='NotAVariable')],
                children=None,
            ),
            ValueError,
            'The tree must start with a root node.',
        ),
        # Test Case 2: Declaration Under Variable Missing Role
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='kitten',
                        attributes=None,  # Should be a variable, but declared with attributes
                        children=None,
                    )
                ],
            ),
            SemanticError,
            "Element 'kitten' must be a 'declaration' under a 'variable' parent.",
        ),
        # Test Case 3: Variable Element Having Declaration Children
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='variable_node',
                        children=[
                            XmlElement(
                                element_name='declaration_node',
                                attributes=[ElementAttribute(name='Attr', value='Value')],
                                children=None,
                            )
                        ],
                    )
                ],
            ),
            SemanticError,
            "Variable element 'variable_node' cannot have declaration children.",
        ),
        # Test Case 4: Mismatched Types in Tree
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='kitten',
                        attributes=None,  # Should be a variable
                        children=[
                            XmlElement(
                                element_name='parent',
                                attributes=[ElementAttribute(name='Name', value='ParentName')],
                                children=None,
                            )
                        ],
                    )
                ],
            ),
            SemanticError,
            "Element 'kitten' must be a 'declaration' under a 'variable' parent.",
        ),
        # Test Case 5: Multiple Roles Conflict
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='kitten',
                        attributes=[ElementAttribute(name='Name', value='Whiskers')],
                        children=[
                            XmlElement(
                                element_name='parent',
                                attributes=[
                                    ElementAttribute(name='Role', value='Director')
                                ],  # Variable with attributes
                                children=None,
                            )
                        ],
                    )
                ],
            ),
            SemanticError,
            "Variable element 'parent' cannot have declaration children.",
        ),
    ],
)
def test_semantic_analyzer_failure(input_ast, expected_exception, expected_message):
    """
    Test the semantic_analyzer with invalid XmlElement trees expecting SemanticError.
    """
    with pytest.raises(expected_exception) as exc_info:
        semantic_analyzer(input_ast)
    assert str(exc_info.value) == expected_message
