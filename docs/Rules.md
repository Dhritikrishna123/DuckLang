# DuckLang Programming Language Documentation

## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Language Customization](#language-customization)
- [Basic Syntax](#basic-syntax)
- [Data Types](#data-types)
- [Control Flow](#control-flow)
- [Functions](#functions)
- [Examples](#examples)
- [Configuration Guide](#configuration-guide)
- [Error Handling](#error-handling)

## Introduction

DuckLang is a flexible, customizable programming language that allows users to define their own keywords and syntax elements through configuration. This makes it ideal for educational purposes, localization, and creating domain-specific language variants.

## Getting Started

### Running DuckLang Programs
To run a DuckLang program:

1. Save your code with the `.duck` extension (e.g., `program.duck`)
2. Open a terminal in the project directory
3. Run the following command:
```bash
python main.py your_program.duck
```

For example:
```bash
# Running a simple program
python main.py hello.duck

# Running with custom keywords (make sure .env is configured)
python main.py custom_program.duck
```

## Language Customization

### Customizable Keywords
All keywords in Duck can be customized through a `.env` file. Here are the default keywords and their customizable environment variables:

| Default Keyword | Environment Variable | Purpose |
|----------------|---------------------|---------|
| `print` | `KEYWORD_PRINT` | Output command |
| `if` | `KEYWORD_IF` | Conditional statement |
| `else` | `KEYWORD_ELSE` | Alternative condition |
| `while` | `KEYWORD_WHILE` | Loop construct |
| `for` | `KEYWORD_FOR` | Iteration construct |
| `function` | `KEYWORD_FUNCTION` | Function definition |
| `return` | `KEYWORD_RETURN` | Function return |
| `break` | `KEYWORD_BREAK` | Loop termination |
| `continue` | `KEYWORD_CONTINUE` | Skip loop iteration |
| `and` | `KEYWORD_AND` | Logical AND |
| `or` | `KEYWORD_OR` | Logical OR |
| `not` | `KEYWORD_NOT` | Logical NOT |
| `true` | `KEYWORD_TRUE` | Boolean true |
| `false` | `KEYWORD_FALSE` | Boolean false |
| `none` | `KEYWORD_NONE` | Null value |
| `var` | `KEYWORD_VAR` | Variable declaration |

### Example Configuration
```env
KEYWORD_PRINT=show
KEYWORD_IF=when
KEYWORD_ELSE=otherwise
KEYWORD_WHILE=repeat
KEYWORD_FUNCTION=def
KEYWORD_RETURN=give
```

## Basic Syntax

### Statement Separation
Statements in Duck are separated by newlines. Semicolons are not required or used as statement separators.

```python
# Correct way
var x = 5
print(x)

# Not needed (but will work)
var x = 5;
print(x);
```

### Variables
```python
# Variable declaration
var x = 5        # Default syntax
let x = 5        # With KEYWORD_VAR=let

# Variable update (no 'var' keyword needed)
x = 10          # Updating existing variable
```

### Output
```python
print("Hello")   # Default syntax
show("Hello")    # With KEYWORD_PRINT=show
```

### Comments
```python
# Single line comment
```

## Data Types

Duck supports the following data types:

### Primitive Types
- Numbers (integers and floating-point)
- Strings (text enclosed in quotes)
- Booleans (`true`/`false` or customized values)
- None (`none` or customized value)

### Complex Types
- Arrays: `[1, 2, 3]`
- Functions

### Type Examples
```python
# Numbers
var num = 42
var float_num = 3.14

# Strings
var text = "Hello, World!"

# Booleans
var flag = true    # Default
var flag = yes     # With KEYWORD_TRUE=yes

# Arrays
var numbers = [1, 2, 3, 4, 5]
```

## Control Flow

### Conditional Statements
```python
# Default syntax
if x > 0 {
    print("Positive")
} else {
    print("Non-positive")
}

# Customized syntax (with configured keywords)
when x > 0 {
    show("Positive")
} otherwise {
    show("Non-positive")
}
```

### Loops
```python
# While loop (default)
while x > 0 {
    print(x)
    x = x - 1
}

# While loop (customized)
repeat x > 0 {
    show(x)
    x = x - 1
}
```

## Functions

### Function Definition
```python
# Default syntax
function factorial(n) {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}

# Customized syntax
def factorial(n) {
    when n <= 1 {
        give 1
    }
    give n * factorial(n - 1)
}
```

### Function Calls
```python
var result = factorial(5)
```

## Examples

### Complete Program Example (Default Syntax)
```python
function factorial(n) {
    if n < 0 {
        return 0
    }
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}

var numbers = [1, 2, 3, 4, 5]
print("Computing factorials:")

for num in numbers {
    print(factorial(num))
}
```

### Same Program with Custom Keywords
```python
def factorial(n) {
    when n < 0 {
        give 0
    }
    when n <= 1 {
        give 1
    }
    give n * factorial(n - 1)
}

let numbers = [1, 2, 3, 4, 5]
show("Computing factorials:")

loop num in numbers {
    show(factorial(num))
}
```

## Configuration Guide

### Setting Up Custom Keywords

1. Create a `.env` file in your project root
2. Define your custom keywords:
```env
KEYWORD_PRINT=show
KEYWORD_IF=when
KEYWORD_ELSE=otherwise
KEYWORD_WHILE=repeat
KEYWORD_FOR=loop
KEYWORD_FUNCTION=def
KEYWORD_RETURN=give
KEYWORD_BREAK=stop
KEYWORD_CONTINUE=skip
KEYWORD_AND=also
KEYWORD_OR=either
KEYWORD_NOT=negate
KEYWORD_TRUE=yes
KEYWORD_FALSE=no
KEYWORD_NONE=nothing
KEYWORD_VAR=let
```

### Configuration Rules
- Keywords must be unique
- Keywords cannot contain spaces
- Keywords are case-insensitive
- Keywords cannot be special characters used by the language (like operators)

## Error Handling

### Common Errors

1. **Syntax Errors**
```python
when x > 0 {    # Error if KEYWORD_IF is not set to "when"
    show(x)     # Error if KEYWORD_PRINT is not set to "show"
}
```

2. **Configuration Errors**
- Duplicate keyword definitions
- Invalid keyword names
- Missing required keywords

### Error Messages
The language provides clear error messages indicating:
- Line number where the error occurred
- Expected vs. received tokens
- Configuration-related issues

### Best Practices
1. Keep a backup of your default configuration
2. Test your custom keywords thoroughly
3. Document your custom language syntax
4. Maintain consistency in keyword naming

## Development Status

The Duck programming language is under active development. Current features:
- ✓ Customizable keywords
- ✓ Basic arithmetic operations
- ✓ Control flow statements
- ✓ Functions
- ✓ Arrays
- ✓ Variable declarations

Future enhancements may include:
- Custom operator definitions
- Additional data types
- Module system
- Standard library
- More customization options

