from __future__ import annotations
from src.context import context, root_context
from src.parser_types import *
from src.special_functions import *
from src.marker import marker
import logging

class interpreter_visitor(visitor):
    def __init__(self, mark: marker = None):
        self.root_context = root_context()
        self.current_context = self.root_context
        self.return_val = []
        self.return_flag = False #do i need this
        self.is_return = False
        self.marker = mark
        logging.basicConfig(filename=f"./interpreter.log", level=logging.DEBUG)
        
    def visit_program(self, element: program) -> None:
        for definition in element.definitions:
            definition.accept(self)

        for statement in element.statements:
            statement.accept(self)
            self.return_val = []

    def visit_definition(self, element: definition) -> None:
        self.current_context.definitions[element.identifier] = element

    def visit_if_statement(self, element: if_statement) -> None:
        element.expression.accept(self)
        new_condition = self.return_val.pop()
        temp_context = self.current_context
        self.current_context = context(parent_context=self.current_context)
        if new_condition:
            element.true_block.accept(self)
        elif element.false_block:
            element.false_block.accept(self)
        self.current_context = temp_context
        

    def visit_while_statement(self, element: while_statement) -> None:
        element.expression.accept(self)
        new_condition = self.return_val.pop()
        temp_context = self.current_context
        self.current_context = context(parent_context=self.current_context)
        while new_condition:
            element.block.accept(self)
            element.expression.accept(self)
            new_condition = self.return_val.pop()
        self.current_context = temp_context


    def visit_block(self, element: block) -> None:
        for statement in element.statement_list:
            if self.is_return:
                self.is_return = False
                return
            else:
                self.return_val = []
            statement.accept(self)

    def visit_assignment(self, element: assignment) -> None:
        element.expression.accept(self)
        result = self.return_val.pop()
        self.current_context.define_variable(element.identifier, result)

    def visit_logic_expression(self, element: logic_expression) -> None:
        result = []
        for relatioin in element.value_list:
            if isinstance(relatioin, str):
                logging.error(f"Strings cannot be interpreted as bool value at: {relatioin.location}")
                raise Exception
            relatioin.accept(self)
            result.append(not self.return_val.pop())
        self.return_val.append(not all(result))

    def visit_condition(self, element: condition) -> None:
        result = []
        for relatioin in element.value_list:
            if isinstance(relatioin, str):
                logging.error(f"Strings cannot be interpreted as bool value at: {relatioin.location}")
                raise Exception
            relatioin.accept(self)
            result.append(self.return_val.pop())
        self.return_val.append(all(result))

    def visit_relation(self, element: relation) -> None:
        COMP_OPERATIONS = {
            "==": lambda l, r: l == r,
            ">=": lambda l, r: l >= r,
            "<=": lambda l, r: l <= r,
            ">": lambda l, r: l > r,
            "<": lambda l, r: l < r,
        }
        element.value_list[0].accept(self)
        left = self.return_val.pop()
        if isinstance(left, str):
            logging.error(f"Strings cannot be interpreted as bool value at: {left.location}")
            raise Exception
        element.value_list[1].accept(self)
        right = self.return_val.pop()
        if isinstance(right, str):
            logging.error(f"Strings cannot be interpreted as bool value at: {right.location}")
            raise Exception
        result = COMP_OPERATIONS[element.operator_list[0].value](left, right)
        self.return_val.append(result)

    def visit_math_expression(self, element: math_expression) -> None:
        element.value_list[0].accept(self)
        result = self.return_val.pop()
        if isinstance(result, str):
            logging.error(f"Strings cannot be added at: {result.location}")
            raise Exception
        i = 1
        while i <= len(element.operator_list):
            operator = element.operator_list[i - 1].value
            element.value_list[i].accept(self)
            new_element = self.return_val.pop()
            if isinstance(new_element, str):
                logging.error(f"Strings cannot be added at: {result.location}")
                raise Exception
            if operator == '+':
                result += new_element
            else:
                result -= new_element
            i += 1
        self.return_val.append(result)

    def visit_factor(self, element: factor) -> None:
        element.value_list[0].accept(self)
        result = self.return_val.pop()
        if isinstance(result, str):
            logging.error(f"Strings cannot be multiplied at: {result.location}")
            raise Exception
        i = 1
        while i <= len(element.operator_list):
            operator = element.operator_list[i - 1].value
            element.value_list[i].accept(self)
            new_element = self.return_val.pop()
            if isinstance(new_element, str):
                logging.error(f"Strings cannot be multiplied at: {new_element.location}")
                raise Exception
            if operator == '*':
                result *= new_element
            else:
                if new_element == 0:
                    logging.error(f"Dividing by zero at: {new_element.location}")
                    raise Exception
                result /= new_element
            i += 1
        self.return_val.append(result)

    def visit_function(self, element: function) -> None:
        for x in element.argument_list:
            x.accept(self)
        values = self.return_val
        self.return_val = []
        if element.identifier in special_function:
            try:
                special_function[element.identifier](self, self.marker, *values)
            except Exception as e:
                logging.error(f"{e} at: {element.argument_list[0].location}")
                raise Exception
        else:
            definition = self.current_context.get_definition(element.identifier)
            self._function_execute(definition, values, self.current_context.get_root_context())

    def _function_execute(self, function: definition, values: list[value], global_context: context):
        variables = {}
        if len(values) != len(function.parameter_list):
            logging.error(f"Numbers of arguments don't match at: {values[0].location}")
            raise Exception
        for name, value in zip([x.id for x in function.parameter_list], values):
            variables[name] = value

        temp_context = self.current_context
        self.current_context = context(variables=variables, parent_context=global_context)
        function.block.accept(self)
        self.current_context = temp_context

    def visit_identifier(self, element: identifier) -> None:
        result = self.current_context.get_variable(element.id)
        if result is None:
            logging.error(f"Trying to access undefined variable at: {element.location}")
            raise Exception
        self.return_val.append(result)

    def visit_number(self, element: number) -> None:
        self.return_val.append(element.value)

    def visit_string(self, element: string) -> None:
        self.return_val.append(element.string)