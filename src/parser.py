from __future__ import annotations
from src.parser_types import *
from src.lexer import lexer
from src.data_structures import *
from src.exceptions import syntax_exception

class parser:
    def __init__(self, token_source: lexer):
        self.token_source = token_source
        self.current_token = self.token_source.build_token()

    def __get_next_token(self) -> token:
        self.current_token = self.token_source.build_token()
        return self.current_token
    
    def parse_program(self) -> program:
        definitions = list()
        statements = list()
        while self.current_token.token_type != token_type.EOT:
            if d := self.__parse_definition():
                definitions.append(d)
            elif s := self.__parse_statement():
                statements.append(s)
            else:
                raise syntax_exception("Expected statement or a function definition", loc = self.current_token.location)
        return program(definitions=definitions,statements=statements)

    def __parse_definition(self) -> definition:
        if self.current_token.token_type == token_type.DEF:
            if self.__get_next_token().token_type == token_type.IDENTIFIER:
                name = self.current_token
                self.__get_next_token()
                if (p := self.__parse_arguments()) != None:
                    if (b := self.__parse_block()) != None:
                        return definition(name.location, name.value, b, p)
                    else:
                        raise syntax_exception("Expected block", loc = self.current_token.location)
                else:
                    raise syntax_exception("Expected function parameters", loc = self.current_token.location)
            else:
                raise syntax_exception("Expected function identifier" ,loc = self.current_token.location)
        else:
            return None

    def __parse_statement(self) -> statement:
        sign = None
        if (i := self.__parse_if()) != None:
            #self.__get_next_token() # skip semicolon
            return i
        elif w := self.__parse_while():
            self.__get_next_token() # skip semicolon
            return w
        elif self.current_token.token_type == token_type.NEGATION:
            sign = "!"
            self.__get_next_token()
        if self.current_token.token_type == token_type.IDENTIFIER:
            name = self.current_token
            self.__get_next_token()
            if not sign:
                if a := self.__parse_assignment(name):
                    self.__get_next_token() # skip semicolon
                    return a
            if (f := self.__parse_function_call(name, sign)) != None:
                if self.current_token.token_type == token_type.SEMICOLON:
                    self.__get_next_token() # skip semicolon
                    return f
                else:
                    raise syntax_exception("Expected semicolon", loc = self.current_token.location)
            else:
                raise syntax_exception("Expected assignment or function call", loc = self.current_token.location)
        else:
            return None

    def __parse_parameters(self) -> list[value]:
        params = list()
        if self.current_token.token_type == token_type.OPEN_BRACKET:
            self.__get_next_token()
            if self.current_token.token_type == token_type.CLOSE_BRACKER:
                self.__get_next_token()
                return []
            elif v := self.__parse_logic_expression():
                params.append(v)
                while self.current_token.token_type == token_type.COMMA:
                    self.__get_next_token()
                    if v := self.__parse_logic_expression():
                        params.append(v)
                    else:
                        raise syntax_exception("Expected function parameter", loc = self.current_token.location)
                if self.current_token.token_type == token_type.CLOSE_BRACKER:
                    self.__get_next_token()
                    return params
                else:
                    raise syntax_exception("Expected closing bracket", loc = self.current_token.location)
            else:
                raise syntax_exception("Expected function parameter", loc = self.current_token.location)
        else:
            return None

    def __parse_arguments(self) -> list[value]:
        params = list()
        if self.current_token.token_type == token_type.OPEN_BRACKET:
            self.__get_next_token()
            if self.current_token.token_type == token_type.CLOSE_BRACKER:
                self.__get_next_token()
                return []
            elif self.current_token.token_type == token_type.IDENTIFIER:
                v = identifier(self.current_token.location, self.current_token.value)
                self.__get_next_token()
                params.append(v)
                while self.current_token.token_type == token_type.COMMA:
                    self.__get_next_token()
                    if self.current_token.token_type == token_type.IDENTIFIER:
                        v = identifier(self.current_token.location, self.current_token.value)
                        self.__get_next_token()
                        params.append(v)
                    else:
                        raise syntax_exception("Expected function argument", loc = self.current_token.location)
                if self.current_token.token_type == token_type.CLOSE_BRACKER:
                    self.__get_next_token()
                    return params
                else:
                    raise syntax_exception("Expected closing bracket", loc = self.current_token.location)
            else:
                raise syntax_exception("Expected function parameter", loc = self.current_token.location)
        else:
            return None

    def __parse_block(self) -> block:
        statements = list()
        location = self.current_token.location
        if self.current_token.token_type == token_type.OPEN_BLOCK:
            if self.__get_next_token().token_type == token_type.CLOSE_BLOCK:
                self.__get_next_token()
                return block(location, [])
            elif s := self.__parse_statement():
                statements.append(s)
                while s := self.__parse_statement():
                    statements.append(s)
                if self.current_token.token_type == token_type.CLOSE_BLOCK:
                    self.__get_next_token()
                    return block(location, statements)
                else:
                    raise syntax_exception("Expected closing block", loc = self.current_token.location)    
                #self.__get_next_token()
                #return block(location, statements)
            else:
                raise syntax_exception("Expected statement", loc = self.current_token.location)    
        else:
            return None

    def __parse_if(self) -> if_statement:
        if self.current_token.token_type == token_type.IF:
            if self.__get_next_token().token_type == token_type.OPEN_BRACKET:
                self.__get_next_token()
                if (l := self.__parse_logic_expression()) != None:
                    if self.current_token.token_type == token_type.CLOSE_BRACKER:
                        self.__get_next_token()
                        if (t := self.__parse_block()) != None:
                            if self.current_token.token_type == token_type.ELSE:
                                self.__get_next_token()
                                if (f := self.__parse_block()) != None:
                                    return if_statement(self.current_token.location, l, t, f)
                                else:
                                    raise syntax_exception("Expected block", loc = self.current_token.location)    
                            else:
                                return if_statement(self.current_token.location, l, t)
                        else:
                            raise syntax_exception("Expected block", loc = self.current_token.location)    
                    else:
                        raise syntax_exception("Expected closing bracket", loc = self.current_token.location)    
                else:
                    raise syntax_exception("Expected logic expression", loc = self.current_token.location)    
            else:
                raise syntax_exception("Expected opening bracket", loc = self.current_token.location)    
        else:
            return None

    def __parse_while(self) -> while_statement:
        if self.current_token.token_type == token_type.WHILE:
            if self.__get_next_token().token_type == token_type.OPEN_BRACKET:
                self.__get_next_token()
                if (l := self.__parse_logic_expression()) != None:
                    if self.current_token.token_type == token_type.CLOSE_BRACKER:
                        self.__get_next_token()
                        if (t := self.__parse_block()) != None:
                            return while_statement(self.current_token.location,l, t)
                        else:
                            raise syntax_exception("Expected block", loc = self.current_token.location)    
                    else:
                        raise syntax_exception("Expected closing bracket", loc = self.current_token.location)    
                else:
                    raise syntax_exception("Expected logic expression", loc = self.current_token.location)    
            else:
                raise syntax_exception("Expected opening bracket", loc = self.current_token.location)    
        else:
            return None

    def __parse_assignment(self, name: token) -> assignment:
        if self.current_token.token_type == token_type.ASSIGNMENT_OPERATOR:
            self.__get_next_token()
            if l := self.__parse_logic_expression():
                return assignment(self.current_token, name.value, l)
            else:
                raise syntax_exception("Expected logic expression", loc = self.current_token.location)    
        else:
            return None

    def __parse_function_call(self, name: token, sign: str) -> function:
        if (p := self.__parse_parameters()) != None:
            return function(self.current_token.location, name.value, p, sign)
        else:
            return None

    def __parse_value(self) -> value:
        signs = ("!", "+", "-")
        sign = None
        if self.current_token.value in signs:
            sign = self.current_token.value
            self.__get_next_token()
        if self.current_token.token_type == token_type.IDENTIFIER:
            if self.current_token.value == 'True' or self.current_token.value == 'False':
                bool_value = 1 if self.current_token.value == 'True' else 0
                temp = number(self.current_token.location, bool_value)
                self.__get_next_token()
                return temp
            temp = identifier(self.current_token.location, self.current_token.value, sign)
            name = self.current_token
            self.__get_next_token()
            if (f := self.__parse_function_call(name, sign)) != None:
                if sign and sign != '!':
                    raise Exception("Function call can only have \'!\' sign")
                return f
            else:
                return temp
        elif self.current_token.token_type == token_type.STRING:
            temp = string(self.current_token.location, self.current_token.value)
            self.__get_next_token()
            if sign:
                raise Exception("String cannot have any sign")
            return temp
        elif self.current_token.token_type == token_type.CONST:
            temp = number(self.current_token.location, self.current_token.value, sign)
            self.__get_next_token()
            if sign and sign == "!":
                raise Exception("Number cannot have \'!\' sign")
            return temp
        else:
            return None

    def __parse_logic_expression(self) -> logic_expression:
        conditions = list()
        operators = list()
        location = self.current_token.location
        if c := self.__parse_condition():
            conditions.append(c)
            if self.current_token.token_type != token_type.OR_OPERATOR:
                return c
            while self.current_token.token_type == token_type.OR_OPERATOR:
                o = self.current_token
                self.__get_next_token()
                if c := self.__parse_condition():
                    conditions.append(c)
                    operators.append(o)
                else:
                    raise syntax_exception("Expected codnition", loc = self.current_token.location)
            return logic_expression(location, operators=operators, values=conditions)
        else:
            return None

    def __parse_condition(self) -> condition:
        relations = list()
        operators = list()
        location = self.current_token.location
        if r := self.__parse_relation():
            relations.append(r)
            if self.current_token.token_type != token_type.AND_OPERATOR:
                return r
            while self.current_token.token_type == token_type.AND_OPERATOR:
                o = self.current_token
                self.__get_next_token()
                if r := self.__parse_relation():
                    relations.append(r)
                    operators.append(o)
                else:
                    raise syntax_exception("Expected relation", loc = self.current_token.location)
            return condition(location, operators=operators, values=relations)
        else:
            None

    def __parse_relation(self) -> relation:
        math_expressions = list()
        operators = list()
        location = self.current_token.location
        if m := self.__parse_math_expression():
            math_expressions.append(m)
            if self.current_token.token_type == token_type.COMP_OPERATOR:
                o = self.current_token
                self.__get_next_token()
                if m := self.__parse_math_expression():
                    math_expressions.append(m)
                    operators.append(o)
                    return relation(location, operators=operators, values=math_expressions)
                else:
                    raise syntax_exception("Expected math expression", loc = self.current_token.location)
            else:
                return m
        else:
            return None

    def __parse_math_expression(self) -> math_expression:
        factors = list()
        operators = list()
        location = self.current_token.location
        if f := self.__parse_factor():
            factors.append(f)
            if self.current_token.token_type != token_type.ADD_OPERATOR:
                return f
            while self.current_token.token_type == token_type.ADD_OPERATOR:
                o = self.current_token
                self.__get_next_token()
                if f := self.__parse_factor():
                    factors.append(f)
                    operators.append(o)
                else:
                    raise syntax_exception("Expected factor", loc = self.current_token.location)
            return math_expression(location, operators=operators, values=factors)
        else:
            None

    def __parse_factor(self) -> factor:
        values = list()
        operators = list()
        location = self.current_token.location
        if v := self.__parse_logic_factor():
            values.append(v)
            if self.current_token.token_type != token_type.MUL_OPERATOR:
                return v
            while self.current_token.token_type == token_type.MUL_OPERATOR:
                o = self.current_token
                self.__get_next_token()
                if v := self.__parse_logic_factor():
                    values.append(v)
                    operators.append(o)
                else:
                    raise syntax_exception("Expected logic_expression", loc = self.current_token.location)
            return factor(location, operators=operators, values=values)
        else:
            None

    def __parse_logic_factor(self) -> value or logic_expression:
        if self.current_token.token_type == token_type.OPEN_BRACKET:
            self.__get_next_token()
            if e := self.__parse_logic_expression():
                if self.current_token.token_type == token_type.CLOSE_BRACKER:
                    self.__get_next_token()
                    return e
                else:
                    raise Exception("Expected closing bracket")
            else:
                raise Exception("Expected logic_expression")
        else:
            if f := self.__parse_value():
                return f
            else:
                raise Exception("Expectred value")