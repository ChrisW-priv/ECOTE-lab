from typing import Callable
from compiler.reader import source_reader
from compiler.scanner import scanner
from compiler.parser import parser
from compiler.semantic_analyser import semantic_analyser
from compiler.code_gen import code_gen
from compiler.writer import writer


def pipe(*functions: Callable) -> Callable:
    def piped(x):
        for f in functions:
            x = f(x)
        return x

    return piped


def compiler(input_file: str, output_dir: str) -> None:
    try:
        generated_code = pipe(source_reader, scanner, parser, semantic_analyser, code_gen)(input_file)
        writer(generated_code, output_dir)
    except Exception as e:
        print(f'Exception occurred: {type(e).__name__} - {e}')
