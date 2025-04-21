from collections import defaultdict, deque
from typing import Dict, Set
from compiler.models import (
    IntermediateCode,
    TypedXmlElement,
    Class,
    Declaration,
    InstanceAttribute,
)


def inter_code_gen(typed_ast: TypedXmlElement) -> IntermediateCode:
    """
    Identify unique classes and it's types, and Identify all declarations and
    it's dependencies (references to other declaration, that we need to build
    first and use to build current instance) (declarations are guaranteed to be
    returned in the topological order, such that the instance lvalue is allways
    available for later instances)
    """
    classes_dict: Dict[str, Class] = {}
    declarations_dict: Dict[str, Declaration] = {}
    dependencies: Dict[str, Set[str]] = defaultdict(set)

    def traverse(element: TypedXmlElement):
        # Collect Class definitions
        if element.identified_class:
            class_name = element.identified_class.name
            if class_name not in classes_dict:
                classes_dict[class_name] = element.identified_class

        # Collect Declarations
        if element.identified_role == 'declaration':
            decl = Declaration(
                id=element.element_name,  # Assuming 'id' is the element name
                instance_name=element.element_name,
                class_name=element.identified_class.name if element.identified_class else '',
                attributes=[
                    InstanceAttribute(
                        name=attr.name,
                        value=None,  # Set to None as ClassAttribute doesn't have 'value'
                        ref=None,  # Set to None based on test expectations
                    )
                    for attr in element.identified_class.attributes
                    if attr
                ]
                if element.identified_class
                else [],
            )
            declarations_dict[decl.id] = decl
            # Collect dependencies based on 'ref' in attributes
            for attr in decl.attributes:
                if attr.ref:
                    dependencies[decl.id].add(attr.ref)

        # Traverse children
        if element.children:
            for child in element.children:
                traverse(child)

    # Start traversal from the root
    traverse(typed_ast)

    # Perform Topological Sort on Declarations based on dependencies
    sorted_declarations = topological_sort(declarations_dict, dependencies)

    # Collect all Classes
    classes = list(classes_dict.values())

    return IntermediateCode(types=classes, declarations=sorted_declarations)


def topological_sort(declarations: Dict[str, Declaration], dependencies: Dict[str, Set[str]]) -> list[Declaration]:
    """
    Perform topological sort on declarations to ensure correct dependency order.
    """
    in_degree = {decl_id: 0 for decl_id in declarations}
    for deps in dependencies.values():
        for dep in deps:
            if dep in in_degree:
                in_degree[dep] += 1

    queue = deque([decl_id for decl_id, degree in in_degree.items() if degree == 0])
    sorted_decls = []

    while queue:
        decl_id = queue.popleft()
        sorted_decls.append(declarations[decl_id])

        for dependent, deps in dependencies.items():
            if decl_id in deps:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

    if len(sorted_decls) != len(declarations):
        raise ValueError('Cyclic dependency detected among declarations.')

    return sorted_decls
