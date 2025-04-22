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

