from src.get_input import get_input
from src.lexer import lexer
from src.parser import parser
from src.visitor import interpreter_visitor

if __name__ == "__main__":
    input = get_input('code_example.txt')
    l = lexer(input)
    p = parser(l)
    program = p.parse_program()
    v = interpreter_visitor()
    program.accept(v)