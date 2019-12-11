from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint, QRectF

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

class CodeDrawable(Drawable):
    def __init__(self):
        super().__init__()
        self.code = ''
    def setCode(self, code):
        self.code = code
    def draw(self, ctx, location, size=None):
        nowx = location[0]
        i = 0
        event = ctx[0]
        qp = ctx[1]
        COND = QColor("#D59DF6")
        METHOD = QColor("#71B1FE")
        NORM = QColor("#FFFFFF")
        fontSize = 16
        lineSpacing = 1.5
        qp.setFont(QFont('D2Coding', fontSize))
        wSpacing = 0.65
        nowx = location[0]
        nowy = location[1]
        code = self.code
        while i<len(code):
            if code[i] == '\n':
                nowx = location[0]
                nowy += 1*lineSpacing*fontSize
                i+=1
            elif code[i:i+2] == 'if':
                qp.setPen(COND)
                qp.drawText(nowx, nowy, code[i:i+2])
                nowx += fontSize * 2 * wSpacing
                i += 2
            elif code[i:i+4] == 'else':
                qp.setPen(COND)
                qp.drawText(nowx, nowy, code[i:i+4])
                nowx += fontSize * 4 * wSpacing
                i += 4
            elif code[i:i+5] == 'while':
                qp.setPen(COND)
                qp.drawText(nowx, nowy, code[i:i+5])
                nowx += fontSize * 5 * wSpacing
                i += 5
            elif code[i:i+2] == 'in':
                qp.setPen(COND)
                qp.drawText(nowx, nowy, code[i:i+2])
                nowx += fontSize * 2 * wSpacing
                i += 2
            elif code[i:i+3] == 'for':
                qp.setPen(COND)
                qp.drawText(nowx, nowy, code[i:i+3])
                nowx += fontSize * 3 * wSpacing
                i += 3
            elif code[i:i+5] == 'range':
                qp.setPen(METHOD)
                qp.drawText(nowx, nowy, code[i:i+5]) 
                nowx += fontSize * 5 * wSpacing
                i += 5
            elif code[i:i+6] == 'attack':
                qp.setPen(METHOD)
                qp.drawText(nowx, nowy, code[i:i+6]) 
                nowx += fontSize * 6 * wSpacing
                i += 6
            elif code[i:i+7] == 'defence':
                qp.setPen(METHOD)
                qp.drawText(nowx, nowy, code[i:i+7]) 
                nowx += fontSize * 7 * wSpacing
                i += 7
            elif code[i:i+6] == 'player':
                qp.setPen(METHOD)
                qp.drawText(nowx, nowy, code[i:i+6]) 
                nowx += fontSize * 6 * wSpacing
                i += 6
            elif code[i:i+5] == 'enemy':
                qp.setPen(METHOD)
                qp.drawText(nowx, nowy, code[i:i+5]) 
                nowx += fontSize * 5 * wSpacing
                i += 5
            else:
                qp.setPen(NORM)
                qp.drawText(nowx, nowy, code[i:i+1]) 
                nowx += fontSize * 1 * wSpacing
                i += 1

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

    def draw(self, ctx, location, size, seeingRight = True):
        event = ctx[0]
        qp = ctx[1]
        if seeingRight:
            qp.drawPixmap(QRect(location[0], location[1], size[0], size[1]), self.pixmap[int(self.frame)])
        else:
            qp.drawPixmap(QRect(location[0], location[1], size[0], size[1]), QPixmap.fromImage(self.pixmap[int(self.frame)].toImage().mirrored(horizontal = True, vertical = False)))
    def animate(self, i):
        if self.frame+i >= len(self.pixmap):
            self.frame = (self.frame+i) % len(self.pixmap)
            return True
        else:
            self.frame = self.frame + i
            return False
    
    def reset(self):
        self.frame = 0
            

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
    def __init__(self, category=10):
        super().__init__()
        self.category = category
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(200, 200, 200), 3))
        category = self.category
        if category == 10:
            color = QColor(30, 30, 30)
        elif category == 0:
            color = QColor(30, 30, 70)
        elif category == 1 or category == 2:
            color = QColor(30, 30, 120)
        elif category == 3:
            color = QColor(40, 40, 150)
        elif category == 11:
            color = QColor(80, 50, 30)
        else:
            color = QColor(100, 100, 100)
        qp.setBrush(color)
        qp.drawRect(location[0], location[1], size[0], size[1])
    
    def drawWrap(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(200, 200, 200, 50), 3))
        qp.setBrush(QColor(200, 200, 200, 50))
        qp.drawRect(location[0], location[1], size[0], size[1])
    
    def drawSold(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(0, 0, 0, 200), 3))
        qp.setBrush(QColor(0, 0, 0, 50))
        qp.drawRect(location[0], location[1], size[0], size[1])


class ButtonDrawable(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(200, 200, 200), 3))
        qp.setBrush(QColor(30, 30, 30))
        qp.drawRect(location[0], location[1], size[0], size[1])

class ShopMoneyDrawable(Drawable):
    def draw(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(255, 255, 0), 10))
        qp.setBrush(QColor(185, 185, 0))
        qp.drawRect(location[0]+10, location[1]+10, size[0]-20, size[1]-20)

    def draw2(self, ctx, location, size):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(255, 255, 255), 2))
        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(location[0], location[1], size[0], size[1])

class CostDrawable(Drawable):
    def __init__(self, cost):
        self.cost = cost
    def draw(self, ctx, location, size=(40, 40)):
        event = ctx[0]
        qp = ctx[1]
        qp.setPen(QPen(QColor(255, 255, 0), 4))
        qp.setBrush(QColor(185, 185, 0))
        qp.drawRect(location[0]-size[0]//2, location[1]-size[1]//2, size[0], size[1])
        Text(str(self.cost), QFont('NotoMono', 24, 1), QColor(0, 0, 0)).draw(ctx, (location[0]-10, location[1]+12))