from src.data_structures import location

class unexpected_character_exception(BaseException):
    pass
class missing_character_exception(BaseException):
    pass
class parse_exception(BaseException):
    pass
class syntax_exception(BaseException):
    def __init__(self, *args: object, loc: location) -> None:
        super().__init__(*args)
        self.location = loc