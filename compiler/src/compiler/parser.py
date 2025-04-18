from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Iterable
from compiler.errors import InvalidTransitionError
from compiler.models import XmlToken, BaseToken


class StateName(StrEnum):
    START_STATE = auto()


@dataclass
class State:
    state_name: StateName
    accumulated: XmlToken | None = None


class StateTransition:
    def __init__(self):
        # Mapping from StateName to handler methods
        self.state_handlers = {
            StateName.START_STATE: ...,
        }

    def __call__(self, state: State, token: BaseToken) -> tuple[State, XmlToken | None]:
        handler = self.state_handlers.get(state.state_name)
        if handler is None:
            raise InvalidTransitionError(f'No handler for state: {state.state_name}')
        return handler(state, token)


def parser(tokens: Iterable[BaseToken]) -> Iterable[XmlToken]:
    """
    Parses a stream of tokens into an Abstract Syntax Tree (AST).

    Args:
        tokens (Iterable[Token]): An iterable stream of tokens.

    Returns:
        Element: The root of the AST.
    """
    parser = StateTransition()
    state = State(StateName.START_STATE)

    for base_token in tokens:
        state, xml_token = parser(state, base_token)
        if xml_token:
            yield xml_token
