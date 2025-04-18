from dataclasses import dataclass, replace
from enum import StrEnum, auto
from typing import Iterable
from compiler.errors import InvalidTransitionError
from compiler.models import (
    XmlToken,
    BaseToken,
    StartToken,
    EndToken,
    SelfClosingToken,
    ElementAttribute,
    Symbol,
    Text,
    String,
)


class StateName(StrEnum):
    START_STATE = auto()
    IN_DOCUMENT = auto()
    ELEMENT_START = auto()
    ELEMENT_ATTR_SET = auto()
    ATTRIBUTE_SET = auto()
    ATTRIBUTE_SET_VALUE = auto()
    ELEMENT_END = auto()
    ELEMENT_END_VERIFY = auto()


@dataclass
class State:
    state_name: StateName
    accumulated: XmlToken | None = None


class StateTransition:
    def __init__(self):
        # Mapping from StateName to handler methods
        self.state_handlers = {
            StateName.START_STATE: self.handle_start_state,
            StateName.IN_DOCUMENT: self.handle_in_document,
            StateName.ELEMENT_START: self.handle_element_start,
            StateName.ELEMENT_ATTR_SET: self.handle_element_attr_set,
            StateName.ATTRIBUTE_SET: self.handle_attribute_set,
            StateName.ATTRIBUTE_SET_VALUE: self.handle_attribute_set_value,
            StateName.ELEMENT_END: self.handle_element_end,
            StateName.ELEMENT_END_VERIFY: self.handle_element_end_verify,
        }

    def handle_start_state(self, state: State, token: BaseToken) -> tuple[State, XmlToken | None]:
        if isinstance(token, Symbol) and token.value == '<':
            start_token = StartToken(name='', attributes=None)
            return State(StateName.ELEMENT_START, start_token), None
        raise InvalidTransitionError('XML must start with a root element.')

    def handle_in_document(self, state: State, token: BaseToken) -> tuple[State, XmlToken | None]:
        if isinstance(token, Symbol) and token.value == '<':
            start_token = StartToken(name='', attributes=[])
            return State(StateName.ELEMENT_START, start_token), None
        if isinstance(token, Symbol) and token.value == '</':
            return State(StateName.ELEMENT_END, None), None
        raise InvalidTransitionError('Unexpected token in document.')

    def handle_element_start(self, state: State, token: BaseToken) -> tuple[State, XmlToken | None]:
        if isinstance(token, Text):
            new_accumulated = replace(state.accumulated, name=token.value)
            return State(StateName.ELEMENT_ATTR_SET, new_accumulated), None
        raise InvalidTransitionError('Element must have a name.')

    def handle_element_attr_set(self, state: State, token: BaseToken) -> tuple[State, XmlToken | None]:
        if isinstance(token, Text):
            new_attr = ElementAttribute(name=token.value, value='')
            new_attributes = (state.accumulated.attributes or []) + [new_attr]
            new_accumulated = replace(state.accumulated, attributes=new_attributes if new_attributes else None)
            return State(StateName.ATTRIBUTE_SET, new_accumulated), None
        if isinstance(token, Symbol) and token.value == '/>':
            closing_token = SelfClosingToken(
                name=state.accumulated.name,
                attributes=None if not state.accumulated.attributes else state.accumulated.attributes,
            )
            return State(StateName.IN_DOCUMENT, None), closing_token
        if isinstance(token, Symbol) and token.value == '>':
            start_token = StartToken(
                name=state.accumulated.name,
                attributes=None if not state.accumulated.attributes else state.accumulated.attributes,
            )
            return State(StateName.IN_DOCUMENT, start_token), start_token
        raise InvalidTransitionError('Invalid attribute set.')

    def handle_attribute_set(self, state: State, token: BaseToken) -> tuple[State, XmlToken | None]:
        if isinstance(token, Symbol) and token.value == '=':
            return State(StateName.ATTRIBUTE_SET_VALUE, state.accumulated), None
        raise InvalidTransitionError('Expected "=" after attribute name.')

    def handle_attribute_set_value(self, state: State, token: BaseToken) -> tuple[State, XmlToken | None]:
        if isinstance(token, String):
            last_attr = state.accumulated.attributes[-1]
            updated_attr = ElementAttribute(name=last_attr.name, value=token.value)
            new_attributes = state.accumulated.attributes[:-1] + [updated_attr]
            new_accumulated = replace(state.accumulated, attributes=new_attributes)
            return State(StateName.ELEMENT_ATTR_SET, new_accumulated), None
        raise InvalidTransitionError('Expected string value for attribute.')

    def handle_element_end(self, state: State, token: BaseToken) -> tuple[State, XmlToken | None]:
        if isinstance(token, Text):
            # Directly create an EndToken with the name
            end_token = EndToken(name=token.value)
            return State(StateName.ELEMENT_END_VERIFY, end_token), None
        raise InvalidTransitionError('Closing element must have a name.')

    def handle_element_end_verify(self, state: State, token: BaseToken) -> tuple[State, XmlToken | None]:
        if isinstance(token, Symbol) and token.value == '>':
            end_token = state.accumulated  # Already an EndToken with the name set
            return State(StateName.IN_DOCUMENT, end_token), end_token
        raise InvalidTransitionError('Expected ">" to close element.')

    def __call__(self, state: State, token: BaseToken) -> tuple[State, XmlToken | None]:
        handler = self.state_handlers.get(state.state_name)
        if handler is None:
            raise InvalidTransitionError(f'No handler for state: {state.state_name}')
        return handler(state, token)


def parser(tokens: Iterable[BaseToken]) -> Iterable[XmlToken]:
    """
    Parses a stream of tokens into an Abstract Syntax Tree (AST).

    Args:
        tokens (Iterable[BaseToken]): An iterable of tokens.

    Returns:
        Iterable of XmlTokens
    """
    state_machine = StateTransition()
    state = State(StateName.START_STATE)

    for base_token in tokens:
        state, xml_token = state_machine(state, base_token)
        if xml_token:
            yield xml_token
