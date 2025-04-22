import pytest

from compiler.code_gen import code_gen, generate_class_code, generate_main
from compiler.models import (
    IntermediateCode,
    Class,
    ClassAttribute,
    Declaration,
    InstanceAttribute,
)


class1 = Class('Class1', [ClassAttribute('Name', 'string'), ClassAttribute('Parent', 'Class1')])


@pytest.mark.parametrize(
    'inter_code,expected',
    [
        (
            IntermediateCode(
                types=[class1],
                declarations=[
                    Declaration('0001', 'cat', 'Class1', [InstanceAttribute('Name', 'The Garfield')]),
                    Declaration(
                        '0002',
                        'kitten',
                        'Class1',
                        [InstanceAttribute('Name', 'Whiskers'), InstanceAttribute('Parent', ref='0001')],
                    ),
                ],
            ),
            {
                'Class1.cs': generate_class_code(class1.name, class1.attributes),
                'Main.cs': generate_main(
                    [
                        Declaration('0001', 'cat', 'Class1', [InstanceAttribute('Name', 'The Garfield')]),
                        Declaration(
                            '0002',
                            'kitten',
                            'Class1',
                            [InstanceAttribute('Name', 'Whiskers'), InstanceAttribute('Parent', ref='0001')],
                        ),
                    ],
                    [class1],
                ),
            },
        ),
    ],
)
def test_code_gen_class3(inter_code: IntermediateCode, expected: dict[str, str]):
    result = code_gen(inter_code)
    assert result == expected
