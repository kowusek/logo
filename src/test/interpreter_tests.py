import pytest
import sys
sys.path.append('./src/')
sys.path.append('.')
sys.path.append('./draw/')
from src.lexer import lexer
from src.parser import parser
from src.get_input import get_input
from src.data_structures import token, token_type, location
from src.parser_types import *
from src.exceptions import syntax_exception
from src.visitor import interpreter_visitor
from src.draw.window_renderer import *

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

def test_add_definition():
    s = string_buffer("def ala(){}")
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.definitions['ala']

def test_value_assignment():
    s = string_buffer('x=1;y="ala ma kota";')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables['x'] == 1
    assert v.current_context.variables['y'] == "ala ma kota"

def test_assign_variable_to_variable():
    s = string_buffer('x=1;y=x;')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables['x'] == 1
    assert v.current_context.variables['y'] == 1

def test_function_call():
    s = string_buffer('def ala(x, y){a = y;b = x;}ala(1, 2);')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables == {}
    
def test_special_function():
    s = string_buffer('print("ala","ma");')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)

def test_return():
    s = string_buffer('def ala(x){return(x);}print(ala(2));')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)

def test_recursion():
    s = string_buffer('def ala(x){print(x);}ala(2);')#add ala(x) to function definiton
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)

def test_value_dumping():
    s = string_buffer('def ala(x){return(x);}ala(2);ala(2);')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.return_val == []

def test_if_statement_blank():
    s = string_buffer('if(1){x=1;}else{x=2;}if(0){y=1;}else{y=2;}')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables == {}

def test_if_statement():
    s = string_buffer('x=0;y=0;if(1){x=1;}else{x=2;}if(0){y=1;}else{y=2;}')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables == {'x': 1, 'y': 2}

def test_simple_if_statement():
    s = string_buffer('x=0;y=0;if(1){x=1;}if(0){y=1;}')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables == {'x': 1, 'y': 0}

def test_simple_while_and_math_expression():
    s = string_buffer('x=5;y=0;while(x){x=x-1;y=y+1;}')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables == {'x': 0, 'y': 5}

def test_factor_and_recursion():
    s = string_buffer('def factorial(x){if(x){return(factorial(x-1)*x);}else{return(1);}}x=factorial(5);')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables == {'x': 120}

def test_expression_evaluation():
    s = string_buffer('x=2*2+3;y=2*(2+3);')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables == {'x': 7, 'y': 10}

def test_comparison():
    s = string_buffer('x=1;y=1;z=x==y;')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables['z'] == True

def test_bool():
    s = string_buffer('x=True;y=True;z=x==y;')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables['z'] == True

def test_logical_expressions():
    s = string_buffer('x=True||False;y=True&&False;z=True&&True')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    v.visit_program(program)
    assert v.current_context.variables['x'] == True
    assert v.current_context.variables['y'] == False
    assert v.current_context.variables['z'] == True

def test_snow_flake():
    t = TurtlePaths()
    r = WindowRenderer(t)
    s = string_buffer('def snowflake(lengthSide,levels){if(levels==0){forward(lengthSide);return();}lengthSide=lengthSide/3.0;snowflake(lengthSide,levels-1);left(60);snowflake(lengthSide,levels-1);right(120);snowflake(lengthSide,levels-1);left(60);snowflake(lengthSide,levels-1);}snowflake(50,5);')
    l = lexer(s)
    p = parser(l)
    program = p.parse_program() 
    v = interpreter_visitor(t)
    v.visit_program(program)
    #r.render()