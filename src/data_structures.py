from enum import Enum, auto

class token_type(Enum):
    IF = auto()
    WHILE = auto()
    ELSE = auto()
    #ELIF = auto()
    DEF = auto()
#    RETURN = auto()
#    PRINT = auto()
#    MARKER_UP = auto()
#    MARKER_DOWN = auto()
#    FORWARD = auto()
#    BACKWARD = auto()
#    LEFT = auto()
#    RIGHT = auto()
#    SET_POS = auto()
#    SET_COLOR = auto()
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

class token:
    def __init__(self, token_type, value, location):
        self.token_type = token_type
        self.value = value
        self.location = location