import pytest

from compiler.models import Symbol, Text, String, StartToken, EndToken, SelfClosingToken, ElementAttribute, XmlElement
from compiler.parser import build_xml_tokens, parser
from compiler.errors import InvalidTransitionError


@pytest.mark.parametrize(
    'base_tokens, expected_xml_tokens',
    [
        (
            [
                Symbol('<'),
                Text('cat'),
                Text('Name'),
                Symbol('='),
                String('Whiskers'),
                Symbol('/>'),
            ],
            [
                SelfClosingToken('cat', [ElementAttribute('Name', 'Whiskers')]),
            ],
        ),
        (
            [
                Symbol('<'),
                Text('root'),
                Symbol('>'),
                Symbol('<'),
                Text('cat'),
                Text('Name'),
                Symbol('='),
                String('Whiskers'),
                Symbol('/>'),
                Symbol('</'),
                Text('root'),
                Symbol('>'),
            ],
            [
                StartToken('root'),
                SelfClosingToken('cat', [ElementAttribute('Name', 'Whiskers')]),
                EndToken('root'),
            ],
        ),
        (
            [
                Symbol('<'),
                Text('root'),
                Symbol('>'),
                Symbol('<'),
                Text('kitten'),
                Text('Name'),
                Symbol('='),
                String('Whiskers'),
                Symbol('>'),
                Symbol('<'),
                Text('parent'),
                Symbol('>'),
                Symbol('<'),
                Text('cat'),
                Text('Name'),
                Symbol('='),
                String('The Garfield'),
                Symbol('/>'),
                Symbol('</'),
                Text('parent'),
                Symbol('>'),
                Symbol('</'),
                Text('kitten'),
                Symbol('>'),
                Symbol('</'),
                Text('root'),
                Symbol('>'),
            ],
            [
                StartToken('root'),
                StartToken('kitten', [ElementAttribute('Name', 'Whiskers')]),
                StartToken('parent'),
                SelfClosingToken('cat', [ElementAttribute('Name', 'The Garfield')]),
                EndToken('parent'),
                EndToken('kitten'),
                EndToken('root'),
            ],
        ),
    ],
)
def test_parser(base_tokens, expected_xml_tokens):
    tokens = list(build_xml_tokens(base_tokens))
    assert tokens == expected_xml_tokens


@pytest.fixture
def create_element():
    def _create_element(element_name, attributes=None, children=None):
        return XmlElement(element_name=element_name, attributes=attributes or [], children=children or [])

    return _create_element


@pytest.mark.parametrize(
    'tokens, expected',
    [
        # 1. Example from README.md
        (
            [
                StartToken(name='root', attributes=[]),
                StartToken(name='kitten', attributes=[ElementAttribute(name='Name', value='Whiskers')]),
                StartToken(name='parent', attributes=[]),
                SelfClosingToken(name='cat', attributes=[ElementAttribute(name='Name', value='The Garfield')]),
                EndToken(name='parent'),
                EndToken(name='kitten'),
                EndToken(name='root'),
            ],
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
        ),
        # 2. Self-Closing Root Element
        (
            [
                SelfClosingToken(name='root', attributes=[]),
            ],
            XmlElement(element_name='root', attributes=[], children=None),
        ),
        # 3. Nested Elements with Multiple Attributes
        (
            [
                StartToken(name='library', attributes=[]),
                StartToken(
                    name='book',
                    attributes=[
                        ElementAttribute(name='title', value='1984'),
                        ElementAttribute(name='author', value='George Orwell'),
                    ],
                ),
                SelfClosingToken(name='chapter', attributes=[ElementAttribute(name='title', value='Chapter 1')]),
                SelfClosingToken(name='chapter', attributes=[ElementAttribute(name='title', value='Chapter 2')]),
                EndToken(name='book'),
                EndToken(name='library'),
            ],
            XmlElement(
                element_name='library',
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
                                element_name='chapter',
                                attributes=[ElementAttribute(name='title', value='Chapter 1')],
                                children=None,
                            ),
                            XmlElement(
                                element_name='chapter',
                                attributes=[ElementAttribute(name='title', value='Chapter 2')],
                                children=None,
                            ),
                        ],
                    )
                ],
            ),
        ),
        # 4. Abstract Example: works on subset of HTML too!
        (
            [
                StartToken(name='html'),
                StartToken(name='body'),
                SelfClosingToken(name='img', attributes=[ElementAttribute(name='src', value='image.png')]),
                EndToken(name='body'),
                EndToken(name='html'),
            ],
            XmlElement(
                element_name='html',
                children=[
                    XmlElement(
                        element_name='body',
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
        ),
    ],
)
def test_semantic_analyser_success(tokens, expected):
    """
    Test the semantic_analyser with valid token sequences.
    """
    typed_tree = parser(tokens)
    assert typed_tree == expected


@pytest.mark.parametrize(
    'tokens, expected_exception, exception_message',
    [
        # 1. Mismatched Tokens: Closing tag does not match opening tag
        (
            [
                StartToken(name='root', attributes=[]),
                StartToken(name='child', attributes=[]),
                EndToken(name='root'),  # Mismatch: should be EndToken(name="child")
            ],
            InvalidTransitionError,
            'Mismatching tokens: child and root',
        ),
        # 2. Mismatched Tokens: Extra closing tag
        (
            [
                StartToken(name='root', attributes=[]),
                EndToken(name='child'),  # Mismatch: no opening 'child' tag
            ],
            InvalidTransitionError,
            'Mismatching tokens: root and child',
        ),
        # 3. Unclosed Start Tokens: Missing EndToken for 'child'
        (
            [
                StartToken(name='root', attributes=[]),
                StartToken(name='child', attributes=[]),
                EndToken(name='root'),
                # Missing EndToken for 'child'
            ],
            InvalidTransitionError,
            'Mismatching tokens: child and root',
        ),
        # 4. Unclosed Start Tokens: No closing tags
        (
            [
                StartToken(name='root', attributes=[]),
                StartToken(name='child', attributes=[]),
                # Missing EndTokens
            ],
            InvalidTransitionError,
            'Unmatched start tokens remain',
        ),
    ],
)
def test_semantic_analyser_failure(tokens, expected_exception, exception_message):
    """
    Test the semantic_analyser with invalid token sequences expecting failures.
    """
    with pytest.raises(expected_exception) as exc_info:
        parser(tokens)
    assert str(exc_info.value) == exception_message
