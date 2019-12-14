from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

import threading, time

from Object import Object
from Drawable import Drawable, Image
from Scene import *

'Font: Noto Mono, D2Coding, Press Start 2P'
class Game(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.setMaximumSize(1600, 900)
        self.scene = None
        self.debug = False
        self.won = False
    
    def setScene(self, scene):
        self.scene = scene
        self.show()
    
    def initUI(self):
        self.resize(1600, 900)
        self.setWindowTitle('Young Rock')

    def paintEvent(self, event):
        qp = QPainter()
        ctx = (event, qp)
        qp.begin(self)
        if self.scene != None:
            self.scene.draw(ctx)
        qp.end()

    # thread
    def loop(self):
        while True:
            if self.scene != None:
                self.scene.update()
            self.update()
            time.sleep(1/60)
    
    def mouseMoveEvent(self, event):
        if self.scene != None:
            self.scene.mouse = (event.x(), event.y())
            self.scene.event("mousemove")

    def mousePressEvent(self, event):
        if self.scene != None:
            self.scene.event("press")

    def mouseReleaseEvent(self, event):
        if self.scene != None:
            self.scene.event("release")

if __name__ == '__main__':
    # init game
    app = QApplication([])
    game = Game()
    Scene.game = game
    game.setScene(IntroScene())
    
    # start main loop
    thread = threading.Thread(target=game.loop)
    thread.start()

    app.exec_()