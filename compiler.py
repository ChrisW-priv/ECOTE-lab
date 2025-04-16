from reader import source_reader
from scanner import scanner
from parser import parser
from semantic_analyser import semantic_analyser
from code_gen import code_gen
from writer import writer


def compiler(input_file: str, output_dir: str) -> None:
    chars = source_reader(input_file)
    tokens = scanner(chars)
    ast = parser(tokens)
    typed_ast = semantic_analyser(ast)
    generated_code = code_gen(typed_ast)
    writer(generated_code, output_dir)
