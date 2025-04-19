from compiler.models import TypedXmlElement, XmlElement
from compiler.errors import SemanticError


def verify_and_build_typed_ast(element: XmlElement, parent_type: str | None = None) -> TypedXmlElement:
    # Determine the type of the current element
    identified_type = 'variable'
    if element.attributes:
        identified_type = 'declaration'

    if identified_type == parent_type:
        raise SemanticError(f'{parent_type=} cannot have child of {identified_type=}')

    # Determine the role of the current element
    if parent_type == 'variable':
        identified_role = 'attribute_of_parent'
    elif parent_type == 'declaration':
        identified_role = 'value_of_an_attribute'
    else:
        identified_role = None

    # Recursively process children
    children = [verify_and_build_typed_ast(child, identified_type) for child in (element.children or [])]

    types = set(child.identified_type for child in children)
    if len(types) != 1:
        raise SemanticError(f'{identified_type=} has mixed children {types=}')

    return TypedXmlElement(
        element_name=element.element_name,
        identified_type=identified_type,
        identified_role=identified_role,
        attributes=element.attributes,
        children=children if children else None,
    )


def semantic_analyzer(ast: XmlElement) -> TypedXmlElement:
    """
    Perform an analysis on the tree for correctness of all the rules and builds
    a TypedTree, to signify the purpose of each element.
    """
    # Start the verification and building process
    if ast.element_name != 'root':
        raise SemanticError('The tree must start with a root node.')

    return verify_and_build_typed_ast(ast)
