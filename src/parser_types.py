from .data_structures import location

class program:
    def __init__(self):
        self.definition_list = []
        self.statement_list = []

    def add_element(self, element: 'statement or definition'):
        if issubclass(type(element), definition):
            self.definition_list.append(element)
        elif issubclass(type(element), statement):
            self.statement_list.append(element)

class definition:
    def __init__(self, location: location, identifier: str, block: 'block', parameters: 'list[str]' = None):
        self.location = location
        self.identifier = identifier
        self.parameter_list = parameters
        self.block = block

class statement:
    def __init__(self, location: location):
        self.location = location

class if_statement(statement):
    def __init__(self, location: location, expression: 'logic_expression', true_block: 'block', false_block: 'block' = None):
        super().__init__(location)
        self.expression = expression
        self.true_block = true_block
        self.false_block = false_block

class while_statement(statement):
    def __init__(self, location: location, expression: 'logic_expression', block: 'block'):
        super().__init__(location)
        self.expression = expression
        self.block = block

class block:
    def __init__(self, location: location, statement_list: 'list[statement]'):
        self.location = location
        self.statement_list = statement_list

class assignment(statement):
    def __init__(self, location, identifier: str, expression: 'logic_expression'):
        super().__init__(location)
        self.identifier = identifier
        self.expression = expression

class logic_expression:
    def __init__(self, location: location, conditions: 'list[condition]'):
        self.location = location
        self.condition_list = conditions
    
class condition:
    def __init__(self, location: location, relations: 'list[relation]' = None, expression: 'logic_expression' = None):
        self.location = location
        self.relation_list = relations
        self.expression = expression

class relation:
    def __init__(self, location: location, math_expressions: 'list[math_expression]', operators: 'list[str]'):
        self.location = location
        self.math_expression_list = math_expressions
        self.comp_operator_list = operators

class math_expression:
    def __init__(self, location: location, factors: 'list[factor]', operators: 'list[str]'):
        self.location = location
        self.factor_list = factors
        self.operator_list = operators

class factor:
    def __init__(self, location: location, values: 'list[value]' = None, operators: 'list[str]' = None, expression: 'math_expression' = None):
        self.location = location
        self.value_list = values
        self.operator_list = operators
        self.math_expression = expression

class value:
    def __init__(self, location: location, sign: str = None):
        self.location = location
        self.sign = sign

class identifier(value):
    def __init__(self, location: location, id: str, sign: str = None):
        super().__init__(location, sign=sign)
        self.id = id

class number(value):
    def __init__(self, location: location, value: int or float, sign: str = None):
        super().__init__(location, sign=sign)
        self.value = value

class string(value):
    def __init__(self, location: location, string: str, sign: str):
        super().__init__(location, sign=sign)
        self.string = string

class function(value):
    def __init__(self, location: location, identifier: identifier, arguments: 'list[logic_expression]' = None, sign: str = None):
        super().__init__(location, sign=sign)
        self.argument_list = arguments
        self.identifier = identifier