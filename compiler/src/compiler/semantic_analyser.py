from compiler.models import XmlElement, StartToken, EndToken, SelfClosingToken, XmlToken
from compiler.errors import InvalidTransitionError


def semantic_analyser(tokens: list[XmlToken]) -> XmlElement:
    """
    Analyzes the list of XmlTokens to enforce semantic rules and builds a TypedTree.

    Args:
        tokens (list[XmlToken]): The list of XML tokens.

    Returns:
        TypedTree: The semantically analyzed AST.
    """
    stack = []
    inter_list = []

    for token in tokens:
        if isinstance(token, StartToken):
            stack.append(token)
        elif isinstance(token, SelfClosingToken):
            element = XmlElement(element_name=token.name, attributes=token.attributes)
            inter_list.append(element)
        elif isinstance(token, EndToken):
            if not stack:
                raise InvalidTransitionError(f'Mismatching token end, never opened: {token.name}')
            if stack and stack[-1].name != token.name:
                raise InvalidTransitionError(f'Mismatching tokens: {stack[-1].name} and {token.name}')
            start_token = stack.pop()
            children = inter_list if inter_list else None
            element = XmlElement(element_name=start_token.name, attributes=start_token.attributes, children=children)
            inter_list = [element]
        else:
            raise InvalidTransitionError('Unexpected token type')

    if stack:
        raise InvalidTransitionError('Unmatched start tokens remain')
    if len(inter_list) != 1:
        raise InvalidTransitionError('There is more than one root element!')

    return inter_list[0]
