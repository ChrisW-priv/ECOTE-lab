from compiler.default import compiler
from compiler.settings import Settings


def main():
    settings = Settings()
    compiler(settings.input_file, settings.output_dir)


if __name__ == '__main__':
    main()
