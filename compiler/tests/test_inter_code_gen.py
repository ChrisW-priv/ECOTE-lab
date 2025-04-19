import pytest
from compiler.inter_code_gen import inter_code_gen
from compiler.models import (
    IntermediateCode,
    Class,
    Declaration,
    InstanceAttribute,
    ClassAttribute,
    TypedXmlElement,
    ElementAttribute,
)


@pytest.mark.skip('Intermediate code generation is not yet implemented')
@pytest.mark.parametrize(
    'input_typed_ast, expected_inter_code',
    [
        # Test Case 1: Simple Valid Tree
        (
            TypedXmlElement(
                element_name='root',
                identified_type='variable',
                identified_role='root',
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
            IntermediateCode(
                types=[
                    Class(
                        name='Class1',
                        attributes=[
                            ClassAttribute(name='Name', attribute_type='string'),
                            ClassAttribute(name='parent', attribute_type='Class1'),
                        ],
                    ),
                ],
                declarations=[
                    Declaration(
                        id='cat1',
                        instance_name='cat',
                        class_name='cat',
                        attributes=[
                            InstanceAttribute(name='Name', value='The Garfield'),
                        ],
                    ),
                    Declaration(
                        id='kitten1',
                        instance_name='kitten',
                        class_name='Class1',
                        attributes=[
                            InstanceAttribute(name='Name', value='Whiskers'),
                            InstanceAttribute(name='parent', ref='cat1'),
                        ],
                    ),
                ],
            ),
        ),
        # Test Case 2: Self-Closing Root Element
        (
            TypedXmlElement(
                element_name='root',
                identified_type='variable',
                identified_role='root',
                attributes=None,
                children=None,
            ),
            IntermediateCode(
                types=[],
                declarations=[],
            ),
        ),
        # Test Case 3: Nested Elements with Multiple Attributes
        (
            TypedXmlElement(
                element_name='root',
                identified_type='variable',
                identified_role='root',
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
                    )
                ],
            ),
            IntermediateCode(
                types=[
                    Class(
                        name='Class1',
                        attributes=[
                            ClassAttribute(name='title', attribute_type='string'),
                            ClassAttribute(name='author', attribute_type='string'),
                        ],
                    )
                ],
                declarations=[
                    Declaration(
                        id='book1',
                        instance_name='book',
                        class_name='Class1',
                        attributes=[
                            InstanceAttribute(name='title', value='1984'),
                            InstanceAttribute(name='author', value='George Orwell'),
                        ],
                    )
                ],
            ),
        ),
    ],
)
def test_inter_code_gen_success(input_typed_ast, expected_inter_code):
    """
    Test the inter_code_gen function with valid TypedXmlElement trees.
    """
    result = inter_code_gen(input_typed_ast)
    assert result == expected_inter_code
