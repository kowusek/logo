from src.get_input import get_input
from src.lexer import lexer
from src.parser import parser
from src.visitor import interpreter_visitor
from src.window import window
from src.marker import marker

if __name__ == "__main__":
    input = get_input('code_example.txt')
    l = lexer(input)
    p = parser(l)
    program = p.parse_program()
    m = marker()
    v = interpreter_visitor(m)
    program.accept(v)
    w = window(m.lines, m.angle)
    w.render()