from typing import Dict
from compiler.models import TypedTree


def code_gen(typed_ast: TypedTree) -> Dict[str, str]:
    """
    Generates C# code from the AST.

    Args:
        typed_ast (TypedTree): The semantically analyzed AST.

    Returns:
        Dict[str, str]: A mapping from filenames to their C# code content.
    """
    code_files = {}

    # Generate C# class definitions
    for class_def in typed_ast.types:
        class_code = f"public class {class_def.name} {{\n"
        for attr in class_def.attributes:
            class_code += f"    public {attr.attribute_type} {attr.name} {{ get; set; }}\n"
        class_code += "}\n"
        code_files[f"{class_def.name}.cs"] = class_code

    # Generate Main.cs with instance declarations
    main_code = "public class Program {\n    public static void Main() {\n"
    for decl in typed_ast.declarations:
        main_code += f"        var {decl.instance_name} = new {decl.class_name} {{\n"
        for attr in decl.attributes:
            main_code += f"            {attr.name} = \"{attr.value}\",\n"
        main_code += "        };\n"
    main_code += "    }\n}\n"
    code_files["Main.cs"] = main_code

    return code_files
