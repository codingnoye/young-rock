from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint, QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import threading, time, sys

from Scene import * # 게임의 각 화면을 구성하는 Scene

'필요한 폰트 목록'
'Noto Serif: Noto Mono, D2Coding, Press Start 2P'

class Game(QWidget):
    def __init__(self, app):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.setMaximumSize(1600, 900)
        self.scene = None
        self.debug = False
        self.app = app
        self.won = False
        self.thread = None
        self.isRunning = True
    
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
        while self.isRunning:
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

    def closeEvent(self, event):
        super().closeEvent(event)
        self.isRunning = False
        self.scene = None
        self.deleteLater()
        self.app.quit()
        sys.exit(0)


if __name__ == '__main__':
    # init game
    app = QApplication([])
    game = Game(app)
    Scene.game = game
    game.setScene(IntroScene())
    # start game loop
    game.thread = threading.Thread(target=game.loop, daemon=True)
    game.thread.start()
    # event loop
    sys.exit(app.exec_())