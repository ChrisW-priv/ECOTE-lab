from compiler import compiler
from settings import Settings
import sys


def main():
    settings = Settings(input_file=sys.argv[1], output_dir=sys.argv[2])
    compiler(settings.input_file, settings.output_dir)


if __name__ == "__main__":
    main()
