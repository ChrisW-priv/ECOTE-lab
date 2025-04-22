# Compiler Project

## Introduction
Brief overview of the project, its purpose, and key functionalities.

## Features
- Tokenization of XML input
- Parsing and AST construction
- Semantic analysis
- Intermediate code generation
- C# code generation
- Comprehensive testing suite

## Components

### Scanner
Detailed explanation of the scanner, including token types and state transitions.

### Parser
Description of the parsing process, state transitions, and AST construction.

### Semantic Analyzer
Insights into semantic analysis, type verification, and role assignments.

### Intermediate Code Generation
Overview of how intermediate representations are created from the AST.

### Code Generation
Explanation of translating intermediate code into C# code using templates.

### Code Writer
Details on writing the generated C# code to the filesystem.

## Testing

The compiler includes a comprehensive suite of tests to ensure functionality and correctness:

- **Scanner Tests (`test_scanner.py`):** Verify tokenization of input XML strings.
- **Parser Tests (`test_parser.py`):** Ensure accurate AST construction from tokens.
- **Semantic Analyzer Tests (`test_semantic_analyzer.py`):** Validate semantic correctness of the AST.
- **Intermediate Code Generation Tests (`test_inter_code_gen.py`):** Check accurate generation of intermediate code.
- **Code Generation Tests (`test_code_gen.py`):** Verify proper translation into C# code.
- **Writer Tests (`test_writer.py`):** Ensure correct writing of generated code to disk.
- **Settings Tests (`test_settings.py`):** Validate configuration and command-line argument parsing.
- **Reader Tests (`test_reader.py`):** Test the source reader's ability to handle input files.

**Running the Tests:**

To execute all tests, navigate to the `compiler` directory and run:

```bash
pytest
```

Ensure all dependencies are installed and the environment is properly set up before running the tests.

## Models

The compiler utilizes various data models defined in `compiler/src/compiler/models.py`. These models represent tokens, XML elements, class attributes, declarations, and intermediate code structures.

## Usage

**Installation:**

Ensure Python is installed. Install required dependencies using:

```bash
pip install -r requirements.txt
```

**Running the Compiler:**

Execute the compiler with the input XML file and specify the output directory for the generated C# code:

```bash
python main.py path/to/input.xml path/to/output_directory
```

- `path/to/input.xml`: Path to your input XML file.
- `path/to/output_directory`: Directory where the generated C# files will be saved. Defaults to `generated` if not specified.

**Generated Code:**

Navigate to the output directory to find the generated C# class files and `Main.cs`.

## Contributing

Guidelines for contributing to the project, including setting up the development environment, coding standards, and submitting pull requests.

## License

Information about the project's license.

## Acknowledgments

Credits and acknowledgments for contributors, resources, and inspirations.
## Usage

**Installation:**

Ensure Python is installed. Install required dependencies using:

```bash
pip install -r requirements.txt
```

**Running the Compiler:**

Execute the compiler with the input XML file and specify the output directory for the generated C# code:

```bash
python main.py path/to/input.xml path/to/output_directory
```

- `path/to/input.xml`: Path to your input XML file.
- `path/to/output_directory`: Directory where the generated C# files will be saved. Defaults to `generated` if not specified.

**Generated Code:**

Navigate to the output directory to find the generated C# class files and `Main.cs`.
