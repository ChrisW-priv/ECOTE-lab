# ECOTE Project

**Author**: Krzysztof Watras  
**Semester**: 2025L  
**Subject**: XML to C# Class Compiler

---

## I. General Overview and Assumptions

This project automates the generation of C# class definitions based on a given XML file. The system parses XML, identifies data structures, and generates corresponding C# classes, constructors, method stubs, and a `Main` method.

### Assumptions

- XML must begin with a `<root>` element. Otherwise, it's an error.
- Each unique type results in a separate file.
- Elements directly under `<root>` are initialized in `Main.cs`.
- Whitespace or indentation is ignored.
- A new type is defined if a unique set of attribute names or child elements is encountered.
- Elements with fewer attributes than a known type use the existing type.
- Element children define how properties should be named.
- Repeated elements of the same type imply a list; mixed types are errors.
- Element instances may use `/>` to self-close.
- Each instance's name is used as its variable name in `Main.cs`.
- Unclosed root or mixed-type lists are errors.
- An empty `<root>` body results in no output, but not an error.

### Required Class Methods (Declared Only)

- `Equals`
- `Finalize`
- `GetHashCode`
- `MemberwiseClone`
- `ToString`

> `GetType` and `ReferenceEquals` should **not** be implemented.

---

## II. Functional Requirements

1. Accept an XML file as input.
2. Parse the XML into an Abstract Syntax Tree (AST).
3. On XML error, display error message and terminate.
4. Save output files to disk.
5. Run via CLI.

---

## III. Grammar Description

### Terminals

- `ALPHANUM`: a–z, A–Z, 0–9
- `WS`: Whitespace (ignored except in strings)
- `SLASH`: `/`
- `LT`: `<`
- `GT`: `>`
- `EQ`: `=`
- `QUOTE`: `"`

### Non-Terminals & Productions

```
ROOT      -> < root > ELEMENTS </ root >
ELEMENTS  -> ELEMENT ELEMENTS | ε
ELEMENT   -> START_TAG ELEMENTS END_TAG | < IDENTIFIER ATTRIBUTES />
START_TAG -> < IDENTIFIER ATTRIBUTES >
END_TAG   -> </ IDENTIFIER >
ATTRIBUTES-> ATTRIBUTE ATTRIBUTES | ε
ATTRIBUTE -> IDENTIFIER = STRING
STRING    -> " IDENTIFIER "
IDENTIFIER-> ALPHANUM IDENTIFIER | ALPHANUM
```

> **TODO**:
- Restrict `IDENTIFIER` to start with alphabet only.
- Allow `STRING` to contain any character except `"`.

---

## IV. Implementation

### Architecture Overview

Modular components include:

- `Source`
- `Scanner`
- `Parser`
- `Semantic Analyzer`
- `Code Generator`
- `Writer`

> **TODO**: Add diagram here.

### Data Structures

- `set`: quick element lookup
- `str`: intermediate and result storage in scanner
- `dict`: AST and mappings

### Module Descriptions

- **Scanner**: Tokenizes XML input.
- **Parser**: Builds AST from tokens.
- **Semantic Analyzer**: Validates AST structure.
- **Code Generator**: Produces a map of filename → content.
- **Writer**: Writes content to disk.

### Input/Output

- CLI accepts XML file path.
- Outputs C# files to the working directory.

### Notes

- Entire implementation resides in `main.py`.
- Unit tests written with `pytest`, in flat file or folder format.

---

## V. Functional Test Cases

| Test Case | Input | Expected Output |
|-----------|-------|-----------------|
| **TC1.1** | Valid XML file | Compiler accepts file |
| **TC1.2** | Non-XML file (.txt/.json) | Error: Invalid file format |
| **TC1.3** | Missing file | Error: File not found |
| **TC2.1** | Well-formed XML | AST generated successfully |
| **TC2.2** | Malformed XML data | Error message displayed |
| **TC3.1** | XML with unclosed tags | Error: XML parsing failed |
| **TC3.2** | Non-XML content | Error: Invalid XML |
| **TC4.1** | Valid input via CLI | Output files saved to disk |

> **TODO**: Add I/O examples to each test case.

