![Ruff](https://github.com/ChrisW-priv/ECOTE-lab/actions/workflows/ruff.yml/badge.svg)
![Pytest](https://github.com/ChrisW-priv/ECOTE-lab/actions/workflows/pytest.yml/badge.svg)

# ECOTE-lab

## Project Overview

ECOTE-lab's compiler pipeline transforms XML files into C# class files through
a structured multi-phase process. The pipeline includes source reading, lexical
analysis, syntax parsing, semantic analysis, code generation, and writing the
output to disk. This ensures efficient and accurate conversion tailored for
project-specific requirements.

## **Compiler Pipeline Overview**

The compiler designed for this project follows a classical multi-phase
structure, tailored specifically for converting XML files into corresponding C#
class files. Each stage of the pipeline plays a specific role:

1. **Source**
2. **Scanner (Lexical Analyzer)**
3. **Parser (Syntactic Analyzer)**
4. **Semantic Analyzer**
5. **Intermediate Code Generation**
6. **Code Generator**
7. **Writer**

On each stage, there can be errors in the input data, so we define special 
methods to both detect them, raise exceptions and capture them safely.

---

## General overview and assumptions

This program is designed to automate the generation of C# class definitions
based on the structure and content of a given XML file. The goal is to parse
the XML, identify unique data structures, and produce corresponding C# classes
with appropriate properties, constructors, and method stubs. In addition to
defining these classes, the program also generates a Main method or equivalent
setup code that instantiates these classes with data read from the XML file.

Assumptions:
-	File always starts with `<root>` identifier. If it doesn’t -> error.
-	Each unique type has a separate file
-	Each element that is defined as a child of root should be initialized in the Main.cs
-	Indentation or spacing between identifiers makes no difference on the final output
-	New type is defined, if there is a unique set of `attribute names` in the body, and subsequent children of the element. If there is an element that has a subset of the attribute names from some “bigger” class, then it is not a new type. Instead, it is the same class, but with fewer params.
-	Children of an element cannot be declarations, they need to be name “wrappers” that define how the property should be called.
-	Any element that has multiple declarations of some type is really a list of that type. If the types are mixed -> error
-	Declaration of each type instance can be stopped by using the `/>` string
-	Element name should be the name of an instance put in the Main.cs
-	If a list contains multiple class types: this is an error
-	If the root element is not closed -> error
-	If the body of root is empty -> Just finish, (no error)
-	Each class should implement a method: (don’t implement just declare)
o	Equals – it will check the equality of each attribute of the class
o	Finalize – release the dynamic memory of the instance (?)
o	GetHashCode – return some unique hash of the instance
o	MemberwiseClone – Creates a shallow copy.
o	ToString – create string representation of the instance (assume each attribute will have ToString method)
-	There will never be variable node inside another variable node.
-	There will never be declaration node inside another declaration node
-	Classes will never have attributes that have a list type.
II.	Functional requirements

1.	The compiler shall accept an XML file as input.
2.	Compiler should parse the XML and produce the AST from it
3.	In case of the error in the XML file structure, 
compiler should terminate and produce error message.
4.	Result of the Compiler run should be saved to appropriate files on disc
5.	User should be able to run the program using CLI 

Grammar Description

Terminals
•	ALPHA: a-zA-Z characters
•	WS: Whitespace characters (space, tab, newline) as well as new line (`\n`)
ignored except within quoted strings.
•	SLASH: `/` character.
•	LT: `<` character.
•	GT: `>` character.
•	EQ: `=` character.
•	QUOTE: `”` character
•	NOT_QUOTE: ANY character that is NOT QUOTE
•	ALPHANUM_UNDER: a-zA-Z0-9 or `_`
•	EOF: end of file

Non- Terminals + productions

ROOT  ->  
TO_TRIM `<` TO_TRIM `root` TO_TRIM `>` 
TO_TRIM ELEMENTS 
TO_TRIM `</` TO_TRIM `root` TO_TRIM `>` TO_TRIM EOF

TO_TRIM -> WS TO_TRIM | epsilon
ELEMENTS -> ELEMENT  TO_TRIM ELEMENTS | epsilon
ELEMENT -> 
START_TAG TO_TRIM ELEMENTS TO_TRIM END_TAG | 
`<` IDENTIFIER TO_TRIM ATTRIBUTES TO_TRIM `/>`

START_TAG -> `<` TO_TRIM IDENTIFIER TO_TRIM ATTRIBUTES TO_TRIM `>`
END_TAG -> `</` TO_TRIM IDENTIFIER TO_TRIM `>`
ATTRIBUTES -> ATTRIBUTE TO_TRIM ATTRIBUTES | epsilon
ATTRIBUTE -> IDENTIFIER TO_TRIM `=` TO_TRIM STRING
STRING -> `”` NOT_QUOTE `”`
IDENTIFIER -> ALPHA IDENTIFIER_CHAR
IDENTIFIER_CHAR -> ALPHANUM_UNDER IDENTIFIER_CHAR | epsilon

The code generation will follow the rules:

- ANY Element defined will have separate initialization. (implicit: there is always a name to a variable)

Example:

```xml
<foo attr1 = “var” />
```

will become

```cs
Class1 foo = new Class1(“var”);
```

- Type declarations:

They will either be one liners:
```xml
<foo attr1 = “var” />
```

or be more complex:

```xml
<foo attr1 = “var” >
<attr2><bar attr1=”vaz”></attr2>
</foo>
```

- If there is two elements as children:

```xml
<cats>
    <tom Name="Tom" Companion="Jerry"/>
    <garfield Name="Garfield" Companion="Odie"/>
</cats>
```

then this is a list:

```cs
Class2 tom = new Class2("Tom", "Jerry");
Class2 garfield = new Class2("Garfield", "Odie");
List<Class2> cats;
cats.Add(tom);
cats.Add(garfield);
```

Notice: the addition to the list is AFTER the initialization.

In case there is only one element as a child to an element where there is no
attributes:

<cats>
<tom Name="Tom" Companion="Jerry"/>
</cats>

then this this is based on a context: in an instance declaration -> cats is a
name of a class attribute in case this is a child of a root, then this is still
a list of one element.

## Implementation

### General architecture

We shall design the compiler to be as separated as possible.
We will have following steps:

- Source
- Scanner
- Parser
- Semantic Analyzer
- Intermediate Code Generator
- Code Generator
- Writer

### Data Structures

The compiler utilizes a well-defined set of data structures to represent tokens, XML elements, class attributes, declarations, and intermediate code. These structures are primarily defined in `compiler/src/compiler/models.py` and are essential for the various phases of the compilation process.

- **Tokens:**
  - **Symbol:** Represents special characters like `<`, `/>`, `>`, `/`, `=`.
  - **Text:** Represents alphanumeric text and underscores.
  - **String:** Represents text enclosed in quotes, excluding newline characters.

- **XML Elements:**
  - **XmlElement:** Represents elements in the Abstract Syntax Tree (AST) with properties such as `element_name`, `attributes`, and `children`.
  - **ElementAttribute:** Represents attributes of XML elements with `name` and `value`.

- **Class Attributes and Declarations:**
  - **ClassAttribute:** Represents attributes of C# classes with `name` and `attribute_type`.
  - **InstanceAttribute:** Represents attributes of class instances with `name`, `value`, `ref`, and `is_list`.
  - **Declaration:** Represents instance declarations in the final C# code with properties like `id`, `instance_name`, `class_name`, `attributes`, and `is_list`.
  - **Class:** Represents C# classes with `name` and a list of `ClassAttribute` objects.
  - **IntermediateCode:** Encapsulates the list of `Class` and `Declaration` objects that form the intermediate representation before code generation.
  - **TypedXmlElement:** Extends `XmlElement` with additional properties such as `identified_type`, `identified_role`, and `is_list` to facilitate semantic analysis.

- **Semantic Analyzer Output:**
  - **SemanticAnalyzerOutput:** Contains the `TypedXmlElement` (typed AST) and a list of sets of `ClassAttribute`, representing identified types after semantic analysis.

These data structures ensure a robust and flexible framework for transforming XML input into structured C# code, allowing each phase of the compiler to operate effectively and maintainably.

### Module Descriptions

Each module in the compiler pipeline is responsible for a distinct phase of the compilation process. Below is an overview of each module and its functionality:

1. **Source:**
   - **Description:** Handles the intake of the XML source files. It reads the input XML files and prepares the data for lexical analysis.
   - **Key Components:** `source_reader` function in `compiler/src/compiler/reader.py`.

2. **Scanner (Lexical Analyzer):**
   - **Description:** Converts the raw XML input into a sequence of lexical tokens. It identifies symbols, text, and strings based on the defined grammar.
   - **Key Components:** `scanner` function in `compiler/src/compiler/scanner.py` and the `StateTransition` class that manages state changes during scanning.

3. **Parser (Syntactic Analyzer):**
   - **Description:** Processes the sequence of tokens generated by the scanner to construct an Abstract Syntax Tree (AST). It ensures the XML structure adheres to the defined grammar rules.
   - **Key Components:** `parser`, `build_ast`, and `build_xml_tokens` functions in `compiler/src/compiler/parser.py`.

4. **Semantic Analyzer:**
   - **Description:** Analyzes the AST to enforce semantic rules, such as type verification and role assignments. It identifies unique data structures and prepares them for intermediate code generation.
   - **Key Components:** `SemanticAnalyzer` class and `semantic_analyzer` function in `compiler/src/compiler/semantic_analyzer.py`.

5. **Intermediate Code Generator:**
   - **Description:** Transforms the semantically analyzed AST into an intermediate representation that simplifies code generation. It maps classes and declarations into a structured format.
   - **Key Components:** `inter_code_gen` function in `compiler/src/compiler/inter_code_gen.py`.

6. **Code Generator:**
   - **Description:** Converts the intermediate code into actual C# code. It uses templates to generate class definitions and instance declarations based on the intermediate representation.
   - **Key Components:** `code_gen` function in `compiler/src/compiler/code_gen.py`.

7. **Writer:**
   - **Description:** Handles the output of the generated C# code to the filesystem. It writes the code to specified directories, organizing files as needed.
   - **Key Components:** `writer` function in `compiler/src/compiler/writer.py`.

8. **Settings:**
   - **Description:** Manages configuration and command-line arguments for the compiler. It allows users to specify input files, output directories, and other configuration options.
   - **Key Components:** `Settings` class in `compiler/src/compiler/settings.py` and `compiler/tests/test_settings.py`.

9. **Main:**
   - **Description:** Serves as the entry point of the compiler. It orchestrates the compilation process by invoking the appropriate modules based on user input.
   - **Key Components:** `main` function in `main.py`.

Each module is designed to operate independently, ensuring a modular and maintainable codebase. Comprehensive tests are provided for each module to validate functionality and handle edge cases effectively.

### Input/Output Description

Understanding the input and output formats is crucial for effectively using the compiler. Below is a detailed description of the expected inputs and the generated outputs.

#### **Input**

- **Format:** XML files.
- **Structure:**
  - The XML file must begin with a `<root>` element. If the root element is missing or not properly closed, the compiler will raise an error.
  - Each XML element represents a C# class or instance, depending on its position and attributes.
  - Attributes within XML elements define the properties of the corresponding C# classes or instances.
  - Self-closing tags (e.g., `<foo attr="value"/>`) represent single-instance declarations.
  - Nested elements define relationships between classes, such as composition or aggregation.

- **Example:**

  ```xml
  <root>
      <kitten Name="Whiskers">
          <parent>
              <cat Name="The Garfield"/>
          </parent>
      </kitten>
  </root>
  ```

#### **Output**

- **Format:** C# class files and a `Main.cs` file.
- **Structure:**
  - **Class Files (`ClassName.cs`):** Each unique class identified in the XML will have its own `.cs` file containing the class definition with properties, constructors, and method stubs.
  - **Main.cs:** This file contains the `Main` method, which instantiates the classes defined in the class files based on the declarations in the XML.
  - **Directory:** All generated files are saved in the specified output directory. By default, this is the `generated` folder unless otherwise specified via command-line arguments.

- **Example Generated Code:**

  - **Class1.cs:**
    ```cs
    using System;

    public class Class1
    {
        public Class1 Parent { get; set; }
        public string Name { get; set; }

        public Class1(Class1 parent, string name)
        {
            Parent = parent;
            Name = name;
        }

        public override bool Equals(object obj)
        {
            throw new NotImplementedException();
        }

        protected override void Finalize()
        {
            // Finalize resources if necessary
        }

        public override int GetHashCode()
        {
            throw new NotImplementedException();
        }

        protected object MemberwiseClone()
        {
            throw new NotImplementedException();
        }

        public override string ToString()
        {
            throw new NotImplementedException();
        }
    }
    ```

  - **Main.cs:**
    ```cs
    Class1 cat = new Class1("The Garfield");
    Class1 kitten = new Class1(cat, "Whiskers");
    ```

#### **Command-Line Interface (CLI)**

Users interact with the compiler via the command line. Below are the commands and options available.

- **Installation:**

  Ensure Python is installed. Install required dependencies using:

  ```bash
  pip install -r requirements.txt
  ```

- **Running the Compiler:**

  Execute the compiler with the input XML file and specify the output directory for the generated C# code:

  ```bash
  python main.py path/to/input.xml path/to/output_directory
  ```

  - `path/to/input.xml`: **(Required)** Path to your input XML file.
  - `path/to/output_directory`: **(Optional)** Directory where the generated C# files will be saved. Defaults to `generated` if not specified.
  - `max_function`: **(Optional)** Specifies the last function to trigger in the compilation pipeline. Defaults to `writer`.

- **Example Usage:**

  ```bash
  python main.py examples/example1.xml output/
  ```

  This command processes `example1.xml` and outputs the generated C# files to the `output` directory.

#### **Error Handling**

The compiler is designed to handle various input errors gracefully. Common errors include:

- **Malformed XML Structure:**
  - Missing or improperly closed `<root>` element.
  - Mismatched opening and closing tags.
  - Duplicate attributes within an element.

- **Semantic Errors:**
  - Declaration nodes followed by another declaration node without an intermediary variable node.
  - Attributes that are lists where they shouldn’t be.
  - Mixed types within a list.

When such errors are encountered, the compiler will terminate and display a descriptive error message indicating the nature and location of the problem.

### Others

We will use some modern techniques of generating higher quality code by using
`ruff` linter and set it as our pre-commit rule such that, even if we wanted to
we will not be able to commit some unlinted code to the repo. Also, we will
automate tests using `pytest` which generates some very descriptive error
messages in case of difference of output received and output expected. We will 
also make use of Github Badges that are included in th README.md in the root of 
the repo. This serves no other purpose than to make the Repo look nicer.
Those badges are ofcourse connected to the automated Github CI that assure 
code quality and tests passing.

