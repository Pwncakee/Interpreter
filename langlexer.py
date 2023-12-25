""
Name: Akli and Aman
Project: Project 2: BYOL
Date: December 2nd, 2023
Description: This program is a parser for our language. It takes input code
converts it into Python Code and outputs a file that can be run.
"""
import re
import os

"""
    class name: Number
    Description: This class represents a number
"""
class Number:
    def __init__(self, value):
        self.value = value

"""
    class name: String
    Description: This class represents a String
"""
class String:
    def __init__(self, value):
        self.value = value

"""
    class name: Variable
    Description: This class represents a Variable
"""
class Variable:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value
"""
    class name: Assignment
    Description: This class represents an equality assignment expression
"""
class Assignment:
    def __init__(self, left, right):
        self.left = left
        self.right = right
"""
    class name: BinOp
    Description: This class represents a binary operation
"""
class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

"""
    class name: IfStatement
    Description: This class represents an if statement
"""
class IfStatement:
    def __init__(self, condition, true_statements, false_statements=None):
        self.condition = condition
        self.true_statements = true_statements
        self.false_statements = false_statements
"""
    class name: FunctionDefintion
    Description: This class represents a function definition
"""
class FunctionDefinition:
    def __init__(self, name, parameters, body_statements):
        self.name = name
        self.parameters = parameters
        self.body_statements = body_statements

"""
    class name: WhileLoop
    Description: This class represents a While Loop
"""
class WhileLoop:
    def __init__(self, condition, body_statements):
        self.condition = condition
        self.body_statements = body_statements
"""
    class name: ForLoop
    Description: This class represents a for loop
"""
class ForLoop:
    def __init__(self, init_expr, condition, update_expr, body_statements):
        self.init_expr = init_expr
        self.condition = condition
        self.update_expr = update_expr
        self.body_statements = body_statements
"""
    class name: variableAssignment
    Description: This class represents a variable assingment expression
"""
class VariableAssignment:
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression
        

    def to_python(self):
        return f"{self.variable} = {self.expression.to_python()}"
"""
    class name: ReturnStatement
    Description: This class represents a Return Statement
"""
class ReturnStatement:
    def __init__(self, expression):
        self.expression = expression
"""
    class name: ClassDefintion
    Description: This class represents a class
"""
class ClassDefinition:
    def __init__(self, name, members):
        self.name = name
        self.members = members
"""
    class name: ClassMember
    Description: This class represents a class member
"""
class ClassMember:
    def __init__(self, name, value):
        self.name = name
        self.value = value
"""
    class name: FunctionCall
    Description: This class represents a function call
"""
class FunctionCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
"""
    class name: TryCatchStatement
    Description: This class represents a try catch statement
"""       
class TryCatchStatement:
    def __init__(self, try_statements, exception_type, catch_statements):
        self.try_statements = try_statements
        self.exception_type = exception_type
        self.catch_statements = catch_statements
"""
    class name: ImportStatement
    Description: This class represents an import statement
"""
class ImportStatement:
    def __init__(self, module_name):
        self.module_name = module_name

"""
    class name: ArrayDefinition
    Description: This class represents an array
"""
class ArrayDefinition:
    def __init__(self, element_type, identifier, size):
        self.element_type = element_type
        self.identifier = identifier
        self.size = size
"""
    class name: BreakStatement
    Description: This class represents a break statement
"""
class BreakStatement:
    pass
"""
    class name: ContinueStatement
    Description: This class represents a continue statement
"""
class ContinueStatement:
    pass
"""
    class name: ForEachLoop
    Description: This class represents a for each loop
"""
class ForEachLoop:
    def __init__(self, variable, iterable, body_statements):
        self.variable = variable
        self.iterable = iterable
        self.body_statements = body_statements

"""
    class name: ThrowStatement
    Description: This class represents a throw statement
"""
class ThrowStatement:
    def __init__(self, expression):
        self.expression = expression
"""
    class name: InterfaceDefinition
    Description: This class represents an interface
"""
class InterfaceDefinition:
    def __init__(self, name, members):
        self.name = name
        self.members = members


"""
    class name: InterfaceMember
    Description: This class represents an interface member
"""
class InterfaceMember:
    def __init__(self, name, parameters, body_statements):
        self.name = name
        self.parameters = parameters
        self.body_statements = body_statements

"""
Class Name: Lexer
init variable: input_text -> the text to be converted
Description: This lexer tokenizes the input so that it can be parsed
"""
class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.current_position = 0
        self.current_char = self.input_text[self.current_position]
    
    def error(self, message):
        raise Exception(f"Lexer error: {message}")
    
    def advance(self):
        self.current_position += 1
        if self.current_position < len(self.input_text):
            self.current_char = self.input_text[self.current_position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def parse_digit(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def parse_letter(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.parse_digit()
            
            if self.current_char.isalpha():
                return self.parse_letter()

            if self.current_char == '"':
                self.advance()  
                string_value = ''
                while self.current_char != '"':
                    string_value += self.current_char
                    self.advance()
                self.advance()  
                return string_value

            if self.current_char in ('+', '-', '*', '/', '<', '>'):
                token_value = self.current_char
                self.advance()
                return token_value

            if self.current_char == '(':
                self.advance()
                return '('

            if self.current_char == ')':
                self.advance()
                return ')'

            if self.current_char == ';':
                self.advance()
                return ';'

            if self.current_char == ',':
                self.advance()
                return ','
            if self.current_char == '=':
                self.advance()
                return '='

            self.advance()
            

        return None
