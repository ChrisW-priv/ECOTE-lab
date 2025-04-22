from compiler.default import compiler
from compiler.settings import Settings


def main():
    settings = Settings()
    result = (
        compiler(input_file=settings.input_file, output_dir=settings.output_dir, max_func=settings.max_function) or []
    )
    print(result)


if __name__ == '__main__':
    main()
