import pytest
from compiler.semantic_analyzer import SemanticAnalyzer
from compiler.models import XmlElement, TypedXmlElement
from compiler.models import ClassAttribute, ElementAttribute


@pytest.mark.parametrize(
    'input_identified_types, expected_minimized_types',
    [
        # Test Case 1: Empty input
        ([], []),
        # Test Case 2: No subsets
        (
            [{ClassAttribute('a', 'string')}, {ClassAttribute('b', 'string')}],
            [{ClassAttribute('a', 'string')}, {ClassAttribute('b', 'string')}],
        ),
        # Test Case 3: With subset
        (
            [
                {ClassAttribute('a', 'string')},
                {ClassAttribute('b', 'string')},
                {ClassAttribute('a', 'string'), ClassAttribute('b', 'string')},
            ],
            [{ClassAttribute('a', 'string'), ClassAttribute('b', 'string')}],
        ),
        # Test Case 4: Duplicate sets
        (
            [
                {ClassAttribute('a', 'string'), ClassAttribute('b', 'string')},
                {ClassAttribute('a', 'string'), ClassAttribute('b', 'string')},
            ],
            [{ClassAttribute('a', 'string'), ClassAttribute('b', 'string')}],
        ),
        # Test Case 5: Mixed subsets
        (
            [
                {ClassAttribute('a', 'string')},
                {ClassAttribute('b', 'string')},
                {ClassAttribute('a', 'string'), ClassAttribute('b', 'string')},
                {ClassAttribute('c', 'string')},
            ],
            [{ClassAttribute('a', 'string'), ClassAttribute('b', 'string')}, {ClassAttribute('c', 'string')}],
        ),
    ],
)
def test_minimize_types(input_identified_types, expected_minimized_types):
    semantic_analyzer = SemanticAnalyzer(XmlElement('root'))
    semantic_analyzer.identified_types = input_identified_types
    semantic_analyzer.minimize_types()
    assert set(frozenset(id_type) for id_type in semantic_analyzer.identified_types) == set(
        frozenset(ex_type) for ex_type in expected_minimized_types
    )


@pytest.mark.parametrize(
    'input_xml_element, expected_typed_ast',
    [
        # Test Case 1: Example from README.md
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='kitten',
                        attributes=[ElementAttribute(name='Name', value='Whiskers')],
                        children=[
                            XmlElement(
                                element_name='parent',
                                attributes=[],
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
                identified_type=-1,
                identified_role='root',
                children=[
                    TypedXmlElement(
                        element_name='kitten',
                        identified_type=0,
                        identified_role='declaration',
                        children=None,
                        identified_class=None,
                        is_list=False,
                    )
                ],
                identified_class=None,
                is_list=False,
            ),
        ),
        # Test Case 2: Self-Closing Root Element
        (
            XmlElement(
                element_name='root',
            ),
            TypedXmlElement(
                element_name='root',
                identified_type=-1,
                identified_role='root',
            ),
        ),
        # Test Case 3: Nested Elements with Multiple Attributes
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='book',
                        attributes=[
                            ElementAttribute(name='title', value='1984'),
                            ElementAttribute(name='author', value='George Orwell'),
                        ],
                        children=[
                            XmlElement(
                                element_name='chapters',
                                children=[
                                    XmlElement(
                                        element_name='chapter1',
                                        attributes=[ElementAttribute(name='title', value='Chapter 1')],
                                        children=None,
                                    ),
                                    XmlElement(
                                        element_name='chapter2',
                                        attributes=[ElementAttribute(name='title', value='Chapter 2')],
                                        children=None,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            TypedXmlElement(
                element_name='root',
                identified_type=-1,
                identified_role='root',
                children=[
                    TypedXmlElement(
                        element_name='book',
                        identified_type=0,
                        identified_role='declaration',
                        children=None,
                        identified_class=None,
                        is_list=False,
                    )
                ],
                identified_class=None,
                is_list=False,
            ),
        ),
        # Test Case 4: Abstract Example Compatible with HTML
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='body',
                        attributes=[],
                        children=[
                            XmlElement(
                                element_name='img',
                                attributes=[ElementAttribute(name='src', value='image.png')],
                                children=None,
                            )
                        ],
                    )
                ],
            ),
            TypedXmlElement(
                element_name='root',
                identified_type=-1,
                identified_role='root',
                children=[
                    TypedXmlElement(
                        element_name='body',
                        identified_type=0,
                        identified_role='variable',
                        children=None,
                        identified_class=None,
                        is_list=True,
                    )
                ],
                identified_class=None,
                is_list=False,
            ),
        ),
    ],
)
def test_semantic_analyzer_empty_expected(input_xml_element, expected_typed_ast):
    # Initialize the semantic analyzer with the provided XmlElement
    semantic_analyzer = SemanticAnalyzer(input_xml_element)

    # Perform the semantic analysis
    analyzed_ast = semantic_analyzer.analyze()

    # Compare the analyzed AST with the initially empty expected AST
    assert analyzed_ast == expected_typed_ast
