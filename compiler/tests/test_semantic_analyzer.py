import pytest
from compiler.semantic_analyzer import SemanticAnalyzer
from compiler.models import XmlElement, TypedXmlElement
from compiler.models import ClassAttribute, ElementAttribute
from compiler.errors import SemanticError
from compiler.semantic_analyzer import semantic_analyzer


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
                        children=[
                            TypedXmlElement(
                                element_name='parent',
                                identified_type=0,
                                identified_role='attribute',
                                children=[
                                    TypedXmlElement(
                                        element_name='cat',
                                        identified_type=0,
                                        identified_role='declaration',
                                        attributes=[ElementAttribute('Name', 'The Garfield')],
                                    ),
                                ],
                                attributes=[],
                            ),
                        ],
                        attributes=[ElementAttribute('Name', 'Whiskers')],
                    )
                ],
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
        # Test Case 3: Abstract Example Compatible with HTML
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
                        children=[
                            TypedXmlElement(
                                element_name='img',
                                identified_type=0,
                                identified_role='declaration',
                                attributes=[ElementAttribute('src', 'image.png')],
                            )
                        ],
                        attributes=[],
                        is_list=True,
                    )
                ],
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


@pytest.mark.parametrize(
    'input_xml_element, expected_exception_message',
    [
        # Test Case 1: Declaration node followed by another declaration node without variable node
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='declaration1',
                        attributes=[ElementAttribute(name='attr1', value='value1')],
                        children=[
                            XmlElement(
                                element_name='declaration2',
                                attributes=[ElementAttribute(name='attr2', value='value2')],
                                children=None,
                            )
                        ],
                    )
                ],
            ),
            'declaration node cannot be followed by another declaration node without variable node in between',
        ),
        # Test Case 2: Node with no attributes following a variable node
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='variable1',
                        attributes=[],
                        children=[
                            XmlElement(
                                element_name='variable2',
                                attributes=[],
                                children=None,
                            )
                        ],
                    )
                ],
            ),
            "node with parent_role='variable' was followed by node with identified_role='variable'!",
        ),
        # New Test Case: Declaration node with an attribute that is a list
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='declaration_node',
                        attributes=[ElementAttribute(name='attr', value='value')],
                        children=[
                            XmlElement(
                                element_name='attribute_node',
                                children=[
                                    XmlElement(
                                        element_name='sub_attribute1',
                                        attributes=[ElementAttribute(name='name1', value='value1')],
                                        children=None,
                                    ),
                                    XmlElement(
                                        element_name='sub_attribute2',
                                        attributes=[ElementAttribute(name='name1', value='value2')],
                                        children=None,
                                    ),
                                ],
                            )
                        ],
                    )
                ],
            ),
            'Declaration nodes cannot have attributes that are lists.',
        ),
        # Test Case 3: Leaf node without attributes
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='leaf',
                        attributes=[],  # No attributes should raise error
                        children=None,
                    )
                ],
            ),
            'leaf node has to be a declaration node (must have attributes)',
        ),
        # Test Case 4: Multiple declarations of the same attribute in a single node
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='duplicate_attr',
                        attributes=[
                            ElementAttribute(name='attr', value='value1'),
                            ElementAttribute(name='attr', value='value2'),
                        ],
                        children=None,
                    )
                ],
            ),
            'multiple declarations of one attribute in a single node',
        ),
        # Test Case 5: Multiple different types in a list with strict=True
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='list',
                        children=[
                            XmlElement(
                                element_name='list_item1',
                                attributes=[ElementAttribute(name='attr1', value='value1')],
                                children=None,
                            ),
                            XmlElement(
                                element_name='list_item2',
                                attributes=[ElementAttribute(name='attr2', value='value2')],
                                children=None,
                            ),
                        ],
                    )
                ],
            ),
            'There are multiple different types in the list that is here!',
        ),
        # Test Case 6: multiple items with the same names
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='list',
                        children=[
                            XmlElement(
                                element_name='list_item',
                                attributes=[ElementAttribute(name='attr1', value='value1')],
                                children=None,
                            ),
                            XmlElement(
                                element_name='list_item',
                                attributes=[ElementAttribute(name='attr2', value='value2')],
                                children=None,
                            ),
                        ],
                    )
                ],
            ),
            'element with name=list_item was already found when parsing the tree',
        ),
    ],
)
def test_semantic_analyzer_errors(input_xml_element, expected_exception_message):
    semantic_analyzer = SemanticAnalyzer(input_xml_element)
    with pytest.raises(SemanticError) as exc_info:
        semantic_analyzer.analyze()
    assert str(exc_info.value) == expected_exception_message


@pytest.mark.parametrize(
    'input_xml_element, expected_types',
    [
        # Test Case 1: Single declaration with unique attributes
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='animal',
                        attributes=[ElementAttribute(name='type', value='mammal')],
                    )
                ],
            ),
            [{ClassAttribute('type', 'string')}],
        ),
        # Test Case 2: Multiple declarations with overlapping attributes
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='vehicle1',
                        attributes=[ElementAttribute(name='make', value='Toyota')],
                    ),
                    XmlElement(
                        element_name='vehicle2',
                        attributes=[ElementAttribute(name='make', value='Honda')],
                    ),
                ],
            ),
            [{ClassAttribute('make', 'string')}],
        ),
        # Test Case 3: Multiple declarations but in a list
        (
            XmlElement(
                element_name='root',
                children=[
                    XmlElement(
                        element_name='vehicles',
                        children=[
                            XmlElement(
                                element_name='vehicle1',
                                attributes=[ElementAttribute(name='make', value='Toyota')],
                            ),
                            XmlElement(
                                element_name='vehicle2',
                                attributes=[ElementAttribute(name='make', value='Honda')],
                            ),
                        ],
                    )
                ],
            ),
            [{ClassAttribute('make', 'string')}],
        ),
        # Test Case 4: Declarations with distinct attribute sets
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='person1',
                        attributes=[ElementAttribute(name='name', value='Alice')],
                        children=None,
                    ),
                    XmlElement(
                        element_name='person2',
                        attributes=[ElementAttribute(name='age', value='30')],
                        children=None,
                    ),
                ],
            ),
            [
                {ClassAttribute('name', 'string')},
                {ClassAttribute('age', 'string')},
            ],
        ),
        # Test Case 5: Declarations with distinct attribute sets, but there is one to unify both
        (
            XmlElement(
                element_name='root',
                attributes=[],
                children=[
                    XmlElement(
                        element_name='person0',
                        attributes=[
                            ElementAttribute(name='name', value='Alice'),
                            ElementAttribute(name='age', value='30'),
                        ],
                        children=None,
                    ),
                    XmlElement(
                        element_name='person1',
                        attributes=[ElementAttribute(name='name', value='Alice')],
                        children=None,
                    ),
                    XmlElement(
                        element_name='person2',
                        attributes=[ElementAttribute(name='age', value='30')],
                        children=None,
                    ),
                ],
            ),
            [
                {ClassAttribute('name', 'string'), ClassAttribute('age', 'string')},
            ],
        ),
        # Test Case 6: No declarations (only root)
        (XmlElement(element_name='root'), []),
    ],
)
def test_semantic_analyzer_output_types(input_xml_element, expected_types):
    output = semantic_analyzer(input_xml_element)
    actual_types = output.types
    # Convert sets to sets of frozensets for comparison
    assert set(frozenset(t) for t in actual_types) == set(frozenset(t) for t in expected_types)
