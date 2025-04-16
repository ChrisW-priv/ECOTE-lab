from typing import Iterable


def source_reader(filename: str) -> Iterable[str]:
    """
    Reads characters from the source XML file one by one.

    Args:
        filename (str): The path to the XML file.

    Yields:
        str: The next character in the file.
    """
    with open(filename, "r") as file:
        while char := file.read(1):
            yield char
