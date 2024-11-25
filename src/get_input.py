from src.data_structures import location

class get_input:
    def __init__(self, file_path):
        self.file_path = file_path
        self.line_count = 1
        self.position_in_line = -1
        self.gen = self._char_generator()

    def _char_generator(self) -> str:
        with open(self.file_path, "r") as file:
            while char := file.read(1):
                if char == '\n':
                    self.position_in_line = -2
                    self.line_count += 1
                self.position_in_line += 1
                yield char

    def get_char(self) -> str:
        return next(self.gen)

    def get_location(self) -> int and int:
        return location(self.line_count, self.position_in_line)