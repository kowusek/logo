from .data_structures import location

class unexpected_character_exception(BaseException):
    pass
class missing_character_exception(BaseException):
    pass
class parse_exception(BaseException):
    pass
class syntax_exception(BaseException):
    location: location