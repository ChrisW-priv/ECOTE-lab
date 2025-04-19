from compiler.models import IntermediateCode, TypedXmlElement


def inter_code_gen(typed_ast: TypedXmlElement) -> IntermediateCode:
    """
    Identify unique classes and it's types, and Identify all declarations and
    it's dependencies (references to other declaration, that we need to build
    first and use to build current instance) (declarations are guaranteed to be
    returned in the topological order, such that the instance lvalue is allways
    available for later instances)
    """
    ...
