from typing import Iterable
from compiler.models import Token, Symbol, Text, String


def scanner(chars: Iterable[str]) -> Iterable[Token]:
    """
    Converts a stream of characters into tokens.

    Args:
        chars (Iterable[str]): An iterable stream of INDIVIDUAL characters.

    Yields:
        Token: The next token in the stream.
    """
    buffer = ''
    in_string = False
    string_char = ''

    symbols = {'<', '>', '/', '=', '/>'}

    char_iter = iter(chars)
    char_buffer = []

    while True:
        if char_buffer:
            char = char_buffer.pop()
        else:
            try:
                char = next(char_iter)
            except StopIteration:
                break
        if in_string:
            if char == string_char:
                yield String(buffer)
                buffer = ''
                in_string = False
            else:
                buffer += char
        else:
            if char in ('"', "'"):
                in_string = True
                string_char = char
            elif char.isspace():
                if buffer:
                    yield Text(buffer)
                    buffer = ''
            elif char in symbols:
                if buffer:
                    yield Text(buffer)
                    buffer = ''
                if char == '<':
                    try:
                        next_char = next(char_iter)
                        if next_char == '/':
                            yield Symbol('</')
                        else:
                            yield Symbol('<')
                            if next_char:
                                char_buffer.append(next_char)
                    except StopIteration:
                        yield Symbol('<')
                elif char == '/':
                    try:
                        next_char = next(char_iter)
                        if next_char == '>':
                            yield Symbol('/>')
                        else:
                            yield Symbol('/')
                            if next_char:
                                char_buffer.append(next_char)
                    except StopIteration:
                        yield Symbol('/')
                else:
                    yield Symbol(char)
            else:
                buffer += char

    if buffer:
        yield Text(buffer)
