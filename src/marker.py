from math import sin, cos, radians

class marker:
    def __init__(self):
        self.lines = [(0,0)]
        self.angle = 0

    def forward(self,value):
        x = value * sin(-radians(self.angle))
        y = value * cos(-radians(self.angle))
        self._move_marker(x, y)

    def rotate(self,value):
        self._rotate_marker(self.angle + value)

    def _move_marker(self, x, y):
        start_x, start_y = self.lines[-1]
        self.lines.append((start_x + x, start_y + y))

    def _rotate_marker(self, angle):
        self.angle = angle