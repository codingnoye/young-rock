from Drawable import *
import time
from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint

class Object:
    def __init__(self, scene, drawable, location, size):
        self.objid = None
        self.drawable = drawable
        self.location = location
        self.size = size
        self.scene = scene
        self.dragging = False
        self.fontSize = 16

    def update(self):
        pass

    def draw(self, ctx):
        if self.drawable != None:
            self.drawable.draw(ctx, self.location, self.size)

    def isHover(self):
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
    def __init__(self, scene, location, size):
        super().__init__(scene, Image('./res/image/python.svg'), location, size)
        self._health = 100
        self._shield = 0
        self._armor = 0
        self._power = 0
        self._evade = 0
        self.effectOffset = (size[0]/2, 0)
        self.hpbar = HpDrawable(150, 30)
        self.blocks = []
        self.nowblock = None
    
    def getAttacked(self, damage):
        if self._evade>0:
            self.showEffect('evade', '회피함!')
            self.evade -= 1
        else:
            self.health -= max(damage-self._armor, 0)
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, newval):
        if newval>100: newval = 100
        print(1)
        if newval<self._health:
            print(2)
            self.showEffect('hurt', self._health - newval)
            self._health = newval
        elif newval>self._health:
            print(3)
            self.showEffect('heal', '+'+str(abs(self._health - newval)))
            self._health = newval
        else:
            print(4)
            self.showEffect('nothing', 0)

    def showEffect(self, effect, text):
        if type(text) != str: text = str(text)
        if effect == 'hurt':
            dmg = Dmg(self.scene, (self.location[0]+32, self.location[1]-32), text, QColor(255, 40, 40), 48)
            dmg.objid = self.scene.addObject(dmg)
        elif effect == 'evade':
            dmg = Dmg(self.scene, (self.location[0]+32, self.location[1]-32), text, QColor(150, 150, 150), 48)
            dmg.objid = self.scene.addObject(dmg)
        elif effect == 'heal':
            dmg = Dmg(self.scene, (self.location[0]+32, self.location[1]-32), text, QColor(40, 255, 40), 48)
            dmg.objid = self.scene.addObject(dmg)
        elif effect == 'nothing':
            dmg = Dmg(self.scene, (self.location[0]+32, self.location[1]-32), text, QColor(170, 170, 170), 48)
            dmg.objid = self.scene.addObject(dmg)
    
    def draw(self, ctx):
        super().draw(ctx)
        self.hpbar.draw(ctx, (self.location[0]+50-75, self.location[1]-70), (150*self.health/100, None))

        

class Scroll(Object):
    def __init__(self, scene,  location, size):
        super().__init__(scene, ScrollDrawable(), location, size)
        self.blocks = []

class Dmg(Object):
    def __init__(self, scene, location, text, color, size):
        super().__init__(scene, Text(text, QFont('D2Coding', size), color), location, (100, 50))
        self.lifetime = 0
    def update(self):
        self.lifetime += 1
        self.location = (self.location[0], self.location[1]-(55 - self.lifetime)/7)
        if self.lifetime>40:
            self.scene.removeObject(self.objid)

class Block(Object):
    def __init__(self, scene,  location, code = []):
        super().__init__(scene, CardDrawable(), location, (300, 180))
        self.code = code
        self.fontSize = 16
        self.lineSpace = 1.5
        self.text = []
        
        self.makeCode()

    def onPress(self):
        super().onPress()
        self.scene.blockUse(self, True)

    def draw(self, ctx):
        super().draw(ctx)
        i=0
        for text in self.text:
            Text(text, QFont('D2Coding', self.fontSize), QColor(255, 255, 255)).draw(ctx, (30+self.location[0], 40+self.location[1] + self.fontSize*self.lineSpace*i))
            i+=1

    def makeCode(self):
        for c in self.code:
            self.text += ['    ' * c[1] + c[0]]
        self.size = (self.size[0], 80-self.fontSize + (len(self.code)-1)*self.fontSize*self.lineSpace)

class Card(Object):
    def __init__(self, scene,  location, size = (300, 90)):
        super().__init__(scene, CardDrawable(), location, size)
        self.tracking = False
        self.trackingXY = (0, 0)
        self.code = []
        self.text = ''
        self.makeCode()
        self.fontSize = 16
    
    def update(self):
        super().update()
        if self.dragging:
            self.location = (self.scene.mouse[0] - self.trackingXY[0], self.scene.mouse[1] - self.trackingXY[1])

    def onPress(self):
        super().onPress()
        self.trackingXY = ((self.scene.mouse[0] - self.location[0], self.scene.mouse[1] - self.location[1]))

    def draw(self, ctx):
        super().draw(ctx)
        Text(self.text, QFont('D2Coding', self.fontSize), QColor(255, 255, 255)).draw(ctx, (30+self.location[0], 40+self.location[1]))

    def makeCode(self):
        for c in self.code:
            self.text += '    ' * c[1] + c[0] + '\n'
