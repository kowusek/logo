from __future__ import annotations
from src.data_structures import location, token_type, token
from src.context import context, root_context
from abc import ABC, abstractmethod

class program:
    def __init__(self, definitions: list[definition] = None, statements: list[statement] = None):
        if not definitions:
            self.definitions = []
        else:
            self.definitions = definitions
        if not statements:
            self.statements = []
        else:
            self.statements = statements
        self.root_context = root_context(self.definitions)

    def accept(self, visitor: visitor):
        visitor.visit_program(self)

class definition:
    def __init__(self, location: location, identifier: str, block: block, parameters: list[value] = None):
        self.location = location
        self.identifier = identifier
        self.parameter_list = parameters
        self.block = block

    def accept(self, visitor: visitor):
        visitor.visit_definition(self)

class statement:
    def __init__(self, location: location):
        self.location = location

    def accept(self, visitor: visitor):
        pass

class if_statement(statement):
    def __init__(self, location: location, expression: logic_expression, true_block: block, false_block: block = None):
        self.location = location
        self.expression = expression
        self.true_block = true_block
        self.false_block = false_block

    def accept(self, visitor: visitor):
        visitor.visit_if_statement(self)

class while_statement(statement):
    def __init__(self, location: location, expression: logic_expression, block: block):
        self.location = location
        self.expression = expression
        self.block = block

    def accept(self, visitor: visitor):
        visitor.visit_while_statement(self)

class block:
    def __init__(self, location: location, statement_list: list[statement]):
        self.location = location
        self.statement_list = statement_list

    def accept(self, visitor: visitor):
        visitor.visit_block(self)

class assignment(statement):
    def __init__(self, location, identifier: str, expression: logic_expression):
        self.location = location
        self.identifier = identifier
        self.expression = expression

    def accept(self, visitor: visitor):
        visitor.visit_assignment(self)

class logic_expression:
    def __init__(self, location: location, operators: list[token], values: list[condition]):
        self.location = location
        self.operator_list = operators
        self.value_list = values

    def accept(self, visitor: visitor):
        visitor.visit_logic_expression(self)

class condition(logic_expression):
    def __init__(self, location: location, operators: list[token], values: list[relation]):
        self.location = location
        self.operator_list = operators
        self.value_list = values

    def accept(self, visitor: visitor):
        visitor.visit_condition(self)

class relation(logic_expression):
    def __init__(self, location: location, operators: list[token], values: list[math_expression]):
        self.location = location
        self.operator_list = operators
        self.value_list = values

    def accept(self, visitor: visitor):
        visitor.visit_relation(self)

class math_expression(logic_expression):
    def __init__(self, location: location, operators: list[token], values: list[factor]):
        self.location = location
        self.operator_list = operators
        self.value_list = values

    def accept(self, visitor: visitor):
        visitor.visit_math_expression(self)

class factor(logic_expression):
    def __init__(self, location: location, operators: list[token], values: list[value or logic_expression]):
        self.location = location
        self.operator_list = operators
        self.value_list = values

    def accept(self, visitor: visitor):
        visitor.visit_factor(self)

class value:
    def __init__(self, location: location, sign: str = None):
        self.location = location
        self.sign = sign

    def accept(self, visitor: visitor):
        pass

class function(value, statement):
    def __init__(self, location: location, identifier: str, arguments: list[value] = None, sign: str = None):
        self.location = location
        self.sign = sign
        self.argument_list = arguments
        self.identifier = identifier

    def accept(self, visitor: visitor):
        visitor.visit_function(self)

class identifier(value):
    def __init__(self, location: location, id: str, sign: str = None):
        super().__init__(location, sign=sign)
        self.id = id

    def accept(self, visitor: visitor):
        visitor.visit_identifier(self)

class number(value):
    def __init__(self, location: location, value: int or float, sign: str = None):
        super().__init__(location, sign=sign)
        if sign == '-':
            self.value = -value
        else:
            self.value = value

    def accept(self, visitor: visitor):
        visitor.visit_number(self)

class string(value):
    def __init__(self, location: location, string: str, sign: str = None):
        super().__init__(location, sign=sign)
        self.string = string

    def accept(self, visitor: visitor):
        visitor.visit_string(self)

class visitor(ABC):
    
    @abstractmethod
    def visit_program(self, element: program) -> None:
        pass

    @abstractmethod
    def visit_definition(self, element: definition) -> None:
        pass

    @abstractmethod
    def visit_if_statement(self, element: if_statement) -> None:
        pass

    @abstractmethod
    def visit_while_statement(self, element: while_statement) -> None:
        pass

    @abstractmethod
    def visit_block(self, element: block) -> None:
        pass

    @abstractmethod
    def visit_assignment(self, element: assignment) -> None:
        pass

    @abstractmethod
    def visit_logic_expression(self, element: logic_expression) -> None:
        pass

    @abstractmethod
    def visit_condition(self, element: condition) -> None:
        pass

    @abstractmethod
    def visit_relation(self, element: relation) -> None:
        pass

    @abstractmethod
    def visit_math_expression(self, element: math_expression) -> None:
        pass

    @abstractmethod
    def visit_factor(self, element: factor) -> None:
        pass

    @abstractmethod
    def visit_function(self, element: function) -> None:
        pass

    @abstractmethod
    def visit_identifier(self, element: identifier) -> None:
        pass

    @abstractmethod
    def visit_number(self, element: number) -> None:
        pass

    @abstractmethod
    def visit_string(self, element: string) -> None:
        pass