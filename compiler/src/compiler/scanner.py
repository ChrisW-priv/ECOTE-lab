from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Iterable, Iterator, Optional
from compiler.errors import (
    InvalidTransitionError,
    UnexpectedSlashError,
    UnexpectedNumericError,
    QuoteFollowedByNonWhitespaceError,
)
from compiler.models import Token, Symbol, Text, String


class StateName(StrEnum):
    START_STATE = auto()
    TEXT_INPUT = auto()
    SYMBOL_INPUT = auto()
    STRING_INPUT = auto()
    STRING_END = auto()


@dataclass
class State:
    state_name: StateName
    accumulated: str = ''


def build_token(state: State) -> Token:
    if state.state_name == StateName.TEXT_INPUT:
        return Text(state.accumulated)
    elif state.state_name in {StateName.SYMBOL_INPUT}:
        return Symbol(state.accumulated)
    elif state.state_name == StateName.STRING_END:
        return String(state.accumulated)
    else:
        raise InvalidTransitionError(f'Cannot build token from state: {state.state_name}')


class StateTransition:
    def __init__(self, symbols: set[str]):
        self.symbols = symbols
        self.symbols_first1 = set(symb[0] for symb in symbols)
        self.symbols_flat_unique = set(char for symbol in symbols for char in symbol)

        # Mapping from StateName to handler methods
        self.state_handlers = {
            StateName.START_STATE: self.handle_start_state,
            StateName.TEXT_INPUT: self.handle_text_input,
            StateName.SYMBOL_INPUT: self.handle_symbol_input,
            StateName.STRING_INPUT: self.handle_string_input,
            StateName.STRING_END: self.handle_string_end,
        }

    def __call__(self, state: State, char: str) -> tuple[State, Optional[Token]]:
        handler = self.state_handlers.get(state.state_name)
        if handler is None:
            raise InvalidTransitionError(f'No handler for state: {state.state_name}')
        return handler(state, char)

    def handle_start_state(self, state: State, char: str) -> tuple[State, Optional[Token]]:
        if char.isspace():
            return State(StateName.START_STATE), None  # Remain in START_STATE
        if char.isalpha():
            new_state = State(StateName.TEXT_INPUT, char)
            return new_state, None
        if char in self.symbols_first1:
            return State(StateName.SYMBOL_INPUT, char), None
        if char == '"':
            return State(StateName.STRING_INPUT, char), None
        if char == '\0':
            return State(StateName.START_STATE), None
        if char.isdigit():
            raise UnexpectedNumericError('Numeric character encountered in START_STATE.')
        raise InvalidTransitionError(f"Invalid character '{char}' in START_STATE.")

    def handle_text_input(self, state: State, char: str) -> tuple[State, Optional[Token]]:
        if char.isalpha() or char == '_':
            new_state = State(StateName.TEXT_INPUT, state.accumulated + char)
            return new_state, None
        if char.isspace():
            token = build_token(state)
            return State(StateName.START_STATE), token
        if char in self.symbols_first1:
            token = build_token(state)
            new_state = State(StateName.SYMBOL_INPUT, char)
            return new_state, token
        if char == '/':
            raise UnexpectedSlashError("Unexpected '/' in TEXT_INPUT.")
        if char.isdigit():
            raise UnexpectedNumericError('Numeric character encountered in TEXT_INPUT.')
        raise InvalidTransitionError(f"Invalid character '{char}' in TEXT_INPUT.")

    def handle_symbol_input(self, state: State, char: str) -> tuple[State, Optional[Token]]:
        if char in self.symbols_flat_unique:
            new_accumulated = state.accumulated + char
            if not any(symbol.startswith(new_accumulated) for symbol in self.symbols):
                raise InvalidTransitionError(f"Invalid symbol '{new_accumulated}'.")
            return State(StateName.SYMBOL_INPUT, new_accumulated), None
        if char.isalpha():
            token = build_token(state)
            new_state = State(StateName.TEXT_INPUT, char)
            return new_state, token
        if char == '"':
            token = build_token(state)
            new_state = State(StateName.STRING_INPUT)
            return new_state, token
        if char == '\0':
            token = build_token(state)
            new_state = State(StateName.START_STATE)
            return new_state, token
        if char.isspace():
            token = build_token(state)
            new_state = State(StateName.START_STATE)
            return new_state, token
        raise InvalidTransitionError(f"Invalid character '{char}' in SYMBOL_INPUT.")

    def handle_string_input(self, state: State, char: str) -> tuple[State, Optional[Token]]:
        if char == '"':
            new_state = State(StateName.STRING_END, state.accumulated)
            return new_state, None
        if char == '\0':
            raise InvalidTransitionError('EOF encountered in STRING_INPUT.')
        if char == '\n':
            raise InvalidTransitionError('Newline encountered in STRING_INPUT.')
        new_state = State(StateName.STRING_INPUT, state.accumulated + char)
        return new_state, None

    def handle_string_end(self, state: State, char: str) -> tuple[State, Optional[Token]]:
        if char.isspace():
            token = build_token(state)
            return State(StateName.START_STATE), token
        if char in self.symbols_first1:
            token = build_token(state)
            return State(StateName.SYMBOL_INPUT, char), token
        raise QuoteFollowedByNonWhitespaceError('Quote followed by non-whitespace character in STRING_END.')


def scanner(chars: Iterable[str]) -> Iterator[Token]:
    """
    Converts a stream of characters into tokens using a state machine.

    Args:
        chars (Iterable[str]): An iterable stream of INDIVIDUAL characters.

    Yields:
        Token: The next token in the stream.
    """
    symbols = {'<', '</', '>', '/>', '='}
    transition = StateTransition(symbols)
    state = State(StateName.START_STATE)

    for char in chars:
        state, token = transition(state, char)
        if token:
            yield token

    # Handle EOF by making a final transition
    state, token = transition(state, '\0')  # Use a null character to represent EOF
    if token:
        yield token
