import pytest
from compiler.code_gen import code_gen
from compiler.models import (
    TypedTree,
    Class,
    ClassAttribute,
    Declaration,
    ElementAttribute,
)


@pytest.fixture
def typed_tree_class1():
    return TypedTree(
        types=[
            Class(
                name='Class1',
                attributes=[
                    ClassAttribute(name='Name', attribute_type='string'),
                    ClassAttribute(name='Parent', attribute_type='Class1'),
                ],
            )
        ],
        declarations=[
            Declaration(
                id='0001',
                instance_name='cat',
                class_name='Class1',
                attributes=[
                    ElementAttribute(name='Name', value='Whiskers'),
                    ElementAttribute(name='Parent', value=None),
                ],
            ),
        ],
    )


@pytest.fixture
def typed_tree_class2():
    return TypedTree(
        types=[
            Class(
                name='Class2',
                attributes=[
                    ClassAttribute(name='Name', attribute_type='string'),
                    ClassAttribute(name='Companion', attribute_type='Class1'),
                ],
            ),
        ],
        declarations=[
            Declaration(
                id='0001',
                instance_name='owner',
                class_name='Class2',
                attributes=[
                    ElementAttribute(name='Name', value='John'),
                    ElementAttribute(name='Companion', value=None),
                ],
            ),
        ],
    )


@pytest.fixture
def expected_code_class1():
    return {
        'Class1.cs': """public class Class1
{
    public string Name { get; set; }
    public Class1 Parent { get; set; }
}
""",
    }


@pytest.fixture
def expected_main_for_class1_typed_tree():
    return {'Main.cs': """Class1 cat = new Class1("Whiskers", null);"""}


@pytest.fixture
def expected_code_class2():
    return {
        'Class2.cs': """public class Class2
{
    public string Name { get; set; }
    public Class1 Companion { get; set; }
}
""",
    }


@pytest.fixture
def expected_main_for_class2_typed_tree():
    return {'Main.cs': """Class2 cat = new Class2("John", null);"""}


def test_code_gen_class1(typed_tree_class1, expected_code_class1, expected_main_for_class1_typed_tree):
    expected = expected_main_for_class1_typed_tree | expected_code_class1
    result = code_gen(typed_tree_class1)
    assert result == expected


def test_code_gen_class2(typed_tree_class2, expected_code_class2, expected_main_for_class2_typed_tree):
    expected = expected_main_for_class2_typed_tree | expected_code_class2
    result = code_gen(typed_tree_class2)
    assert result == expected
