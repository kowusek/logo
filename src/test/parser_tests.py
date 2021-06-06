import pytest
import sys
sys.path.append('./src/')
sys.path.append('.')
from src.lexer import lexer
from src.parser import parser
from src.get_input import get_input
from src.data_structures import token, token_type, location
from src.parser_types import *
from src.exceptions import syntax_exception

class string_buffer(get_input):
    def __init__(self, string):
        self.input = string
        self.g = self.next_char_generator()
        self.location = -1

    def next_char_generator(self):
        for char in self.input:
            yield char
            self.location += 1

    def get_char(self):
        try:
            temp = next(self.g)
        except StopIteration:
            temp = None
        return temp

    def get_location(self):
        return self.location

#checks whether tests are working
def test_test():
    assert True

def test_build_simple_assignment():
    s = string_buffer("x=1;")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.statements[0].identifier == "x"
    assert program.statements[0].expression.value == 1

def test_build_assignment():
    s = string_buffer("x=1+2*3;")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.statements[0].identifier == "x"
    assert program.statements[0].expression.value_list[0].value == 1
    assert program.statements[0].expression.value_list[0].sign == None
    assert program.statements[0].expression.operator_list[0].value == "+"
    assert program.statements[0].expression.value_list[1].value_list[0].value == 2
    assert program.statements[0].expression.value_list[1].value_list[0].sign == None
    assert program.statements[0].expression.value_list[1].operator_list[0].value == "*"
    assert program.statements[0].expression.value_list[1].value_list[1].value == 3
    assert program.statements[0].expression.value_list[1].value_list[1].sign == None

def test_build_simple_if():
    s = string_buffer("if(a){}")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.statements[0].expression.id == 'a'
    assert program.statements[0].true_block.statement_list == []

def test_build_simple_if_else():
    s = string_buffer("if(a){}else{}")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.statements[0].true_block.statement_list == []
    assert program.statements[0].false_block.statement_list == []

def test_build_if_else():
    s = string_buffer("if(a>b){x=1+2*3;}else{x=1+2*3;}")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.statements[0].expression.value_list[0].id == "a"
    assert program.statements[0].expression.operator_list[0].value == ">"
    assert program.statements[0].expression.value_list[1].id == "b"
    assert program.statements[0].true_block.statement_list != []
    assert program.statements[0].false_block.statement_list != []

def test_build_simple_while():
    s = string_buffer("while(1){}")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.statements[0].expression.value == 1
    assert program.statements[0].block.statement_list == []

def test_build_while():
    s = string_buffer("while(a>b){x=1+2*3;}")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.statements[0].expression.value_list[0].id == "a"
    assert program.statements[0].expression.operator_list[0].value == ">"
    assert program.statements[0].expression.value_list[1].id == "b"
    assert program.statements[0].block.statement_list != []

def test_build_simple_function_call():
    s = string_buffer("ala();")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.statements[0].argument_list == []
    assert program.statements[0].identifier == "ala"

def test_build_function_call():
    s = string_buffer("!ala(a, b);")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.statements[0].argument_list[0].id == "a"
    assert program.statements[0].argument_list[1].id == "b"
    assert program.statements[0].sign == "!"
    assert program.statements[0].identifier == "ala"

def test_build_simple_def():
    s = string_buffer("def ala(){}")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.definitions[0].identifier == "ala"
    assert program.definitions[0].parameter_list == []
    assert program.definitions[0].block.statement_list == []

def test_build_def_no_block():
    s = string_buffer("def ala(x, y){}")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.definitions[0].identifier == "ala"
    assert program.definitions[0].parameter_list[0].id == "x"
    assert program.definitions[0].parameter_list[1].id == "y"
    assert program.definitions[0].block.statement_list == []

def test_build_def():
    s = string_buffer("def ala(x, y){x=1+2*3;x=1+2*3;}")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.definitions[0].identifier == "ala"
    assert program.definitions[0].parameter_list[0].id == "x"
    assert program.definitions[0].parameter_list[1].id == "y"
    assert program.definitions[0].block.statement_list[0].identifier == "x"
    assert program.definitions[0].block.statement_list[0].expression.value_list[0].value == 1
    assert program.definitions[0].block.statement_list[0].expression.value_list[0].sign == None
    assert program.definitions[0].block.statement_list[0].expression.operator_list[0].value == "+"
    assert program.definitions[0].block.statement_list[0].expression.value_list[1].value_list[0].value == 2
    assert program.definitions[0].block.statement_list[0].expression.value_list[1].value_list[0].sign == None
    assert program.definitions[0].block.statement_list[0].expression.value_list[1].operator_list[0].value == "*"
    assert program.definitions[0].block.statement_list[0].expression.value_list[1].value_list[1].value == 3
    assert program.definitions[0].block.statement_list[0].expression.value_list[1].value_list[1].sign == None
    assert program.definitions[0].block.statement_list[1].identifier == "x"
    assert program.definitions[0].block.statement_list[1].expression.value_list[0].value == 1
    assert program.definitions[0].block.statement_list[1].expression.value_list[0].sign == None
    assert program.definitions[0].block.statement_list[1].expression.operator_list[0].value == "+"
    assert program.definitions[0].block.statement_list[1].expression.value_list[1].value_list[0].value == 2
    assert program.definitions[0].block.statement_list[1].expression.value_list[1].value_list[0].sign == None
    assert program.definitions[0].block.statement_list[1].expression.value_list[1].operator_list[0].value == "*"
    assert program.definitions[0].block.statement_list[1].expression.value_list[1].value_list[1].value == 3
    assert program.definitions[0].block.statement_list[1].expression.value_list[1].value_list[1].sign == None

def test_build_2_statements():
    s = string_buffer("def ala(x, y){x=1+2*3;x=1+2*3;}ala();")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    assert program.definitions[0].identifier == "ala"
    assert program.statements[0].identifier == "ala"

if __name__ == "__main__":
    test_build_simple_assignment()
    test_build_assignment()
    test_build_simple_if()
    test_build_simple_if_else()
    test_build_if_else()
    test_build_simple_while()
    test_build_while()
    test_build_simple_function_call()
    test_build_function_call()
    test_build_simple_def()
    test_build_def_no_block()
    test_build_def()
    test_build_2_statements()