import pytest

from compiler.code_gen import code_gen
from compiler.models import (
    IntermediateCode,
    Class,
    ClassAttribute,
    Declaration,
    InstanceAttribute,
)


@pytest.mark.parametrize(
    'inter_code, expected',
    [
        (
            IntermediateCode(
                types=[
                    Class(
                        name='Class1',
                        attributes=[
                            ClassAttribute(name='Parent', attribute_type='Class1'),
                            ClassAttribute(name='Name', attribute_type='string'),
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
            {
                'Class1.cs': (
                    'using System;\n\npublic class Class1\n{\n'
                    '    public Class1 Parent { get; set; }\n'
                    '    public string Name { get; set; }\n'
                    '    public Class1 Bestfriend { get; set; }\n\n'
                    '    public Class1(Class1 parent, string name, Class1 bestfriend)\n'
                    '    {\n'
                    '        Parent = parent;\n'
                    '        Name = name;\n'
                    '        Bestfriend = bestfriend;\n'
                    '    }\n\n'
                    '    public override bool Equals(object obj)\n'
                    '    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n\n'
                    '    protected override void Finalize()\n'
                    '    {\n'
                    '        // Finalize resources if necessary\n'
                    '    }\n\n'
                    '    public override int GetHashCode()\n'
                    '    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n\n'
                    '    protected object MemberwiseClone()\n'
                    '    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n\n'
                    '    public override string ToString()\n'
                    '    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n'
                    '}'
                ),
                'Main.cs': (
                    'Class1 cat = new Class1("The Garfield");\n'
                    'Class1 scout = new Class1("Scout");\n'
                    'Class1 kitten = new Class1(cat, "Whiskers", scout);\n'
                    'Class1 john = new Class1("John");\n'
                    'List<Class1> ppl = new List<Class1>();\n'
                    'ppl.add(john);\n'
                    'Class1 car1 = new Class1("Lightning");\n'
                    'Class1 car2 = new Class1("Sally");\n'
                    'List<Class1> cars = new List<Class1>();\n'
                    'cars.add(car1);\n'
                    'cars.add(car2);\n'
                    'Class1 newman = new Class1("Joseph");\n'
                    'Class1 pauls_father = new Class1("Duke Leto Atreides I");\n'
                    'Class1 paul = new Class1(pauls_father, "Paul Atreides");'
                ),
            },
        ),
        (
            IntermediateCode(
                types=[
                    Class(
                        name='Class1',
                        attributes=[
                            ClassAttribute(name='Name', attribute_type='string'),
                            ClassAttribute(name='parent', attribute_type='Class2'),
                        ],
                    ),
                    Class(
                        name='Class2',
                        attributes=[
                            ClassAttribute(name='kind', attribute_type='string'),
                        ],
                    ),
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
            {
                'Class1.cs': (
                    'using System;\n\npublic class Class1\n{\n'
                    '    public string Name { get; set; }\n'
                    '    public Class2 Parent { get; set; }\n\n'
                    '    public Class1(string name, Class2 parent)\n    {\n'
                    '        Name = name;\n'
                    '        Parent = parent;\n'
                    '    }\n\n'
                    '    public override bool Equals(object obj)\n    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n\n'
                    '    protected override void Finalize()\n    {\n'
                    '        // Finalize resources if necessary\n'
                    '    }\n\n'
                    '    public override int GetHashCode()\n    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n\n'
                    '    protected object MemberwiseClone()\n    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n\n'
                    '    public override string ToString()\n    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n'
                    '}'
                ),
                'Class2.cs': (
                    'using System;\n\npublic class Class2\n{\n'
                    '    public string Kind { get; set; }\n\n'
                    '    public Class2(string kind)\n    {\n'
                    '        Kind = kind;\n'
                    '    }\n\n'
                    '    public override bool Equals(object obj)\n    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n\n'
                    '    protected override void Finalize()\n    {\n'
                    '        // Finalize resources if necessary\n'
                    '    }\n\n'
                    '    public override int GetHashCode()\n    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n\n'
                    '    protected object MemberwiseClone()\n    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n\n'
                    '    public override string ToString()\n    {\n'
                    '        throw new NotImplementedException();\n'
                    '    }\n'
                    '}'
                ),
                'Main.cs': (
                    'Class2 flower = new Class2("Iris");\n'
                    'Class1 cat = new Class1("The Garfield");\n'
                    'Class1 kitten = new Class1("Whiskers", cat);'
                ),
            },
        ),
    ],
)
def test_code_gen_class3(inter_code: IntermediateCode, expected: dict[str, str]):
    result = code_gen(inter_code)
    assert result == expected
