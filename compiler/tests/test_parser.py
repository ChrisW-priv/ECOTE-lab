from compiler.models import Symbol, Text, String, StartToken, EndToken, SelfClosingToken, ElementAttribute
import pytest
from compiler.parser import parser


@pytest.mark.parametrize(
    'base_tokens, expected_xml_tokens',
    [
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
                StartToken('cat', [ElementAttribute('Name', 'The Garfield')]),
                EndToken('parent'),
                EndToken('kitten'),
                EndToken('root'),
            ],
        ),
    ],
)
def test_parser(base_tokens, expected_xml_tokens):
    tokens = list(parser(base_tokens))
    assert tokens == expected_xml_tokens
