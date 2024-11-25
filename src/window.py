import sys
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QGraphicsScene, QWidget, QGraphicsView, QVBoxLayout
from PyQt5.QtWidgets import QApplication

class logo_scene(QGraphicsScene):
    def __init__(self):
        super(QGraphicsScene, self).__init__(-500, -500, 1000, 1000)
        self.setBackgroundBrush(QBrush(Qt.white))
        self.marker = QPen(Qt.black)

    def draw_line(self, x1, y1, x2, y2):
        self.addLine(x1, y1, x2, y2, self.marker)

class window:
    def __init__(self, lines: 'list[tuple]', angle: float):
        self.lines = lines
        self.angle = angle

    def render(self):
        app = QApplication(sys.argv)
        self.scene = logo_scene()
        widget = QWidget()
        view = QGraphicsView()
        layout = QVBoxLayout()
        
        view.setScene(self.scene)
        view.resizeEvent = lambda x: view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        layout.addWidget(view)
        widget.setLayout(layout)

        self.draw_lines()

        widget.show()
        sys.exit(app.exec_())

    def draw_lines(self):
        start_x = 0
        start_y = 0
        for x, y in self.lines:
            self.scene.draw_line(start_x, start_y, x, y)
            start_x = x
            start_y = y
        self.draw_marker(x, y)

    def draw_marker(self, x: int, y: int):
        path = QPainterPath(QPointF(0, 0))
        path.lineTo(QPointF(5, -5))
        path.lineTo(QPointF(0, 5))
        path.lineTo(QPointF(-5, -5))
        path.lineTo(QPointF(0, 0))
        marker = self.scene.addPath(path, QPen(Qt.black), QBrush(Qt.black))
        marker.moveBy(x, y)
        marker.setRotation(self.angle)