import pytest
from .lexer import lexer
from .parser import parser
from .get_input import get_input
from .data_structures import token, token_type, location
from .parser_types import *
from .exceptions import syntax_exception

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



if __name__ == "__main__":
    pass