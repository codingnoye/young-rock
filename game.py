from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

import threading, time

from Object import Object
from Drawable import Drawable, Image
from Scene import Scene, TestScene

class Game(QWidget):
    def __init__(self, scene):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.setMaximumSize(1600, 900)
        self.scene = scene
        self.show()
    
    def initUI(self):
        self.resize(1600, 900)
        self.setWindowTitle('Young Rock')
        self.setStyleSheet("background-color:rgb(150, 150, 150);");

    def paintEvent(self, event):
        qp = QPainter()
        ctx = (event, qp)
        qp.begin(self)
        self.scene.draw(ctx)
        qp.end()

    def loop(self):
        while True:
            self.scene.update()
            self.update()
            time.sleep(1/60)
    
    def mouseMoveEvent(self, event):
        self.scene.mouse = (event.x(), event.y())
        self.scene.event("mousemove")

    def mousePressEvent(self, event):
        self.scene.event("press")

    def mouseReleaseEvent(self, event):
        self.scene.event("release")

if __name__ == '__main__':
    # init game
    app = QApplication([])
    scene = TestScene()
    game = Game(scene)

    # start main loop
    thread = threading.Thread(target=game.loop)
    thread.start()

    app.exec_()