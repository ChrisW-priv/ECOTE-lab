import pytest
from compiler.code_gen import code_gen, generate_class_code
from compiler.models import (
    TypedTree,
    Class,
    ClassAttribute,
    Declaration,
    InstanceAttribute,
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
                    InstanceAttribute(name='Name', value='Whiskers'),
                    InstanceAttribute(name='Parent', value=None),
                ],
            ),
        ],
    )


@pytest.fixture
def expected_code_class1():
    return {
        'Class1.cs': generate_class_code(
            'Class1',
            [
                ClassAttribute(name='Name', attribute_type='string'),
                ClassAttribute(name='Parent', attribute_type='Class1'),
            ],
        )
    }


@pytest.fixture
def expected_main_for_class1_typed_tree():
    return {'Main.cs': """Class1 cat = new Class1("Whiskers", null);"""}


def test_code_gen_class1(typed_tree_class1, expected_code_class1, expected_main_for_class1_typed_tree):
    expected = expected_main_for_class1_typed_tree | expected_code_class1
    result = code_gen(typed_tree_class1)
    assert result == expected


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
                    InstanceAttribute(name='Name', value='John'),
                    InstanceAttribute(name='Companion', value=None),
                ],
            ),
        ],
    )


@pytest.fixture
def expected_code_class2():
    return {
        'Class2.cs': generate_class_code(
            'Class2',
            [
                ClassAttribute(name='Name', attribute_type='string'),
                ClassAttribute(name='Companion', attribute_type='Class1'),
            ],
        )
    }


@pytest.fixture
def expected_main_for_class2_typed_tree():
    return {'Main.cs': """Class2 owner = new Class2("John", null);"""}


def test_code_gen_class2(typed_tree_class2, expected_code_class2, expected_main_for_class2_typed_tree):
    expected = expected_main_for_class2_typed_tree | expected_code_class2
    result = code_gen(typed_tree_class2)
    assert result == expected


@pytest.fixture
def typed_tree_class3():
    return TypedTree(
        types=[
            Class(
                name='Class1',
                attributes=[
                    ClassAttribute(name='Name', attribute_type='string'),
                ],
            ),
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
                instance_name='companion',
                class_name='Class1',
                attributes=[
                    InstanceAttribute(name='Name', value='Whiskers'),
                ],
            ),
            Declaration(
                id='0002',
                instance_name='owner',
                class_name='Class2',
                attributes=[
                    InstanceAttribute(name='Name', value='Fluffy'),
                    InstanceAttribute(name='Companion', value=None, ref='0001'),
                ],
            ),
        ],
    )


@pytest.fixture
def expected_code_class3_class1():
    return {'Class1.cs': generate_class_code('Class1', [ClassAttribute(name='Name', attribute_type='string')])}


@pytest.fixture
def expected_code_class3_class2():
    return {
        'Class2.cs': generate_class_code(
            'Class2',
            [
                ClassAttribute(name='Name', attribute_type='string'),
                ClassAttribute(name='Companion', attribute_type='Class1'),
            ],
        )
    }


@pytest.fixture
def expected_main_for_class3_typed_tree():
    return {
        'Main.cs': """Class1 companion = new Class1("Whiskers");
Class2 owner = new Class2("Fluffy", companion);"""
    }


def test_code_gen_class3(
    typed_tree_class3, expected_code_class3_class1, expected_code_class3_class2, expected_main_for_class3_typed_tree
):
    expected = expected_code_class3_class1 | expected_code_class3_class2 | expected_main_for_class3_typed_tree
    result = code_gen(typed_tree_class3)
    assert result == expected
