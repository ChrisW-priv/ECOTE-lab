from compiler import compiler
from settings import Settings
from pydantic_settings import CliApp


def main():
    settings = CliApp.run(Settings)
    compiler(settings.input_file, settings.output_dir)


if __name__ == "__main__":
    main()
