from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Iterable
from compiler.errors import (
    InvalidTransitionError,
    UnexpectedSlashError,
    UnexpectedNumericError,
    QuoteFollowedByNonWhitespaceError,
)
from compiler.models import BaseToken, Symbol, Text, String


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


def build_token(state: State) -> BaseToken:
    if state.state_name == StateName.TEXT_INPUT:
        return Text(state.accumulated)
    if state.state_name == StateName.SYMBOL_INPUT:
        return Symbol(state.accumulated)
    if state.state_name == StateName.STRING_END:
        return String(state.accumulated)
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

    def __call__(self, state: State, char: str) -> tuple[State, BaseToken | None]:
        handler = self.state_handlers.get(state.state_name)
        if handler is None:
            raise InvalidTransitionError(f'No handler for state: {state.state_name}')
        return handler(state, char)

    def handle_start_state(self, state: State, char: str) -> tuple[State, BaseToken | None]:
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

    def handle_text_input(self, state: State, char: str) -> tuple[State, BaseToken | None]:
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
            new_state = State(StateName.TEXT_INPUT, state.accumulated + char)
            return new_state, None
        raise InvalidTransitionError(f"Invalid character '{char}' in TEXT_INPUT.")

    def handle_symbol_input(self, state: State, char: str) -> tuple[State, BaseToken | None]:
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

    def handle_string_input(self, state: State, char: str) -> tuple[State, BaseToken | None]:
        if char == '"':
            new_state = State(StateName.STRING_END, state.accumulated)
            return new_state, None
        if char == '\0':
            raise InvalidTransitionError('EOF encountered in STRING_INPUT.')
        if char == '\n':
            raise InvalidTransitionError('Newline encountered in STRING_INPUT.')
        new_state = State(StateName.STRING_INPUT, state.accumulated + char)
        return new_state, None

    def handle_string_end(self, state: State, char: str) -> tuple[State, BaseToken | None]:
        if char.isspace():
            token = build_token(state)
            return State(StateName.START_STATE), token
        if char in self.symbols_first1:
            token = build_token(state)
            return State(StateName.SYMBOL_INPUT, char), token
        raise QuoteFollowedByNonWhitespaceError('Quote followed by non-whitespace character in STRING_END.')


def scanner(chars: Iterable[str]) -> Iterable[BaseToken]:
    """
    Converts a stream of characters into tokens using a state machine.

    Args:
        chars (Iterable[str]): An iterable stream of INDIVIDUAL characters.

    Yields:
        Token: The next token in the stream.
    """
    symbols = {'<', '</', '>', '/>', '='}
    state_machine = StateTransition(symbols)
    state = State(StateName.START_STATE)

    for char in chars:
        state, token = state_machine(state, char)
        if token:
            yield token

    # Handle EOF by making a final transition
    state, token = state_machine(state, '\0')  # Use a null character to represent EOF
    if token:
        yield token
