from models import Element, TypedTree


def semantic_analyser(ast: Element) -> TypedTree:
    """
    Analyzes the AST to enforce semantic rules. Generates new, tree that enables easy code generation in later stages.

    Args:
        ast (Element): The root of the AST.

    Returns:
        TypedTree: The semantically analyzed AST.
    """
    # Implementation of the semantic analyzer goes here
    return TypedTree([], [])
