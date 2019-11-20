from Drawable import *
import time
from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint

class Object:
    def __init__(self, scene, drawable, location, size):
        self.drawable = drawable
        self.location = location
        self.size = size
        self.scene = scene
        self.dragging = False

    def update(self):
        pass

    def draw(self, ctx):
        if self.drawable != None:
            self.drawable.draw(ctx, self.location, self.size)

    def isHover(self):
        print((self.scene.mouse[0] >= self.location[0] and self.scene.mouse[1] >= self.location[1] and self.scene.mouse[0] <= self.location[0] + self.size[0] and self.scene.mouse[1] <= self.location[1] + self.size[1]))
        return (self.scene.mouse[0] >= self.location[0] and self.scene.mouse[1] >= self.location[1] and self.scene.mouse[0] <= self.location[0] + self.size[0] and self.scene.mouse[1] <= self.location[1] + self.size[1])

    def event(self, e):
        if e == 'press':
            self.onPress()
        elif e == 'release':
            self.onRelease()
        elif e == 'mousemove':
            self.onMouseMove()
    def onPress(self):
        if self.isHover():
            self.dragging = True
    
    def onRelease(self):
        if self.isHover():
            self.dragging = False
    
    def onMouseMove(self):
        pass

class Player(Object):
    def __init__(self, scene,  location, size):
        super().__init__(scene, Image('./res/image/python.svg'), location, size)

class MainScroll(Object):
    def __init__(self, scene,  location, size):
        super().__init__(scene, Rect(), location, size)

class Card(Object):
    def __init__(self, scene,  location, size = (300, 180)):
        super().__init__(scene, CardDrawable(), location, size)
        self.tracking = False
        self.trackingXY = (0, 0)
        self.code = [
            ("for i in range(3):", 0)
        ]
    
    def update(self):
        super().update()
        if self.dragging:
            self.location = (self.scene.mouse[0] - self.trackingXY[0], self.scene.mouse[1] - self.trackingXY[1])

    def onPress(self):
        super().onPress()
        self.trackingXY = ((self.scene.mouse[0] - self.location[0], self.scene.mouse[1] - self.location[1]))

    def draw(self, ctx):
        super().draw(ctx)
