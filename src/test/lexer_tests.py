import pytest
import sys
sys.path.append('./src/')
sys.path.append('.')
from src.lexer import lexer
from src.get_input import get_input
from src.data_structures import token_type

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

#checks whether get_source class works as intended
def test_get_source():
    s = string_buffer("ala ma kota!\n")
    assert s.get_char() == "a"
    assert s.get_char() == "l"
    assert s.get_char() == "a"
    assert s.get_char() == " "
    assert s.get_char() == "m"
    assert s.get_char() == "a"
    assert s.get_char() == " "
    assert s.get_char() == "k"
    assert s.get_char() == "o"
    assert s.get_char() == "t"
    assert s.get_char() == "a"
    assert s.get_char() == "!"
    assert s.get_char() == "\n"

def test_build_simple_tokens():
    s = string_buffer("}{();")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BLOCK
    assert t.location == 0
    assert t.value == "}"
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BLOCK
    assert t.location == 1
    assert t.value == "{"
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BRACKET
    assert t.location == 2
    assert t.value == "("
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BRACKER
    assert t.location == 3
    assert t.value == ")"
    t = l.build_token()
    assert t.token_type == token_type.SEMICOLON
    assert t.location == 4
    assert t.value == ";"

#checks whether whitespaces are ommited 
def test_whitespace():
    s = string_buffer(" }\t{    (\n) ;    ")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BLOCK
    assert t.location == 1
    assert t.value == "}"
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BLOCK
    assert t.location == 3
    assert t.value == "{"
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BRACKET
    assert t.location == 8
    assert t.value == "("
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BRACKER
    assert t.location == 10
    assert t.value == ")"
    t = l.build_token()
    assert t.token_type == token_type.SEMICOLON
    assert t.location == 12
    assert t.value == ";"

#checks whether comments are ommited
def test_is_comment():
    s = string_buffer(" }\t{(\n)#;\n;    ")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BLOCK
    assert t.location == 1
    assert t.value == "}"
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BLOCK
    assert t.location == 3
    assert t.value == "{"
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BRACKET
    assert t.location == 4
    assert t.value == "("
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BRACKER
    assert t.location == 6
    assert t.value == ")"
    t = l.build_token()
    assert t.token_type == token_type.SEMICOLON
    assert t.location == 10
    assert t.value == ";"

def test_build_quote():
    s = string_buffer(" }\t{(\n)#;\"\"\n;\";aujsyhdgasu#y\"    ")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BLOCK
    assert t.location == 1
    assert t.value == "}"
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BLOCK
    assert t.location == 3
    assert t.value == "{"
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BRACKET
    assert t.location == 4
    assert t.value == "("
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BRACKER
    assert t.location == 6
    assert t.value == ")"
    t = l.build_token()
    assert t.token_type == token_type.SEMICOLON
    assert t.location == 12
    assert t.value == ";"
    t = l.build_token()
    assert t.token_type == token_type.STRING
    assert t.location == 13
    assert t.value == ";aujsyhdgasu#y"

def test_build_two_character_token():
    s = string_buffer("!=||&&")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.COMP_OPERATOR
    assert t.location == 0
    assert t.value == "!="
    t = l.build_token()
    assert t.token_type == token_type.OR_OPERATOR
    assert t.location == 2
    assert t.value == "||"
    t = l.build_token()
    assert t.token_type == token_type.AND_OPERATOR
    assert t.location == 4
    assert t.value == "&&"

def test_simple_character_token_confirm():
    s = string_buffer("<=<>=><===")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.COMP_OPERATOR
    assert t.location == 0
    assert t.value == "<="
    t = l.build_token()
    assert t.token_type == token_type.COMP_OPERATOR
    assert t.location == 2
    assert t.value == "<"
    t = l.build_token()
    assert t.token_type == token_type.COMP_OPERATOR
    assert t.location == 3
    assert t.value == ">="
    t = l.build_token()
    assert t.token_type == token_type.COMP_OPERATOR
    assert t.location == 5
    assert t.value == ">"
    t = l.build_token()
    assert t.token_type == token_type.COMP_OPERATOR
    assert t.location == 6
    assert t.value == "<="
    t = l.build_token()
    assert t.token_type == token_type.COMP_OPERATOR
    assert t.location == 8
    assert t.value == "=="

def test_quote_escape():
    s = string_buffer(" }\t{(\n)#;\"\"\n;\";aujsyh\\\"dgasu#y\"    ")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BLOCK
    assert t.location == 1
    assert t.value == "}"
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BLOCK
    assert t.location == 3
    assert t.value == "{"
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BRACKET
    assert t.location == 4
    assert t.value == "("
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BRACKER
    assert t.location == 6
    assert t.value == ")"
    t = l.build_token()
    assert t.token_type == token_type.SEMICOLON
    assert t.location == 12
    assert t.value == ";"
    t = l.build_token()
    assert t.token_type == token_type.STRING
    assert t.location == 13
    assert t.value == ";aujsyh\\\"dgasu#y"
    

def test_multi_line_comment():
    s = string_buffer("#\n#\n}")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.CLOSE_BLOCK
    assert t.location == 4
    assert t.value == "}"

def test_eot_token():
    s = string_buffer("{")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.OPEN_BLOCK
    assert t.location == 0
    assert t.value == "{"
    t = l.build_token()
    assert t.token_type == token_type.EOT
    assert t.location == 0
    assert t.value == "\0"

def test_digit():
    s = string_buffer("12312431 23.74623")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.CONST
    assert t.location == 0
    assert t.value == 12312431
    t = l.build_token()
    assert t.token_type == token_type.CONST
    assert t.location == 9
    assert t.value == 23.74623

def test_identifier():
    s = string_buffer("_ala_ma_kota _ala_ma_kota")
    l = lexer(s)
    t = l.build_token()
    assert t.token_type == token_type.IDENTIFIER
    assert t.location == 0
    assert t.value == "_ala_ma_kota"
    t = l.build_token()
    assert t.token_type == token_type.IDENTIFIER
    assert t.location == 13
    assert t.value == "_ala_ma_kota"

def test_whole_text():
    s = string_buffer(
"""def square(x) {
  i = 0;
  while(i<=3) {
    forward(x);
    right(90);
    i=i+1;
  }
  return x * x;
}

i = 0;
while(square(i) <= 100) {
    if(i > 5) {
        print("area of your square is more than 25");
    } else {
        print("area of your square is less than 25");
    }
    i = i + 1;
}
print("Done")
""")
    l = lexer(s)
    t = None
    tokens = list()
    for token in l.get_all_tokens():
        tokens.append(token)
    for token in tokens:
        print(token.value, "\t\t",token.token_type)

if __name__ == "__main__":
    test_build_simple_tokens()
    test_is_comment()
    test_build_quote()
    test_simple_character_token_confirm()
    test_build_two_character_token()
    test_quote_escape()
    test_multi_line_comment()
    test_eot_token()
    test_digit()
    test_identifier()
    test_whole_text()