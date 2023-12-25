"""
Name: Akli and Aman
Project: Project 2: BYOL
Date: December 2nd, 2023
Description: This program is a parser for our language. It takes input code
converts it into Python Code and outputs a file that can be run.
"""
from langlexer import *
from langparser import *

input_code1 = open("sample1_valid.txt").read()
input_code2 = open("sample2_valid.txt").read()
input_code3 = open("sample3_valid.txt").read()
input_code4 = open("sample1_invalid.txt").read()
input_code5 = open("sample2_invalid.txt").read()
input_code6 = open("sample3_invalid.txt").read()

codes = [input_code1, input_code2, input_code3, input_code4, input_code5, input_code6]

file_id = 1
for i in codes:
    lexer = Lexer(i)
    parser = Parser(lexer)
    ast = None
    try:
        ast = parser.parse_statements()
    except:
        print(f"File {file_id} syntax error: Could not Resolve")
        continue
    # You might need to adjust this based on your actual usage
    parser.make_file(ast[0].split("\n"), f"file{file_id}.py")
    file_id += 1
