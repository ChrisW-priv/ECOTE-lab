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
        <parent>
            <cat Name="The Garfield"/>
        </parent>
    </kitten>
  </root>
  ```
  becomes:
  ```json
    XmlToken(kind=startTag, name=root)
    XmlToken(kind=startTag, name=kitten, attributes=[Attribute("Name", "Whiskers"))
    XmlToken(kind=startTag, name=parent)
    XmlToken(kind=selfClosingTag, name=cat, attributes=[Attribute("Name", "The Garfield"))
    XmlToken(kind=endTag, name=parent)
    XmlToken(kind=endTag, name=kitten)
    XmlToken(kind=endTag, name=root)
  ```

  OR
  ```xml 
  <root>
    <kitten Name="Whiskers"/>
  </root>
  ```
  becomes:
  ```text 
  ElementStart(name=root)
      ElementStart(name=kitten, attributes=[Attribute("Name", "Whiskers"))
  ElementEnd(name=root)
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
  ElementStart(name=root)
      ElementStart(name=kitten, attributes=[Attribute("Name", "Whiskers"))
          ElementStart(name=parent)
              ElementStart(name=cat, attributes=[Attribute("Name", "The Garfield"))
          ElementEnd(name=parent)
      ElementEnd(name=kitten)
  ElementEnd(name=root)
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

## **5. Intermediate Code Generator**


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

---

## **6. Code Generator**

- **Goal**: Generate C# code representations.
- **Output**: Map of `filename` to an expected content of that file

---

## **7. Writer**

- **Goal**: Write generated code to disk.
- **Output**: None -> this step saves files to disk 
- **Location**: All files saved in `./output/` directory.

