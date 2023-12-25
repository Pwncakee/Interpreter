"""
Name: Akli and Aman
Project: Project 2: BYOL
Date: December 2nd, 2023
Description: This program is a parser for our language. It takes input code
converts it into Python Code and outputs a file that can be run.
"""
import os
import re
from langlexer import *

"""
    class name: Parser
    Description: This is the Parser. It takes in a lexer and begins to parse all of the
    statements in the input code passed through the lexer
"""
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.statements = []
        self.types = ['string', 'bool', 'int','float','var', 'null'] 
        self.stored_variables = {}
        self.code_for_file = []
        self.operations = ['+', '-', '*', '/']
        self.function_name = ""


    def make_file(self, input_code, file_name):
        output_file = open(file_name, "x")
        code = input_code
        statements = code
    
        for statement in statements:
            if(statement != ''):
                print("STATEMENT = " +statement)
                if("def" in statement):
                    output_file.write(statement + "\n")
                else:
                    output_file.write("\t" + statement + "\n")
        output_file.write(self.function_name+"()")
        output_file.close()
        print("program.py was created in: " + os.getcwd())

    def eat(self, expected_token):
        if self.current_token == expected_token:
            self.current_token = self.lexer.get_next_token()
        else:
            raise ValueError(f"Expected {expected_token}, but got {self.current_token}")

    def parse_digit(self):
        return self.lexer.parse_digit()

    def parse_letter(self):
        return self.lexer.parse_letter()

    def parse_string(self):
        token = self.current_token
        self.eat(token)
        return f'"{token}"'

    def parse_identifier(self):
        #self.current_token = self.lexer.get_next_token()
        return self.current_token

    def parse_type(self):
        token = self.current_token
        if token in ('boolean', 'int', 'float', 'string'):
            self.eat(token)
            return token
        else:
            raise ValueError(f"Expected type, but got {token}")

    def parse_operation(self):
        token = self.current_token
        if token in ('+', '-', '*', '/'):
            self.eat(token)
            return token
        else:
            raise ValueError(f"Expected operation, but got {token}")

    def parse_null_literal(self):
        token = self.current_token
        if token == 'null':
            self.eat(token)
            return token
        else:
            raise ValueError(f"Expected 'null', but got {token}")
        
    def parse_expression(self):
        token_type = type(self.current_token)

        if token_type == int:
            return self.parse_digit()
        elif token_type == str and self.current_token.isalpha():
            return self.parse_identifier()
        elif token_type == str and self.current_token[0] == '"':
            return self.parse_string()
        elif self.current_token == '(':
            self.eat('(')
            expr = self.parse_expression()
            self.current_token  = self.lexer.get_next_token()
            self.eat(')')
            return expr
        else:
            raise ValueError(f"Unexpected token in expression: {self.current_token}")
        
    def parse_unary_expression(self):
        token = self.current_token
        if token in ('not', '~'):
            op = token
            self.eat(token)
            expr = self.parse_expression()
            return f"{op}({expr})"
        else:
            return self.parse_expression()

    def parse_math_statement(self):
        #print("HEREE")
        if self.current_token == '(':
            self.eat('(')
            left = self.parse_math_statement()
        else:
            left = self.current_token
            self.eat(self.current_token)

        operation = self.parse_operation()
        #print("OPERATION = " + operation )
    
        if self.current_token == '(':
            self.eat('(')
            right = self.parse_math_statement()
        elif type(self.current_token) == int:
            right = self.current_token
            self.current_token = self.lexer.get_next_token()
        else:
            right = self.current_token
            self.current_token = self.lexer.get_next_token()

        #self.eat(')')
        #print(left)
        #print(operation)
        #print(right)
        return f"({left} {operation} {right})"

    def parse_statement(self):
        token = self.current_token
        if token == 'if':
            return self.parse_if_statement()
        elif token == 'function':
            return self.parse_function_definition()
        elif token == 'while':
            return self.parse_while_loop()
        elif token == 'for':
            return self.parse_for_loop()
        elif token == 'return':
            return self.parse_return_statement()
        elif token == 'try':
            return self.parse_try_catch_statement()
        elif token == '{':
            return self.parse_block()
        elif token == 'int':
            return self.parse_variable_assignment()
        elif token == 'var':
            return self.parse_variable_assignment()
        elif token == 'println':
            return self.parse_println()
        elif token == '}':
            return
        elif token == '***':
            return self.parse_comment() 
        else:
            raise ValueError(f"Unexpected token in statement: {token}")
    

    def parse_comment(self):
        return_val = "###"
        self.eat("***")
        while(self.current_token != '***'):
            return_val = return_val + "\n ###" + self.current_token
            self.current_token += self.lexer.get_next_token()
        print(return_val)
        self.eat('***')
        return return_val 

    def parse_println(self):
        return_val = "print" 
        self.eat("println")
        while (self.current_token != ';'):
            return_val += self.current_token
            self.current_token = self.lexer.get_next_token()
        return return_val
    
    def parse_condition(self):
        if self.current_token == '(':
            print("DELETING")
            self.eat('(')
        left_op = self.current_token
        self.current_token = self.lexer.get_next_token()
        operator = self.current_token
        self.current_token = self.lexer.get_next_token()
        right = self.current_token
        print(left_op)
        print(operator)
        print(right)
        #self.eat(left_op)
        #self.eat(operator)
        self.eat(right)
        #print(f"({left_op} {operator} {right})")
        if self.current_token == ')':
            print("DELETINGF")
            self.eat(")")
        return f"({left_op} {operator} {right})"

    def parse_if_statement(self):
        self.eat('if')
        print(self.current_token)
        condition = self.parse_condition()
        #self.eat('{')
        true_statements = self.parse_statements()
        print("TRUE STATEMENTS: ")
        true_join = '\n'.join(true_statements)
        for i in range(0, len(true_statements)-1):
            true_statements[i] = "\t"+ true_statements[i]
        print(true_statements)
        #self.eat('print')
        if self.current_token == '}':
            self.eat('}')
        if self.current_token == 'else':
            self.eat('else')
            self.eat('{')
            false_statements = self.parse_statements()
            self.eat('}')
            return f"if {condition}:\n\t{{ {true_statements} }} \nelse:\n\t{{ {false_statements} }}"
        else:
            return f"if {condition}:\n\t{true_join }"

    def parse_statements(self):
        statements = []
        while self.current_token is not None:
            statement = self.parse_statement()
            #print("CURRENT STATEMENT : "+statement )
            if statement is not None:
                statements.append(statement)

            if self.current_token == ';':
                self.eat(';')
            else:
                #print(self.current_token)
                break  # Exit the loop when encountering a statement without a semicolon
        
        self.statements += statements
        #print(statements)
        return statements

    def parse_function_definition(self):
        self.eat('function')
        self.function_name = self.current_token
        self.current_token = self.lexer.get_next_token()
        self.eat('(')
        parameters = self.parse_parameter_list()
        self.eat(')')
        sec = self.parse_statements()
        sec_join = ' \n'.join(map(str, sec))
        #print(sec_join)
        total = f"def {self.function_name}({parameters}: \n{(sec_join)}"
        #print(total)
        return total

    def parse_parameter_list(self):
        parameters = [self.parse_identifier()]
        while self.current_token == ',':
            self.eat(',')
            parameters.append(self.parse_identifier())
        return ', '.join(parameters)

    def parse_while_loop(self):
        self.eat('while')
        condition = self.parse_condition()
        #self.eat('{')
        statements = self.parse_statements()
        statements_join = '\n'.join(statements)
        #self.eat('}')
        return f"while ({condition}):\n\t{statements_join} "

    def parse_for_loop(self):
        self.eat('for')
        self.eat('(')
        init_expr = self.parse_expression()
        self.eat(';')
        condition = self.parse_expression()
        self.eat(';')
        update_expr = self.parse_expression()
        self.eat(')')
        self.eat('{')
        statements = self.parse_statements()
        self.eat('}')
        return f"for ({init_expr}; {condition}; {update_expr}) {{ {statements} }}"

    def parse_switch_statement(self):
        self.eat('switch')
        self.eat('(')
        switch_expr = self.parse_expression()
        self.eat(')')
        self.eat('{')
        case_clauses = self.parse_case_clauses()
        default_statements = ''
        if self.current_token == 'default':
            self.eat('default')
            self.eat(':')
            default_statements = self.parse_statements()
        self.eat('}')
        return f"switch ({switch_expr}) {{ {case_clauses} default: {default_statements} }}"
    
    def parse_case_clauses(self):
        case_clauses = ''
        while self.current_token == 'case':
            self.eat('case')
            case_expr = self.parse_expression()
            self.eat(':')
            statements = self.parse_statements()
            case_clauses += f"case {case_expr}: {statements}"
        return case_clauses
    
    def parse_try_catch_statement(self):
        self.eat('try')
        self.eat('{')
        try_statements = self.parse_statements()
        self.eat('}')
        self.eat('catch')
        self.eat('(')
        exception_type = self.parse_identifier()
        self.eat(')')
        self.eat('{')
        catch_statements = self.parse_statements()
        self.eat('}')
        return f"try {{ {try_statements} }} catch ({exception_type}) {{ {catch_statements} }}"

    def parse_type(self):
        type = self.current_token
        #print(type)
        if type in self.types: 
            return type
        else :
            raise ValueError(f"ERROR: Expected a keyword GOT A {type}")
        
    def get_variable_value(self, variable):
        if variable in self.stored_variables.keys():
            return self.stored_variables[variable].value
        else:
            raise ValueError(f"NO {variable} found in VARIABLES ")

    def parse_variable_assignment(self):
    # Parse keyword or variable type
        typeOf = self.parse_type()
        self.eat(self.current_token)
        #print('TYPE: '+ typeOf)

    # Parse variable name
        variable = self.current_token
        self.eat(self.current_token)
        #print('VAR NAME: ' +variable)

        #print(self.current_token)
    # Verify the assignment operator
        self.eat('=')
    
    # Initialize expression
        expression = None
    
    # Parse expression based on the keyword or type
        if typeOf == self.types[2] or typeOf == self.types[3]:        # TYPE 2 is int and TYPE 3 is float
            #print("CC = "+str(self.current_token))
            if self.current_token == '(':
                self.eat('(')
                expression = self.parse_math_statement()
            elif type(self.current_token) == int:
                expression = self.current_token
                self.eat(self.current_token)
            
            elif type(self.current_token) == str and self.current_token.isalpha():
                #print("HERE for var" + self.current_token)
                current_token = self.current_token
                #self.current_token = self.lexer.get_next_token()
                #print("NEXT TOKEN = "+ self.current_token)
                expression = self.parse_math_statement()
                #expression = self.get_variable_value(self.current_token)
        elif typeOf == self.types[0]: #TYPE 0 is string
            expression = self.parse_string()
        elif typeOf == self.types[1]:
            expression = self.parse_bool() # TYPE 1 is bool
        else:
        # Additional checks based on existing variables or types can be added here
            raise ValueError(f"Unexpected type in variable assignment: {typeOf}")
    
    # Update the variable assignment in the stored variables dictionary
        self.stored_variables[variable] = Variable(variable, type, expression)
        #print("DONE ONCE")
        return f"{variable} = {expression}"


    def parse_return_statement(self):
        self.eat('return')
        expression = self.parse_expression()
        #print("Final token", self.current_token)
        self.eat(self.current_token)
        self.eat(';')
        return f"return {expression}"

    def parse_block(self):
        self.eat('{')
        statements = self.parse_statements()
        if self.current_token == '}':
            self.eat('}')
        return f"{{ {statements} }}"
    
    def parse_class_definition(self):
        self.eat('class')
        class_name = self.parse_identifier()
        self.eat('{')
        class_body = self.parse_class_body()
        self.eat('}')
        return f"class {class_name} {{ {class_body} }}"

    def parse_class_body(self):
        class_members = []
        while self.current_token != '}':
            class_members.append(self.parse_class_member())
        return ' '.join(class_members)

    def parse_class_member(self):
        token = self.current_token
        if token == 'function':
            return self.parse_function_definition()
        elif token.isalpha():
            return self.parse_variable_definition()
        else:
            raise ValueError(f"Unexpected token in class member: {token}")

    def parse_new_object_creation(self):
        self.eat('new')
        class_name = self.parse_identifier()
        self.eat('(')
        self.eat(')')
        return f"new {class_name}()"

    def parse_interface_definition(self):
        self.eat('interface')
        interface_name = self.parse_identifier()
        self.eat('{')
        interface_body = self.parse_interface_body()
        self.eat('}')
        return f"interface {interface_name} {{ {interface_body} }}"

    def parse_interface_body(self):
        interface_members = []
        while self.current_token != '}':
            interface_members.append(self.parse_interface_member())
        return ' '.join(interface_members)

    def parse_interface_member(self):
        return self.parse_function_definition()

    def parse_property_definition(self):
        prop_type = self.parse_type()
        prop_name = self.parse_identifier()
        self.eat('{')
        get_accessor = self.parse_get_accessor()
        set_accessor = self.parse_set_accessor()
        self.eat('}')
        return f"{prop_type} {prop_name} {{ {get_accessor} {set_accessor} }}"
        
    def parse_dictionary(self):
        self.eat('{')
        key_value_pairs = self.parse_key_value_pairs()
        self.eat('}')
        return key_value_pairs

    def parse_key_value_pairs(self):
        key_value_pairs = []
        key = self.parse_expression()
        self.eat(':')
        value = self.parse_expression()
        key_value_pairs.append((key, value))

        while self.current_token == ',':
            self.eat(',')
            key = self.parse_expression()
            self.eat(':')
            value = self.parse_expression()
            key_value_pairs.append((key, value))

        return dict(key_value_pairs)

    def parse_tuple(self):
        self.eat('(')
        expressions = self.parse_expression_list()
        self.eat(')')
        return tuple(expressions)

    def parse_expression_list(self):
        expressions = [self.parse_expression()]
        while self.current_token == ',':
            self.eat(',')
            expressions.append(self.parse_expression())
        return expressions
    def parse_get_accessor(self):
        self.eat('get')
        self.eat('{')
        statements = self.parse_statements()
        self.eat('}')
        return f"get {{ {statements} }}"

    def parse_set_accessor(self):
        self.eat('set')
        self.eat('{')
        statements = self.parse_statements()
        self.eat('}')
        return f"set {{ {statements} }}"
