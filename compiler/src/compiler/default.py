from typing import Callable
from compiler.reader import source_reader
from compiler.scanner import scanner
from compiler.parser import parser
from compiler.semantic_analyzer import semantic_analyzer
from compiler.inter_code_gen import inter_code_gen
from compiler.code_gen import code_gen
from compiler.writer import writer


def pipe(*functions: Callable) -> Callable:
    def piped(x):
        for f in functions:
            x = f(x)
        return x

    return piped


def compiler(input_file: str, output_dir: str, max_func) -> None:
    functions = (source_reader, scanner, parser, semantic_analyzer, inter_code_gen, code_gen, writer)
    str_functions = (
        'source_reader',
        'scanner',
        'parser',
        'semantic_analyzer',
        'inter_code_gen',
        'code_gen',
    )
    max_index = str_functions.index(max_func)
    functions = functions[: max_index + 1]
    try:
        result = pipe(*functions)(input_file)
        return result
    except Exception as e:
        print(f'Exception occurred: {type(e).__name__} - {e}')
