from .get_input import get_input
from .exceptions import unexpected_character_exception, parse_exception, missing_character_exception
from .data_structures import token, token_type, location
import string

class lexer:

    def __init__(self, source: get_input):
        self.current_char = None
        self.input = source
        self.is_comment = False
        self.next_char = self.input.get_char()
        self.location = None

        self._simple_tokens = {
            "+" : token_type.ADD_OPERATOR,
            "-" : token_type.ADD_OPERATOR,
            ";" : token_type.SEMICOLON,
            "(" : token_type.OPEN_BRACKET,
            ")" : token_type.CLOSE_BRACKER,
            "{" : token_type.OPEN_BLOCK,
            "}" : token_type.CLOSE_BLOCK,
            "*" : token_type.MUL_OPERATOR,
            "/" : token_type.MUL_OPERATOR,
            "," : token_type.COMMA
        }

        self._simple_tokens_confirm = {
            "=" : token_type.ASSIGNMENT_OPERATOR,
            "<" : token_type.COMP_OPERATOR,
            ">" : token_type.COMP_OPERATOR,
            "!" : token_type.NEGATION
        }

        self._two_char_tokens = {
            "==" : token_type.COMP_OPERATOR,
            "!=" : token_type.COMP_OPERATOR,
            "<=" : token_type.COMP_OPERATOR,
            ">=" : token_type.COMP_OPERATOR,
            "||" : token_type.OR_OPERATOR,
            "&&" : token_type.AND_OPERATOR,
        }

        self._identifiers = {
            "def" : token_type.DEF,
            "if" : token_type.IF,
            "while" : token_type.WHILE,
            "else" : token_type.ELSE,
#            "elif" : token_type.ELIF,
#            "return" : token_type.RETURN,
#            "print" : token_type.PRINT,
#            "marker_up" : token_type.MARKER_UP,
#            "marker_down" : token_type.MARKER_DOWN,
#            "forward" : token_type.FORWARD,
#            "backward" : token_type.BACKWARD,
#            "left" : token_type.LEFT,
#            "right" : token_type.RIGHT,
#            "set_pos" : token_type.SET_POS,
#            "set_color" : token_type.SET_COLOR,
        }

    def _get_next_char(self):
        self.current_char = self.next_char
        try:
            self.next_char = self.input.get_char()
        except StopIteration:
            self.next_char = None

    def build_token(self):
        self._get_next_char()
        #ommit whitespace and comment
        while self.current_char and (self.current_char in string.whitespace or self.is_comment or self.current_char == "#"):
            if self.current_char == "#":
                self.is_comment = True
            if self.current_char == "\n":
                self.is_comment = False
            self._get_next_char()
        #detect end of file
        self.location = self.input.get_location()
        if self.current_char is None:
            return token(token_type.EOT, "\0", self.location)
        #build quote
        if self.current_char == "\"":
            return self._build_string()
        #build simple token
        elif self.current_char in self._simple_tokens:
            return token(self._simple_tokens[self.current_char], self.current_char, self.location)
        #build one-character token that needs confirmation or two character token
        elif self.current_char in self._simple_tokens_confirm:
            token_temp = self.current_char + self.next_char
            if token_temp in self._two_char_tokens:
                self._get_next_char()
                return token(self._two_char_tokens[token_temp], token_temp, self.location)
            else:
                return token(self._simple_tokens_confirm[self.current_char], self.current_char, self.location)
        #build two character token
        elif self.current_char == "!" or self.current_char == "|" or self.current_char == "&":
            token_temp = self.current_char + self.next_char
            if token_temp in self._two_char_tokens:
                self._get_next_char()
                return token(self._two_char_tokens[token_temp], token_temp, self.location)
            else:
                raise unexpected_character_exception(f"Unexpected token {token_temp} at: {self.location}")
        #build digit
        elif self.current_char.isdigit():
            return self._build_digit()
        #build identifier
        elif self.current_char.isalpha() or self.current_char == "_":
            return self._build_identifier()
        #something's wrong
        else:
            raise unexpected_character_exception(f"Unknown token at: {self.location}")

    def _build_string(self):
        value = ""
        self._get_next_char()
        if self.current_char != "\"":
            while self.current_char == "\\" or (self.current_char != "\\" and self.next_char != "\""):
                if self.current_char is None:
                    raise missing_character_exception("Missing quote")
                value += self.current_char
                self._get_next_char()
            value += self.current_char
            self._get_next_char()
        return token(token_type.STRING, value, self.location)

    def _build_digit(self):
        value = ""
        if self.current_char == "0":
            if self.next_char.isdigit():
                raise parse_exception(f"No digits allowed after 0 at: {self.location}")
            return token(token_type.CONST, int(self.current_char), self.location)
        else:
            while self.next_char and self.next_char.isdigit():
                value += self.current_char
                self._get_next_char()
            value += self.current_char
        if self.next_char == ".":
            self._get_next_char()
            value += self.current_char
            self._get_next_char()
            if not self.current_char.isdigit():
                raise parse_exception(f"Expected digit got: {self.current_char} at: {self.location}")
            while self.next_char and self.next_char.isdigit():
                value += self.current_char
                self._get_next_char()
            value += self.current_char
            return token(token_type.CONST, float(value), self.location)
        return token(token_type.CONST, int(value), self.location)

    def _build_identifier(self):
        value = ""
        while self.next_char and (self.next_char.isalpha() or self.next_char == "_"):
            value += self.current_char
            self._get_next_char()
        value += self.current_char
        if value in self._identifiers:
            return token(self._identifiers[value], value, self.location)
        return token(token_type.IDENTIFIER, value, self.location)
    
    def get_all_tokens(self):
        t = self.build_token()
        while t.token_type != token_type.EOT:
            yield t
            t = self.build_token()
        yield t