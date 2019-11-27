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

class AnimatedImage(Drawable):
    def __init__(self, urls):
        super().__init__()
        self.pixmap = []
        self.frame = 0
        for url in urls:
            self.pixmap.append(QPixmap(url))

    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.drawPixmap(QRect(location[0], location[1], size[0], size[1]), self.pixmap[self.frame//1])
    
    def animate(self, i):
        self.frame = (self.frame*2+i) % len(pixmap)
            

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

class BlockDrawable(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(200, 200, 200), 3))
        qp.setBrush(QColor(30, 30, 30))
        qp.drawRect(location[0], location[1], size[0], size[1])
    
    def drawWrap(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(200, 200, 200, 50), 3))
        qp.setBrush(QColor(200, 200, 200, 50))
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

class ShopDrawable(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(200, 200, 200), 5))
        qp.setBrush(QColor(30, 30, 30))
        qp.drawRect(location[0], location[1], size[0], size[1])

class ShopButtonDrawable(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(200, 200, 200), 3))
        qp.setBrush(QColor(30, 30, 30))
        qp.drawRect(location[0], location[1], size[0], size[1])
    
    def drawWrap(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(200, 200, 200, 50), 3))
        qp.setBrush(QColor(200, 200, 200, 50))
        qp.drawRect(location[0], location[1], size[0], size[1])

class ShopMoneyDrawable(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(0, 0, 0), 1))
        qp.setBrush(QColor(20, 20, 200))
        qp.drawRect(location[0], location[1], size[0], size[1])

    def draw2(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(0, 0, 0), 1))
        qp.setBrush(QColor(20, 20, 20))
        qp.drawRect(location[0], location[1], size[0], size[1])

class CostDrawable(Drawable):
    def __init__(self, cost):
        self.cost = cost
    def draw(self, ctx, location, size=(40, 40)):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(0, 0, 0), 1))
        qp.setBrush(QColor(20, 20, 200))
        qp.drawRect(location[0]-size[0]//2, location[1]-size[1]//2, size[0], size[1])
        Text(str(self.cost), QFont('D2Coding', 24), QColor(255, 255, 255)).draw(ctx, (location[0]-8, location[1]+12))