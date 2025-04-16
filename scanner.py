from typing import Iterable
from models import Token, Symbol


def scanner(chars: Iterable[str]) -> Iterable[Token]:
    """
    Converts a stream of characters into tokens.

    Args:
        chars (Iterable[str]): An iterable stream of INDIVIDUAL characters.

    Yields:
        Token: The next token in the stream.
    """
    # Implementation of the scanner goes here
    for char in chars:
        yield Symbol(char)
