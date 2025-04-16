from typing import Iterable


def source_reader(filename: str):
    with open(filename) as file:
        while (char := file.read(1)):
            yield char


def scanner(chars: Iterable[str]):
    ...


def parser(tokens: Iterable[Token]):
    ...


def semantic_analyser(ast):
    ...


def code_gen(ast):
    ...


def writer(file_map: dict[str, str]):
    ...

