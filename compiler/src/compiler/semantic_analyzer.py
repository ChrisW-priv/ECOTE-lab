from compiler.models import ClassAttribute, TypedXmlElement, XmlElement
from compiler.errors import SemanticError


def verify_and_build_typed_ast(
    element: XmlElement, parent_type: str | None = None, parent_role: str | None = None
) -> TypedXmlElement:
    # Determine the type of the current element
    identified_type = 'variable'
    if element.attributes:
        identified_type = 'declaration'

    # Determine the role of the current element
    if identified_type == 'declaration' and parent_role != 'root':
        identified_role = 'value_of_an_attribute'
    elif identified_type == 'variable' and parent_type is None:
        identified_type = 'root'
        identified_role = 'root'
    elif parent_type == 'declaration':
        identified_role = 'attribute_of_parent'
    else:
        identified_role = None

    # Recursively process children
    children = [
        verify_and_build_typed_ast(child, identified_type, identified_role) for child in (element.children or [])
    ]

    types = set(child.identified_type for child in children)
    if len(types) == 0 and identified_type == 'variable' and element.element_name != 'root':
        raise SemanticError('"variable" node has no children')
    if len(types) == 1:
        children_type = next(iter(types))
        if identified_type == children_type:
            raise SemanticError(f'{identified_type=} cannot have children of type {children_type=}')
    if len(types) > 1 and identified_role != 'root':
        raise SemanticError(f'{identified_type=} has mixed children {types=}')

    full_attributes = list(ClassAttribute(attribute.name, 'string') for attribute in element.attributes or [])
    children_names = []
    if identified_type == 'declaration' and element.children:
        children_names = list(ClassAttribute(child.element_name, 'declaration') for child in children)
    full_attributes = (full_attributes + children_names) or None

    return TypedXmlElement(
        element_name=element.element_name,
        identified_type=identified_type,
        identified_role=identified_role,
        attributes=element.attributes,
        full_attributes=full_attributes,
        children=children if children else None,
    )


def resolve_types(typed_ast: TypedXmlElement) -> TypedXmlElement:
    """
    Should add any type to generic "declaration" type and return types of the
    declarations.
    """
    return typed_ast


def semantic_analyzer(ast: XmlElement) -> TypedXmlElement:
    """
    Perform an analysis on the tree for correctness of all the rules and builds
    a TypedTree, to signify the purpose of each element.
    """
    # Start the verification and building process
    if ast.element_name != 'root':
        raise SemanticError('The tree must start with a root node.')

    semi_typed_ast = verify_and_build_typed_ast(ast)
    typed_ast = resolve_types(semi_typed_ast)
    return typed_ast
