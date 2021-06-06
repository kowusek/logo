from __future__ import annotations

class context:
    def __init__(self, definition_list: list = None, variables: dict = None, parent_context: context or root_context = None ):
        self.parent = parent_context

        self.definitions = {}
        if definition_list:
            for el in definition_list:
                self.definitions[el.identifier] = el

        self.variables = {}
        if variables:
            self.variables = variables

    def define_variable(self, name, value):
        if name in self.definitions.keys():
            raise Exception("Redefinition of variable")

        existing_variable = self.variables.get(name)
        if existing_variable is None and self.parent:
            existing_variable = self.parent.get_variable(name)
            if existing_variable is not None:
                self.parent.define_variable(name, value)
                return
        self.variables[name] = value

    def get_variable(self, name):
        result = self.variables.get(name)

        if result is None and self.parent:
            return self.parent.get_variable(name)
        else:
            return result

    def get_definition(self, name):
        return self.parent.get_definition(name)

    def get_root_context(self):
        if self.parent:
            return self.parent.get_root_context()

class root_context(context):
    def __init__(self, definition_list=[]):
        super().__init__(definition_list)

    def get_definition(self, name):
        return self.definitions.get(name)

    def get_root_context(self):
        return self