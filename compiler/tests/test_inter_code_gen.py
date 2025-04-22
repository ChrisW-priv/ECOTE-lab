import pytest
from compiler.inter_code_gen import inter_code_gen
from compiler.models import SemanticAnalyzerOutput
from compiler.models import (
    IntermediateCode,
    TypedXmlElement,
    Class,
    Declaration,
    ClassAttribute,
    InstanceAttribute,
)


@pytest.mark.parametrize(
    'semantic_output, expected_inter_code',
    [
        (
            SemanticAnalyzerOutput(
                types=[
                    {ClassAttribute('Name', 'string'), ClassAttribute('attr', '0')},
                ],
                typed_ast=TypedXmlElement(
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
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
            ),
            IntermediateCode(
                types=[
                    Class(
                        name='Class1',
                        attributes=[
                            ClassAttribute(name='Name', attribute_type='string'),
                            ClassAttribute(name='attr', attribute_type='Class1'),
                        ],
                    )
                ],
                declarations=[
                    Declaration(
                        id='0',
                        instance_name='cat',
                        class_name='Class1',
                        attributes=[],
                        is_list=False,
                    ),
                    Declaration(
                        id='1',
                        instance_name='kitten',
                        class_name='Class1',
                        attributes=[
                            InstanceAttribute(
                                name='parent',
                                value=None,
                                ref='0',
                                is_list=False,
                            ),
                        ],
                        is_list=False,
                    ),
                ],
            ),
        ),
        # Test Case 2: Self-Closing Root Element
        (
            SemanticAnalyzerOutput(
                types=[],
                typed_ast=TypedXmlElement(
                    element_name='root',
                    identified_type=-1,
                    identified_role='root',
                ),
            ),
            IntermediateCode(types=[], declarations=[]),
        ),
        # Test Case 3: Abstract Example Compatible with HTML
        (
            SemanticAnalyzerOutput(
                types=[
                    {ClassAttribute('src', 'string')},
                ],
                typed_ast=TypedXmlElement(
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
                                )
                            ],
                        )
                    ],
                ),
            ),
            IntermediateCode(
                types=[Class(name='Class1', attributes=[ClassAttribute(name='src', attribute_type='string')])],
                declarations=[
                    Declaration(id='0', instance_name='img', class_name='Class1', is_list=False, attributes=[]),
                    Declaration(
                        id='1',
                        instance_name='body',
                        class_name='Class1',
                        is_list=True,
                        attributes=[
                            InstanceAttribute(
                                name='img',
                                value=None,
                                ref='0',
                                is_list=False,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    ],
)
def test_inter_code_gen_success(semantic_output, expected_inter_code):
    """
    Test the inter_code_gen function with valid SemanticAnalyzerOutput objects.
    """
    generated_inter_code = inter_code_gen(semantic_output)
    assert generated_inter_code == expected_inter_code
