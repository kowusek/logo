from enum import Enum, auto

class token_type(Enum):
    IF = auto()
    WHILE = auto()
    ELSE = auto()
    DEF = auto()
    NEGATION = auto()
    ADD_OPERATOR = auto()
    MUL_OPERATOR = auto()
    ASSIGNMENT_OPERATOR = auto()
    COMP_OPERATOR = auto()
    OR_OPERATOR = auto()
    AND_OPERATOR = auto()
    SEMICOLON = auto()
    STRING = auto()
    OPEN_BRACKET = auto()
    CLOSE_BRACKER = auto()
    OPEN_BLOCK = auto()
    CLOSE_BLOCK = auto()
    IDENTIFIER = auto()
    CONST = auto()
    EOT = auto()
    COMMA = auto()

class location:
    def __init__(self, line, char_number):
        self.line = line
        self.char_number = char_number
    
    def __str__(self) -> str:
        return f'line: {self.line}, position: {self.char_number}'

class token:
    def __init__(self, token_type, value, location):
        self.token_type = token_type
        self.value = value
        self.location = location