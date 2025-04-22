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
    ElementAttribute,
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
        # New Test Case
        (
            SemanticAnalyzerOutput(
                typed_ast=TypedXmlElement(
                    element_name='root',
                    identified_type=-1,
                    identified_role='root',
                    children=[
                        TypedXmlElement(
                            element_name='flower',
                            identified_type=1,
                            identified_role='declaration',
                            children=None,
                            attributes=[ElementAttribute(name='kind', value='Iris')],
                            identified_class=None,
                            is_list=False,
                        ),
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
                                            children=None,
                                            attributes=[ElementAttribute(name='Name', value='The Garfield')],
                                            identified_class=None,
                                            is_list=False,
                                        ),
                                    ],
                                    attributes=None,
                                    identified_class=None,
                                    is_list=False,
                                )
                            ],
                            attributes=[ElementAttribute(name='Name', value='Whiskers')],
                            identified_class=None,
                            is_list=False,
                        ),
                    ],
                    attributes=None,
                    identified_class=None,
                    is_list=False,
                ),
                types=[
                    {
                        ClassAttribute(name='Name', attribute_type='string'),
                        ClassAttribute(name='parent', attribute_type='1'),
                    },
                    {ClassAttribute(name='kind', attribute_type='string')},
                ],
            ),
            IntermediateCode(
                types=[
                    Class(
                        name='Class1',
                        attributes=[
                            ClassAttribute(name='parent', attribute_type='Class2'),
                            ClassAttribute(name='Name', attribute_type='string'),
                        ],
                    ),
                    Class(name='Class2', attributes=[ClassAttribute(name='kind', attribute_type='string')]),
                ],
                declarations=[
                    Declaration(
                        id='0',
                        instance_name='flower',
                        class_name='Class2',
                        attributes=[InstanceAttribute(name='kind', value='Iris', ref=None, is_list=False)],
                        is_list=False,
                    ),
                    Declaration(
                        id='1',
                        instance_name='cat',
                        class_name='Class1',
                        attributes=[InstanceAttribute(name='Name', value='The Garfield', ref=None, is_list=False)],
                        is_list=False,
                    ),
                    Declaration(
                        id='2',
                        instance_name='kitten',
                        class_name='Class1',
                        attributes=[
                            InstanceAttribute(name='Name', value='Whiskers', ref=None, is_list=False),
                            InstanceAttribute(name='parent', value=None, ref='1', is_list=False),
                        ],
                        is_list=False,
                    ),
                ],
            ),
        ),
        # New Test Case for example3.xml
        (
            SemanticAnalyzerOutput(
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
                                    element_name='Parent',
                                    identified_type=0,
                                    identified_role='attribute',
                                    children=[
                                        TypedXmlElement(
                                            element_name='cat',
                                            identified_type=0,
                                            identified_role='declaration',
                                            children=None,
                                            attributes=[ElementAttribute(name='Name', value='The Garfield')],
                                            identified_class=None,
                                            is_list=False,
                                        )
                                    ],
                                    attributes=None,
                                    identified_class=None,
                                    is_list=False,
                                ),
                                TypedXmlElement(
                                    element_name='BestFriend',
                                    identified_type=0,
                                    identified_role='attribute',
                                    children=[
                                        TypedXmlElement(
                                            element_name='scout',
                                            identified_type=0,
                                            identified_role='declaration',
                                            children=None,
                                            attributes=[ElementAttribute(name='Name', value='Scout')],
                                            identified_class=None,
                                            is_list=False,
                                        )
                                    ],
                                    attributes=None,
                                    identified_class=None,
                                    is_list=False,
                                ),
                            ],
                            attributes=[ElementAttribute(name='Name', value='Whiskers')],
                            identified_class=None,
                            is_list=False,
                        ),
                        TypedXmlElement(
                            element_name='ppl',
                            identified_type=0,
                            identified_role='variable',
                            children=[
                                TypedXmlElement(
                                    element_name='john',
                                    identified_type=0,
                                    identified_role='declaration',
                                    children=None,
                                    attributes=[ElementAttribute(name='Name', value='John')],
                                    identified_class=None,
                                    is_list=False,
                                )
                            ],
                            attributes=None,
                            identified_class=None,
                            is_list=True,
                        ),
                        TypedXmlElement(
                            element_name='cars',
                            identified_type=0,
                            identified_role='variable',
                            children=[
                                TypedXmlElement(
                                    element_name='car1',
                                    identified_type=0,
                                    identified_role='declaration',
                                    children=None,
                                    attributes=[ElementAttribute(name='Name', value='Lightning')],
                                    identified_class=None,
                                    is_list=False,
                                ),
                                TypedXmlElement(
                                    element_name='car2',
                                    identified_type=0,
                                    identified_role='declaration',
                                    children=None,
                                    attributes=[ElementAttribute(name='Name', value='Sally')],
                                    identified_class=None,
                                    is_list=False,
                                ),
                            ],
                            attributes=None,
                            identified_class=None,
                            is_list=True,
                        ),
                        TypedXmlElement(
                            element_name='newman',
                            identified_type=0,
                            identified_role='declaration',
                            children=None,
                            attributes=[ElementAttribute(name='Name', value='Joseph')],
                            identified_class=None,
                            is_list=False,
                        ),
                        TypedXmlElement(
                            element_name='paul',
                            identified_type=0,
                            identified_role='declaration',
                            children=[
                                TypedXmlElement(
                                    element_name='Parent',
                                    identified_type=0,
                                    identified_role='attribute',
                                    children=[
                                        TypedXmlElement(
                                            element_name='pauls_father',
                                            identified_type=0,
                                            identified_role='declaration',
                                            children=None,
                                            attributes=[ElementAttribute(name='Name', value='Duke Leto Atreides I')],
                                            identified_class=None,
                                            is_list=False,
                                        )
                                    ],
                                    attributes=None,
                                    identified_class=None,
                                    is_list=False,
                                )
                            ],
                            attributes=[ElementAttribute(name='Name', value='Paul Atreides')],
                            identified_class=None,
                            is_list=False,
                        ),
                    ],
                    attributes=None,
                    identified_class=None,
                    is_list=False,
                ),
                types=[
                    {
                        ClassAttribute(name='Name', attribute_type='string'),
                        ClassAttribute(name='Parent', attribute_type='0'),
                        ClassAttribute(name='BestFriend', attribute_type='0'),
                    }
                ],
            ),
            IntermediateCode(
                types=[
                    Class(
                        name='Class1',
                        attributes=[
                            ClassAttribute(name='Name', attribute_type='string'),
                            ClassAttribute(name='Parent', attribute_type='Class1'),
                            ClassAttribute(name='BestFriend', attribute_type='Class1'),
                        ],
                    )
                ],
                declarations=[
                    Declaration(
                        id='0',
                        instance_name='cat',
                        class_name='Class1',
                        attributes=[InstanceAttribute(name='Name', value='The Garfield', ref=None, is_list=False)],
                        is_list=False,
                    ),
                    Declaration(
                        id='1',
                        instance_name='scout',
                        class_name='Class1',
                        attributes=[InstanceAttribute(name='Name', value='Scout', ref=None, is_list=False)],
                        is_list=False,
                    ),
                    Declaration(
                        id='2',
                        instance_name='kitten',
                        class_name='Class1',
                        attributes=[
                            InstanceAttribute(name='Name', value='Whiskers', ref=None, is_list=False),
                            InstanceAttribute(name='Parent', value=None, ref='0', is_list=False),
                            InstanceAttribute(name='BestFriend', value=None, ref='1', is_list=False),
                        ],
                        is_list=False,
                    ),
                    Declaration(
                        id='3',
                        instance_name='john',
                        class_name='Class1',
                        attributes=[InstanceAttribute(name='Name', value='John', ref=None, is_list=False)],
                        is_list=False,
                    ),
                    Declaration(
                        id='4',
                        instance_name='ppl',
                        class_name='Class1',
                        attributes=[InstanceAttribute(name='john', value=None, ref='3', is_list=False)],
                        is_list=True,
                    ),
                    Declaration(
                        id='5',
                        instance_name='car1',
                        class_name='Class1',
                        attributes=[InstanceAttribute(name='Name', value='Lightning', ref=None, is_list=False)],
                        is_list=False,
                    ),
                    Declaration(
                        id='6',
                        instance_name='car2',
                        class_name='Class1',
                        attributes=[InstanceAttribute(name='Name', value='Sally', ref=None, is_list=False)],
                        is_list=False,
                    ),
                    Declaration(
                        id='7',
                        instance_name='cars',
                        class_name='Class1',
                        attributes=[
                            InstanceAttribute(name='car1', value=None, ref='5', is_list=False),
                            InstanceAttribute(name='car2', value=None, ref='6', is_list=False),
                        ],
                        is_list=True,
                    ),
                    Declaration(
                        id='8',
                        instance_name='newman',
                        class_name='Class1',
                        attributes=[InstanceAttribute(name='Name', value='Joseph', ref=None, is_list=False)],
                        is_list=False,
                    ),
                    Declaration(
                        id='9',
                        instance_name='pauls_father',
                        class_name='Class1',
                        attributes=[
                            InstanceAttribute(name='Name', value='Duke Leto Atreides I', ref=None, is_list=False)
                        ],
                        is_list=False,
                    ),
                    Declaration(
                        id='10',
                        instance_name='paul',
                        class_name='Class1',
                        attributes=[
                            InstanceAttribute(name='Name', value='Paul Atreides', ref=None, is_list=False),
                            InstanceAttribute(name='Parent', value=None, ref='9', is_list=False),
                        ],
                        is_list=False,
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
