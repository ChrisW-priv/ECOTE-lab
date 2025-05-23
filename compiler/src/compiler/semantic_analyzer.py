from compiler.models import ClassAttribute, TypedXmlElement, XmlElement, SemanticAnalyzerOutput
from compiler.errors import SemanticError


class SemanticAnalyzer:
    def __init__(self, root_element: XmlElement) -> None:
        assert root_element.element_name == 'root', 'The tree must start with a root node.'
        self.identified_types: list[set[ClassAttribute]] = []
        self.element_names: list[str] = []
        self.root = root_element

    def analyze(self):
        """
        Perform an analysis on the tree for correctness of all the rules and builds
        a TypedTree, to signify the purpose of each element.
        """
        self.verify_and_build_typed_ast(self.root)

        self.minimize_types()
        self.element_names = []

        typed_ast = self.verify_and_build_typed_ast(self.root, strict=True)

        return typed_ast

    def minimize_types(self):
        """
        Given a list of sets, produce smaller list of sets that will contain all subsets in that list

        Examples:
            input: [{'a'}, {'b'}]
            output: [{'a'}, {'b'}]

            input: [{'a'}, {'b'}, {'a', 'b'}]
            output: [{'a', 'b'}]

            input: [{'a', 'b'}, {'a', 'b'}]
            output: [{'a', 'b'}]
        """
        minimized = set(frozenset(s) for s in self.identified_types)
        to_remove = set()

        for s1 in minimized:
            for s2 in minimized:
                if s1 != s2 and s1.issubset(s2):
                    to_remove.add(s1)
                    break

        self.identified_types = [set(s) for s in minimized if s not in to_remove]

        # Sort the identified_types to ensure deterministic order. Sort them by attribute.name
        self.identified_types.sort(key=lambda attrs: tuple(sorted(attr.name for attr in attrs)))

    def verify_and_build_typed_ast(
        self, element: XmlElement, parent_role: str | None = None, strict: bool = False
    ) -> TypedXmlElement:
        """
        Recursively go through the tree and identify the role of each element,
        and do type analysis based on the available attributes of each element
        """

        """ 
        The type of the current element: if has attributes then it
        is a declaration, else it is a variable, unless this is a child of
        declaration, then it is an attribute.

        There can also be a situation when we begin the analysis, and the
        parent_role is None, in which case it makes sense to identify it as
        root node.
        """
        if parent_role is None:
            identified_role = 'root'
        elif element.attributes:
            identified_role = 'declaration'
            if parent_role == 'declaration':
                raise SemanticError(
                    'declaration node cannot be followed by another declaration node without variable node in between'
                )
        else:
            identified_role = 'variable'
            if parent_role == 'declaration':
                identified_role = 'attribute'
            if parent_role in ('variable', 'attribute'):
                raise SemanticError(f'node with {parent_role=} was followed by node with {identified_role=}!')

        if identified_role in ('variable', 'declaration'):
            if element.element_name in self.element_names:
                raise SemanticError(f'element with name={element.element_name} was already found when parsing the tree')
            self.element_names.append(element.element_name)

        if not element.children:  # leaf nodes
            if identified_role == 'root':
                return TypedXmlElement(
                    element_name=element.element_name,
                    identified_type=-1,
                    identified_role=identified_role,
                    attributes=element.attributes,
                )
            attrs = element.attributes
            if not attrs:
                raise SemanticError('leaf node has to be a declaration node (must have attributes)')
            class_attrs = [ClassAttribute(attr.name, 'string') for attr in attrs]
            unique_class_attrs = set(class_attrs)
            if len(class_attrs) != len(unique_class_attrs):
                raise SemanticError('multiple declarations of one attribute in a single node')

            expand = False

            for i, glob_identified_type in enumerate(self.identified_types):
                if unique_class_attrs.issubset(glob_identified_type):
                    identified_type = i

                    break
                elif glob_identified_type.issubset(unique_class_attrs):
                    identified_type = i
                    expand = True
                    break
            else:
                self.identified_types.append(unique_class_attrs)
                identified_type = len(self.identified_types) - 1
                i = 0

            if expand:
                self.identified_types[i] = unique_class_attrs

            return TypedXmlElement(
                element_name=element.element_name,
                identified_type=identified_type,
                identified_role=identified_role,
                attributes=element.attributes,
            )

        children = [self.verify_and_build_typed_ast(child, identified_role, strict) for child in element.children]
        if identified_role in ('variable', 'attribute'):
            is_list = len(children) > 1 or parent_role == 'root'

            types = set(child.identified_type for child in children)

            if is_list and strict and len(types) > 1:
                raise SemanticError('There are multiple different types in the list that is here!')
            if is_list and parent_role == 'declaration':
                raise SemanticError('Declaration nodes cannot have attributes that are lists.')

            return TypedXmlElement(
                element_name=element.element_name,
                identified_type=children[0].identified_type,
                identified_role=identified_role,
                attributes=element.attributes,
                is_list=is_list,
                children=children,
            )
        if identified_role == 'root':
            return TypedXmlElement(
                element_name=element.element_name,
                identified_type=-1,
                identified_role=identified_role,
                children=children,
            )

        attrs = list(ClassAttribute(attribute.name, 'string') for attribute in element.attributes or [])
        children_types = list(ClassAttribute(child.element_name, str(child.identified_type)) for child in children)
        class_attrs = attrs + children_types
        unique_class_attrs = set(class_attrs)
        if len(class_attrs) != len(unique_class_attrs):
            raise SemanticError('multiple declarations of one attribute in a single node')

        expand = False
        for i, glob_identified_type in enumerate(self.identified_types):
            if unique_class_attrs.issubset(glob_identified_type):
                identified_type = i
                break
            elif glob_identified_type.issubset(unique_class_attrs):
                identified_type = i
                expand = True
                break
        else:
            self.identified_types.append(unique_class_attrs)
            identified_type = len(self.identified_types) - 1

        if expand:
            self.identified_types[i] = unique_class_attrs

        return TypedXmlElement(
            element_name=element.element_name,
            identified_type=identified_type,
            identified_role=identified_role,
            children=children,
            attributes=element.attributes,
        )


def semantic_analyzer(ast: XmlElement) -> SemanticAnalyzerOutput:
    """
    Takes in naive input of XmlElement and analyzes it for correctness.
    In the same time, it generates some Typed AST to make it easy for the later
    stages to do the work (since we already have done the work once)
    """
    semantic_analyzer = SemanticAnalyzer(ast)

    # Perform the semantic analysis
    typed_ast = semantic_analyzer.analyze()
    types = semantic_analyzer.identified_types
    return SemanticAnalyzerOutput(typed_ast, types)
