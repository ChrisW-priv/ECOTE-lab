import pytest
from compiler.inter_code_gen import inter_code_gen
from compiler.models import (
    IntermediateCode,
    TypedXmlElement,
    Class,
    Declaration,
    ClassAttribute,
    InstanceAttribute,
)


@pytest.mark.parametrize(
    'input_typed_ast, expected_inter_code',
    [
        # Test Case 1: No Declarations
        (
            TypedXmlElement(
                element_name='root',
                identified_type=-1,
                identified_role='root',
                children=None,
                identified_class=None,
                is_list=False,
            ),
            IntermediateCode(
                types=[],
                declarations=[],
            ),
        ),
        # Test Case 2: Single Declaration, No Dependencies
        (
            TypedXmlElement(
                element_name='root',
                identified_type=-1,
                identified_role='root',
                children=[
                    TypedXmlElement(
                        element_name='animal1',
                        identified_type=0,
                        identified_role='declaration',
                        children=None,
                        identified_class=Class(
                            name='Animal',
                            attributes=[
                                ClassAttribute(name='name', attribute_type='string'),
                                ClassAttribute(name='age', attribute_type='int'),
                            ],
                        ),
                        is_list=False,
                    )
                ],
                identified_class=None,
                is_list=False,
            ),
            IntermediateCode(
                types=[
                    Class(
                        name='Animal',
                        attributes=[
                            ClassAttribute(name='name', attribute_type='string'),
                            ClassAttribute(name='age', attribute_type='int'),
                        ],
                    )
                ],
                declarations=[
                    Declaration(
                        id='animal1',
                        instance_name='animal1',
                        class_name='Animal',
                        attributes=[
                            InstanceAttribute(name='name', value=None, ref=None),
                            InstanceAttribute(name='age', value=None, ref=None),
                        ],
                    )
                ],
            ),
        ),
        # Test Case 3: Multiple Declarations, No Dependencies
        (
            TypedXmlElement(
                element_name='root',
                identified_type=-1,
                identified_role='root',
                children=[
                    TypedXmlElement(
                        element_name='animal1',
                        identified_type=0,
                        identified_role='declaration',
                        children=None,
                        identified_class=Class(
                            name='Animal',
                            attributes=[
                                ClassAttribute(name='name', attribute_type='string'),
                                ClassAttribute(name='age', attribute_type='int'),
                            ],
                        ),
                        is_list=False,
                    ),
                    TypedXmlElement(
                        element_name='animal2',
                        identified_type=0,
                        identified_role='declaration',
                        children=None,
                        identified_class=Class(
                            name='Animal',
                            attributes=[
                                ClassAttribute(name='name', attribute_type='string'),
                                ClassAttribute(name='age', attribute_type='int'),
                            ],
                        ),
                        is_list=False,
                    ),
                ],
                identified_class=None,
                is_list=False,
            ),
            IntermediateCode(
                types=[
                    Class(
                        name='Animal',
                        attributes=[
                            ClassAttribute(name='name', attribute_type='string'),
                            ClassAttribute(name='age', attribute_type='int'),
                        ],
                    )
                ],
                declarations=[
                    Declaration(
                        id='animal1',
                        instance_name='animal1',
                        class_name='Animal',
                        attributes=[
                            InstanceAttribute(name='name', value=None, ref=None),
                            InstanceAttribute(name='age', value=None, ref=None),
                        ],
                    ),
                    Declaration(
                        id='animal2',
                        instance_name='animal2',
                        class_name='Animal',
                        attributes=[
                            InstanceAttribute(name='name', value=None, ref=None),
                            InstanceAttribute(name='age', value=None, ref=None),
                        ],
                    ),
                ],
            ),
        ),
        # Test Case 4: Declarations with Dependencies
        (
            TypedXmlElement(
                element_name='root',
                identified_type=-1,
                identified_role='root',
                children=[
                    TypedXmlElement(
                        element_name='owner1',
                        identified_type=0,
                        identified_role='declaration',
                        children=None,
                        identified_class=Class(
                            name='Owner',
                            attributes=[
                                ClassAttribute(name='name', attribute_type='string'),
                            ],
                        ),
                        is_list=False,
                    ),
                    TypedXmlElement(
                        element_name='pet1',
                        identified_type=0,
                        identified_role='declaration',
                        children=None,
                        identified_class=Class(
                            name='Pet',
                            attributes=[
                                ClassAttribute(name='name', attribute_type='string'),
                                ClassAttribute(name='owner', attribute_type='Owner'),
                            ],
                        ),
                        is_list=False,
                    ),
                ],
                identified_class=None,
                is_list=False,
            ),
            IntermediateCode(
                types=[
                    Class(
                        name='Owner',
                        attributes=[
                            ClassAttribute(name='name', attribute_type='string'),
                        ],
                    ),
                    Class(
                        name='Pet',
                        attributes=[
                            ClassAttribute(name='name', attribute_type='string'),
                            ClassAttribute(name='owner', attribute_type='Owner'),
                        ],
                    ),
                ],
                declarations=[
                    Declaration(
                        id='owner1',
                        instance_name='owner1',
                        class_name='Owner',
                        attributes=[
                            InstanceAttribute(name='name', value=None, ref=None),
                        ],
                    ),
                    Declaration(
                        id='pet1',
                        instance_name='pet1',
                        class_name='Pet',
                        attributes=[
                            InstanceAttribute(name='name', value=None, ref=None),
                            InstanceAttribute(name='owner', value=None, ref=None),  # Assuming no refs
                        ],
                    ),
                ],
            ),
        ),
        # Test Case 5: Declarations with Dependencies (Refs)
        (
            TypedXmlElement(
                element_name='root',
                identified_type=-1,
                identified_role='root',
                children=[
                    TypedXmlElement(
                        element_name='owner1',
                        identified_type=0,
                        identified_role='declaration',
                        children=None,
                        identified_class=Class(
                            name='Owner',
                            attributes=[
                                ClassAttribute(name='name', attribute_type='string'),
                            ],
                        ),
                        is_list=False,
                    ),
                    TypedXmlElement(
                        element_name='pet1',
                        identified_type=0,
                        identified_role='declaration',
                        children=None,
                        identified_class=Class(
                            name='Pet',
                            attributes=[
                                ClassAttribute(name='name', attribute_type='string'),
                                ClassAttribute(name='owner', attribute_type='Owner'),
                            ],
                        ),
                        is_list=False,
                    ),
                ],
                identified_class=None,
                is_list=False,
            ),
            IntermediateCode(
                types=[
                    Class(
                        name='Owner',
                        attributes=[
                            ClassAttribute(name='name', attribute_type='string'),
                        ],
                    ),
                    Class(
                        name='Pet',
                        attributes=[
                            ClassAttribute(name='name', attribute_type='string'),
                            ClassAttribute(name='owner', attribute_type='Owner'),
                        ],
                    ),
                ],
                declarations=[
                    Declaration(
                        id='owner1',
                        instance_name='owner1',
                        class_name='Owner',
                        attributes=[
                            InstanceAttribute(name='name', value=None, ref=None),
                        ],
                    ),
                    Declaration(
                        id='pet1',
                        instance_name='pet1',
                        class_name='Pet',
                        attributes=[
                            InstanceAttribute(name='name', value=None, ref=None),
                            InstanceAttribute(name='owner', value=None, ref=None),
                        ],
                    ),
                ],
            ),
        ),
    ],
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
