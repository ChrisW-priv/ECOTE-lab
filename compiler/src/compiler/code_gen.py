from compiler.models import TypedTree, ClassAttribute


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


def code_gen(typed_ast: TypedTree) -> dict[str, str]:
    """
    Generates C# code from the AST.

    Args:
        typed_ast (TypedTree): The semantically analyzed AST.

    Returns:
        Dict[str, str]: A mapping from filenames to their C# code content.
    """
    code_files = {}

    instances = {}
    for cls in typed_ast.types:
        class_code = generate_class_code(cls.name, cls.attributes)
        filename = f'{cls.name}.cs'
        code_files[filename] = class_code

    # Generate Main.cs based on declarations
    main_lines = []
    for decl in typed_ast.declarations:
        class_name = decl.class_name
        instance_name = decl.instance_name
        # Prepare constructor arguments
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
        main_lines.append(f'{class_name} {instance_name} = new {class_name}({args_str});')

        instances[decl.id] = instance_name  # Store instance for references

    code_files['Main.cs'] = '\n'.join(main_lines)

    return code_files
