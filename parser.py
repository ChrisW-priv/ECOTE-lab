from typing import Iterable
from models import Token, Element


def parser(tokens: Iterable[Token]) -> Element:
    """
    Parses a stream of tokens into an Abstract Syntax Tree (AST).

    Args:
        tokens (Iterable[Token]): An iterable stream of tokens.

    Returns:
        Element: The root of the AST.
    """
    # Implementation of the parser goes here
    return Element("root", [], [])
