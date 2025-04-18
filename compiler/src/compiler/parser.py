from typing import Iterable, Iterator, List
from compiler.models import Token, Symbol, Text, String, Element, ElementAttribute


def parser(tokens: Iterable[Token]) -> Element:
    """
    Parses a stream of tokens into an Abstract Syntax Tree (AST).

    Args:
        tokens (Iterable[Token]): An iterable stream of tokens.

    Returns:
        Element: The root of the AST.
    """
    parser_instance = Parser(iter(tokens))
    return parser_instance.parse()


class Parser:
    def __init__(self, tokens: Iterator[Token]):
        self.tokens = tokens
        self.current_token = next(self.tokens, None)

    def consume(self):
        """Advance to the next token."""
        self.current_token = next(self.tokens, None)

    def expect(self, token_type, value=None):
        """Ensure the current token matches the expectation."""
        if not isinstance(self.current_token, token_type):
            raise SyntaxError(f'Expected token type {token_type}, got {type(self.current_token)}')
        if value and self.current_token.value != value:
            raise SyntaxError(f"Expected token value '{value}', got '{self.current_token.value}'")
        self.consume()

    def parse(self) -> Element:
        """Parse the token stream and return the root Element."""
        element = self.parse_element()
        if self.current_token is not None:
            raise SyntaxError('Extra tokens after parsing complete')
        return element

    def parse_element(self) -> Element:
        """Parse a single XML element."""
        # Expecting the start of an element
        self.expect(Symbol, '<')

        if isinstance(self.current_token, Text):
            element_name = self.current_token.value
            self.consume()
        else:
            raise SyntaxError("Expected element name after '<'")

        attributes = self.parse_attributes()

        # Check for self-closing tag
        if isinstance(self.current_token, Symbol) and self.current_token.value == '/>':
            self.consume()
            return Element(element_name=element_name, attributes=attributes, children=[])

        # Expecting closing '>'
        self.expect(Symbol, '>')

        # Parse child elements
        children = self.parse_children(element_name)

        return Element(element_name=element_name, attributes=attributes, children=children)

    def parse_attributes(self) -> List[ElementAttribute]:
        """Parse attributes within an element."""
        attributes = []
        while isinstance(self.current_token, Text):
            attr_name = self.current_token.value
            self.consume()
            self.expect(Symbol, '=')
            if isinstance(self.current_token, String):
                attr_value = self.current_token.value
                self.consume()
            else:
                raise SyntaxError('Expected string value for attribute')
            attributes.append(ElementAttribute(name=attr_name, value=attr_value))
        return attributes

    def parse_children(self, parent_name: str) -> List[Element]:
        """Parse all child elements of the current element."""
        children = []
        while True:
            if isinstance(self.current_token, Symbol) and self.current_token.value.startswith('</'):
                break  # Start of a closing tag
            elif isinstance(self.current_token, Symbol) and self.current_token.value == '<':
                # Parse a child element
                child = self.parse_element()
                children.append(child)
            elif self.current_token is None:
                raise SyntaxError(f"Expected closing tag for '{parent_name}'")
            else:
                raise SyntaxError(f"Unexpected token {self.current_token} inside '{parent_name}'")
        # Handle closing tag
        self.consume()  # Consume Symbol("</")
        self.expect(Text, parent_name)
        self.expect(Symbol, '>')
        return children
