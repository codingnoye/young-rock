import time

from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint

from Object import *
from Drawable import *

class Scene:
    def __init__(self):
        self.objects = []
        self.mouse = (0, 0)
        self.dragging = False

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self, ctx):
        for obj in self.objects:
            obj.draw(ctx)

    def addObject(self, obj):
        self.objects.append(obj)
    
    def event(self, e):
        for obj in self.objects:
            obj.event(e)

class TestScene(Scene):
    def __init__(self):
        super().__init__()

        #self.player = Player(self, (100, 500), (100, 500))
        #self.addObject(self.player)

        self.mainScroll = MainScroll(self, (100, 100), (400, 800))
        self.addObject(self.mainScroll)

        self.card = Card(self, (100, 100))
        self.addObject(self.card)
    
    def draw(self, ctx):
        super().draw(ctx)
        Text(str(time.time()), (50, 50), QFont('Consolas', 48), QColor(0, 255, 255)).draw(ctx)
        Text(str(self.mouse), (100, 100), QFont('Consolas', 48), QColor(0, 255, 255)).draw(ctx)