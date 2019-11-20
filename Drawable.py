from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint

class Drawable:
    def draw(self, ctx, location, size):
        pass

class Text(Drawable):
    def __init__(self, text, location, font, color):
        super().__init__()
        self.text = text
        self.font = font
        self.color = color
        self.location = location

    def draw(self, ctx):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(self.color)
        qp.setFont(self.font)
        qp.drawText(self.location[0], self.location[1], self.text)

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

class MainScrollDrawable(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(0, 0, 0, 255), 5))
        qp.setBrush(QColor(255, 255, 255, 255))
        qp.drawRect(location[0], location[1], size[0], size[1])

class CardDrawable(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(0, 0, 0, 255), 5))
        qp.setBrush(QColor(255, 255, 255, 255))
        qp.drawRect(location[0], location[1], size[0], size[1])