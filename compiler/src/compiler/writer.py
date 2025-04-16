import os


def writer(file_map: dict[str, str], output_dir: str) -> None:
    """
    Writes the generated C# code to disk.

    Args:
        file_map (Dict[str, str]): A mapping from filenames to their C# code content.
        output_dir (str): The directory to output the C# code.
    """
    os.makedirs(output_dir, exist_ok=True)
    for filename, content in file_map.items():
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w") as file:
            file.write(content)
