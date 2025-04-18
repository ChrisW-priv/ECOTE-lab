![Ruff](https://img.shields.io/badge/ruff-check-brightgreen)
![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen)

# ECOTE-lab

## Project Overview

ECOTE-lab's compiler pipeline transforms XML files into C# class files through a structured multi-phase process. The pipeline includes source reading, lexical analysis, syntax parsing, semantic analysis, code generation, and writing the output to disk. This ensures efficient and accurate conversion tailored for project-specific requirements.

## **Compiler Pipeline Overview**

The compiler designed for this project follows a classical multi-phase structure, tailored specifically for converting XML files into corresponding C# class files. Each stage of the pipeline plays a specific role:

1. **Source**
2. **Scanner (Lexical Analyzer)**
3. **Parser (Syntactic Analyzer)**
4. **Semantic Analyzer**
5. **Code Generator**
6. **Writer**

---

## **1. Source**

- **Input**: Raw XML file (with `.xml` extension)
- **Preconditions**:
  - Must begin with `<root>` and end with `</root>`
  - Valid file extension
  - File must exist
- **Transformations**:
  - No transformation; this is the input feed stage.
- **Example**:
  ```xml
  <root>
    <cat Name="Whiskers"/>
  </root>
  ```
  becomes:
  ```
  "<", "r", "o", "o", "t", ">" ...
  ```

---

## **2. Scanner (Lexical Analysis)**

- **Goal**: Convert character stream into tokens.
- **Ignored**: Whitespace outside of quoted strings.
- **Output**: Iterable stream of tokens for the parser.
- **Example**:
  ```xml
  <cat Name="Whiskers"/>
  ```
  becomes:
  ```
  SYMBOL(<) TEXT(cat) TEXT(Name) SYMBOL(=) STRING(Whiskers) SYMBOL(/>)
  ```

---

## **3. Parser (Syntax Analysis)**

- **Goal**: Create Abstract Syntax Tree (AST) from token stream.
- **Transformations**:
  - Organize the XML into a tree-like AST structure representing hierarchy and attributes.
- **Example**:
  ```xml
  <root>
    <kitten Name="Whiskers">
        </parent>
            <cat Name="The Garfield"/>
        </parent>
    </kitten>
  </root>
  ```
  becomes:
  ```json
  {
      "element_name": "root",
      "children": [
          {
              "element_name": "kitten",
              "attributes": [
                  {
                      "name": "Name",
                      "value": "Whiskers"
                  },
              ],
              "children": [
                  {
                      "element_name": "parent",
                      "attributes": [],
                      "children": [
                          {
                              "element_name": "cat",
                              "attributes": [
                                  {
                                      "name": "Name",
                                      "value": "The Garfield"
                                  },
                              ],
                              "children": [ ]
                          }
                      ]
                  }
              ]
          }
      ]
  }
  ```

---

## **4. Semantic Analyzer**

- **Goal**: Enforce rules on the AST structure.
- **Checks**:
  - Root rule: must start and end with `<root>` tags.
  - Duplicate or mixed-type lists → error
- **Transformations**:
  - Identifies classes, lists, instances
  - Assigns types to each element
- **Example**:

  ```json
  {
      "element_name": "root",
      "children": [
          {
              "element_name": "kitten",
              "attributes": [
                  {
                      "name": "Name",
                      "value": "Whiskers"
                  },
              ],
              "children": [
                  {
                      "element_name": "parent",
                      "attributes": [],
                      "children": [
                          {
                              "element_name": "cat",
                              "attributes": [
                                  {
                                      "name": "Name",
                                      "value": "The Garfield"
                                  },
                              ],
                              "children": [ ]
                          }
                      ]
                  }
              ]
          }
      ]
  }
  ```
  
  becomes:
  ```json
  {
      "types": [
          {
              "name": "Class1",
              "attributes": [
                  {
                      "name": "Name",
                      "attribute_type": "string"
                  },
                  {
                      "name": "Parent",
                      "attribute_type": "Class1"
                  }
              ]
          }
      ],
      "declarations": [
          {
              "id": "0001",
              "instance_name": "cat",
              "class_name": "Class1",
              "attributes": [
                   {
                       "name": "Name",
                       "value": "The Garfield"
                   },
                   {
                       "name": "Parent",
                       "value": null
                   }
              ]
          },
          {
              "id": "0002",
              "instance_name": "kitten",
              "class_name": "Class1",
              "attributes": [
                   {
                       "name": "Name",
                       "value": "Whiskers"
                   },
                   {
                       "name": "Parent",
                       "value": null,
                       "ref": "kitten-001"
                   }
              ]
          }
      ]
  }
  ```

Note: this may seem overblown, but this step makes the later code gen trivial. 
and yes, this is trivial later ONLY because we do hard things first but I dygress

---

## **5. Code Generator**

- **Goal**: Generate C# code representations.
- **Output**: Map of `filename` to an expected content of that file

---

## **6. Writer**

- **Goal**: Write generated code to disk.
- **Output**: None -> this step saves files to disk 
- **Location**: All files saved in `./output/` directory.

