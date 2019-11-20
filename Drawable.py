from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint

class Drawable:
    def draw(self, ctx, location, size):
        pass

class Text(Drawable):
    def __init__(self, text, font, color):
        super().__init__()
        self.text = text
        self.font = font
        self.color = color

    def draw(self, ctx, location, size=None):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(self.color)
        qp.setFont(self.font)
        qp.drawText(location[0], location[1], self.text)

class Image(Drawable):
    def __init__(self, url):
        super().__init__()
        self.pixmap = QPixmap(url)

    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.drawPixmap(QRect(location[0], location[1], size[0], size[1]), self.pixmap)

class Rect(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setBrush(QColor(25, 0, 90, 200))
        qp.drawRect(location[0], location[1], size[0], size[1])

class ScrollDrawable(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(200, 200, 200), 5))
        qp.setBrush(QColor(30, 30, 30))
        qp.drawRect(location[0], location[1], size[0], size[1])

class CardDrawable(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(200, 200, 200), 3))
        qp.setBrush(QColor(30, 30, 30))
        qp.drawRect(location[0], location[1], size[0], size[1])
    
class HpDrawable(Drawable):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(0, 0, 0), 2))
        qp.setBrush(QColor(20, 20, 20))
        qp.drawRect(location[0], location[1], self.width, self.height)
        qp.setPen(QPen(QColor(0, 0, 0), 2))
        qp.setBrush(QColor(255, 40, 40))
        qp.drawRect(location[0], location[1], size[0], self.height)