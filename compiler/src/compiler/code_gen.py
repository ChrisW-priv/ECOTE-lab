from compiler.models import TypedTree, ClassAttribute, Declaration


def generate_class_code(class_name: str, attributes: list[ClassAttribute]) -> str:
    """
    Generates C# class code for the given class name and attributes.

    Args:
        class_name (str): The name of the class.
        attributes (List[ClassAttribute]): A list of class attributes.

    Returns:
        str: The generated C# class code as a string.
    """
    lines = ['using System;', '', f'public class {class_name}', '{']

    for attr in attributes:
        csharp_type = attr.attribute_type
        # Capitalize the attribute name to follow C# naming conventions
        prop_name = attr.name.title()
        lines.append(f'    public {csharp_type} {prop_name} {{ get; set; }}')

    # Add boilerplate method declarations
    boilerplate_methods = [
        '',
        '    public override bool Equals(object obj)',
        '    {',
        '        throw new NotImplementedException();',
        '    }',
        '',
        '    protected override void Finalize()',
        '    {',
        '        // Finalize resources if necessary',
        '    }',
        '',
        '    public override int GetHashCode()',
        '    {',
        '        throw new NotImplementedException();',
        '    }',
        '',
        '    protected object MemberwiseClone()',
        '    {',
        '        throw new NotImplementedException();',
        '    }',
        '',
        '    public override string ToString()',
        '    {',
        '        throw new NotImplementedException();',
        '    }',
    ]
    lines.extend(boilerplate_methods)
    lines.append('}')
    return '\n'.join(lines)


def generate_instance_declaration(decl: Declaration, instances: dict) -> tuple[str, dict]:
    """
    Generates a single instance declaration line for Main.cs based on the declaration.

    Args:
        decl (Declaration): The declaration object containing instance details.
        instances (dict): A dictionary mapping declaration IDs to instance names.

    Returns:
        str: The generated instance declaration line as a string.
    """
    class_name = decl.class_name
    instance_name = decl.instance_name
    args = []
    for attr in decl.attributes:
        if attr.ref:
            # Reference to another instance
            ref_instance = instances.get(attr.ref)
            if not ref_instance:
                raise ValueError(f'Reference ID {attr.ref} not found.')
            args.append(ref_instance)
        elif attr.value is not None:
            # Only append value if ref is not present
            args.append(f'"{attr.value}"')
        else:
            # If neither ref nor value is present, append null
            args.append('null')
    args_str = ', '.join(args)
    declaration_line = f'{class_name} {instance_name} = new {class_name}({args_str});'
    instances[decl.id] = instance_name  # Store instance for future references
    return declaration_line, instances


def generate_main(declarations: list[Declaration]) -> str:
    """
    Generates the content for Main.cs based on the declarations.

    Args:
        declarations (List[Declaration]): The list of declarations.

    Returns:
        str: The generated Main.cs content.
    """
    main_lines = []
    instances = {}
    for decl in declarations:
        declaration_line, instances = generate_instance_declaration(decl, instances)
        main_lines.append(declaration_line)
    return '\n'.join(main_lines)


def code_gen(typed_ast: TypedTree) -> dict[str, str]:
    """
    Generates C# code from the AST.

    Args:
        typed_ast (TypedTree): The semantically analyzed AST.

    Returns:
        Dict[str, str]: A mapping from filenames to their C# code content.
    """
    """
    Generates C# code from the AST.

    Args:
        typed_ast (TypedTree): The semantically analyzed AST.

    Returns:
        Dict[str, str]: A mapping from filenames to their C# code content.
    """
    code_files = {}

    for new_type in typed_ast.types:
        class_code = generate_class_code(new_type.name, new_type.attributes)
        filename = f'{new_type.name}.cs'
        code_files[filename] = class_code

    # Generate Main.cs based on declarations
    main_content = generate_main(typed_ast.declarations)
    code_files['Main.cs'] = main_content

    return code_files
