from compiler.models import (
    ClassAttribute,
    InstanceAttribute,
    IntermediateCode,
    SemanticAnalyzerOutput,
    Class,
    Declaration,
    TypedXmlElement,
)


class IntermediateCodeGeneration:
    def __init__(self, sem_output: SemanticAnalyzerOutput) -> None:
        self.sem_output = sem_output
        self.declarations: list[Declaration] = []
        self.types: list[Class] = []
        self.declaration_seq = 0

    def run(self):
        self.populate_types()
        self.populate_declarations()

    def populate_types(self):
        for i, set_of_attrs in enumerate(self.sem_output.types, start=1):
            class_name = f'Class{i}'
            self.types.append(Class(class_name, list(set_of_attrs)))

        for _type in self.types:
            attrs = []
            for attr in _type.attributes:
                if attr.attribute_type in (str(i) for i in range(10)):
                    type_index = int(attr.attribute_type)
                    type_name = self.types[type_index].name
                    attr = ClassAttribute(attr.name, type_name)
                attrs.append(attr)
            _type.attributes = attrs

    def populate_declarations(self):
        def rec(element: TypedXmlElement, parent_role: str | None = None):
            if not element.children:  # leaf node
                id_assigned = self.declaration_seq
                self.declaration_seq += 1
                el_type = (
                    element.identified_type
                    if element.identified_type == 'string'
                    else self.types[int(element.identified_type)].name
                )
                is_list = parent_role == 'root' and element.identified_role == 'variable'
                attributes = list(
                    InstanceAttribute(name=attr.name, value=attr.value) for attr in element.attributes or []
                )
                self.declarations.append(
                    Declaration(
                        id=str(id_assigned),
                        instance_name=element.element_name,
                        class_name=el_type,
                        is_list=is_list,
                        attributes=attributes,
                    )
                )
                return str(id_assigned)
            ids = [rec(child, parent_role=element.identified_role) for child in element.children]
            if element.identified_role == 'root':
                return
            if element.identified_role == 'attribute':
                return ids[0]
            id_assigned = self.declaration_seq
            self.declaration_seq += 1
            el_type = (
                element.identified_type
                if element.identified_type == 'string'
                else self.types[int(element.identified_type)].name
            )
            is_list = parent_role == 'root' and element.identified_role == 'variable'
            immediate_attributes = list(
                InstanceAttribute(name=attr.name, value=attr.value) for attr in element.attributes or []
            )
            child_attributes = list(
                InstanceAttribute(name=child.element_name, ref=id) for child, id in zip(element.children, ids)
            )
            attributes = immediate_attributes + child_attributes
            self.declarations.append(
                Declaration(
                    id=str(id_assigned),
                    instance_name=element.element_name,
                    class_name=el_type,
                    is_list=is_list,
                    attributes=attributes,
                )
            )
            return str(id_assigned)

        if not self.sem_output.typed_ast.children:
            return
        rec(self.sem_output.typed_ast)


def inter_code_gen(semantic_analysis_output: SemanticAnalyzerOutput) -> IntermediateCode:
    """
    Identify unique classes and it's types, and Identify all declarations and
    it's dependencies (references to other declaration, that we need to build
    first and use to build current instance) (declarations are guaranteed to be
    returned in the topological order, such that the instance lvalue is allways
    available for later instances)
    """
    inter_code_generation = IntermediateCodeGeneration(semantic_analysis_output)
    inter_code_generation.run()
    types = inter_code_generation.types
    declarations = inter_code_generation.declarations
    return IntermediateCode(types, declarations)
