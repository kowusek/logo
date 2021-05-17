from .lexer import lexer
from .data_structures import *
from .parser_types import *
from .exceptions import syntax_exception

class parser:
    def __init__(self, token_source: lexer = None):
        self.current_token = None
        self.token_source = token_source

    def __get_token(self) -> token:
        if not self.current_token:
            self.current_token = self.token_source.build_token()
        return self.current_token

    def __get_next_token(self) -> token:
        self.current_token = self.token_source.build_token()
        return self.current_token

    def parse_program(self) -> program:
        parsed_element = self.parse_element()
        if parsed_element:
            program = program()
            while parsed_element:
                program.add_element(parsed_element)
                parsed_element = self.parse_element()
            return program
        return None

    def parse_element(self) -> statement or definition:
        token = self.__get_token()
        if token.token_type == token_type.DEF:
            self.__get_next_token()
            return self.__parse_definition()
        return self.__parse_statement()

    def __parse_statement(self) -> statement:
        token = self.__get_token()
        if token.token_type == token_type.IF:
            self.__get_next_token()
            return self.__parse_if()
        elif token.token_type == token_type.WHILE:
            self.__get_next_token()
            return self.__parse_while()
        elif token.token_type == token_type.IDENTIFIER:
            if self.__get_next_token().token_type == token_type.ASSIGNMENT_OPERATOR:
                self.__get_next_token()
                return self.__parse_assignment(token)
            else:
                if self.__get_token().token_type == token_type.OPEN_BRACKET:
                    sign = self.__get_next_token()
                    if sign.value == "!":
                        temp = function(token.location, token.value, self.__parse_function(token), sign=sign)
                        if self.__get_next_token().token_type == token_type.CLOSE_BRACKER:
                            return temp
                        else:
                            raise syntax_exception("Expected closing bracket")
                    else:
                        raise syntax_exception("Expected \"!\" sign")
                else:
                    raise syntax_exception("expected opening bracket")
        raise syntax_exception("Unexpected token")

    def __parse_fun_args(self, identifier: token) -> 'list[logic_expression]':
        arguments = list()
        self.__get_next_token()
        arguments.append(self.__parse_value())
        while self.__get_token().token_type == token_type.COMMA:
            self.__get_next_token()
            arguments.append(self.__parse_value())
        return arguments

    def __parse_assignment(self, identifier: token) -> assignment:
        temp = assignment(identifier.location, identifier.value, self.__parse_logic_expression())
        if self.__get_token().token_type == token_type.SEMICOLON:
            self.__get_next_token() #skip ";"
        else: 
            raise syntax_exception("Expected semicolon")
        return temp

    def __parse_logic_expression(self) -> logic_expression:
        conditions = list()
        conditions.append(self.__parse_condition())
        while self.__get_token().token_type == token_type.OR_OPERATOR:
            self.__get_next_token()
            conditions.append(self.__parse_condition())
        return logic_expression(conditions[0].location, conditions)

    def __parse_condition(self) -> condition:
        relations = list()
        if self.__get_token().token_type == token_type.OPEN_BRACKET:
            temp = self.__parse_logic_expression()
            if self.__get_token().token_type == token_type.CLOSE_BRACKER:
                self.__get_next_token() #skip ")"
            else:
                raise syntax_exception("Expected close bracket")
            return condition(temp.location, expression=temp)
        relations.append(self.__parse_relation())
        while self.__get_token().token_type == token_type.AND_OPERATOR:
            self.__get_next_token()
            relations.append(self.__parse_relation())
        return condition(relations[0].location, relations)

    def __parse_relation(self) -> relation:
        math_expressions = list()
        signs = list()
        COMP_SIGN = ("==", "!=", "<", "<=", ">", ">=")
        math_expressions.append(self.__parse_math_expression())
        while self.__get_token().value in COMP_SIGN:
            signs.append(self.__get_token().value)
            self.__get_next_token()
            math_expressions.append(self.__parse_math_expression())
        return relation(math_expressions[0].location, math_expressions=math_expressions, operators=signs)

    def __parse_math_expression(self) -> math_expression:
        factors = list()
        signs = list()
        ADD_SIGN = ("+", "-")
        factors.append(self.__parse_factor())
        while self.__get_token().value in ADD_SIGN:
            signs.append(self.__get_token().value)
            self.__get_next_token()
            factors.append(self.__parse_factor())
        return math_expression(factors[0].location, factors=factors, operators=signs)

    def __parse_factor(self) -> factor:
        values = list()
        signs = list()
        MUL_SIGN = ("*", "/")
        if self.__get_token().token_type == token_type.OPEN_BRACKET:
            temp = self.__parse_math_expression()
            if self.__get_token().token_type == token_type.CLOSE_BRACKER:
                self.__get_next_token() #skip ")"
            else:
                raise syntax_exception("Expected close bracket")
            return factor(temp.location, expression=temp)
        values.append(self.__parse_value())
        while self.__get_token().value in MUL_SIGN:
            signs.append(self.__get_token().value)
            self.__get_next_token()
            values.append(self.__parse_value())
        return factor(values[0].location, values=values, operators=signs)

    def __parse_value(self) -> value:
        sign = None
        ADD_SIGN = ("!", "+", "-")
        if self.__get_token().value in ADD_SIGN:
            sign = self.__get_token()
            self.__get_next_token()
        if self.__get_token().token_type == token_type.IDENTIFIER:
            token = self.__get_token()
            if self.__get_next_token().token_type == token_type.OPEN_BRACKET:
                args = self.__parse_fun_args()
                return function(sign.location, token.value, args, sign)
            else:
                return identifier(token.location, token.value, sign)
        if self.__get_token().token_type == token_type.CONST:
            temp = self.__get_token()
            temp_number = number(temp.location, temp.value, sign)
            self.__get_next_token()
            return temp_number
        if self.__get_token().token_type == token_type.STRING:
            temp = self.__get_token()
            temp_string = string(temp.location, temp.value, sign)
            self.__get_next_token()
            return temp_string
        else:
            raise une

    def __parse_definition(self) -> function_definition:
        if self.__get_token().token_type != token_type.DEF:
            return None

        identifier = self.__get_next_token()
        if identifier.token_type != token_type.IDENTIFIER:
            raise syntax_exception("Expected dunction identifier")

        if self.__get_next_token() != token_type.OPEN_BRACKET:
            raise syntax_exception("Missing opening bracket in argument list")

        self.__get_next_token()
        argument_list = []

        # parse arguments
        if self.current_token.token_type == token_type.IDENTIFIER:
            argument_list.append(self.current_token.value)
        else:
            raise syntax_exception("Expected argument identifier")

        while self.__get_next_token().token_type == token_type.COMMA:
            if self.__get_next_token().token_type != token_type.IDENTIFIER:
                raise syntax_exception("Wrong function argument")
            argument_list.append(self.__get_next_token().value)

        if self.__get_next_token().token_type != token_type.CLOSE_BRACKER:
            raise syntax_exception("Missing closing bracket in argument list")

        self.__get_next_token()
        block = self.__parse_block()

        return function_definition(identifier.location, identifier.value, block, argument_list)

    def __parse_block(self) -> block:
        if self.__get_token().token_type != token_type.OPEN_BLOCK:
            raise syntax_exception("Missing block opening in block declaration")

        statement_list = []
        self.__get_next_token()
        statement = self.__parse_statement()
        while statement:
            statement_list.append(statement)
            statement = self.__parse_statement()

        if self.current_token.token_type != token_type.CLOSE_BLOCK:
            raise syntax_exception("Missing block closing in block declaration")

        self.__get_next_token()
        return block(statement_list)