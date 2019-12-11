from Drawable import *
import time
from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint
import Codes
import Socket
import json
import enum
import random

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

class Button(Object):
    def __init__(self, scene, text, callback, location, size=(300, 150)):
        super().__init__(scene, ButtonDrawable(), location, size)
        self.text = text
        self.callback = callback
    def draw(self, ctx):
        super().draw(ctx)
        Text(self.text, QFont('NotoMono', self.fontSize), QColor(255, 255, 255)).draw(ctx, (30+self.location[0], self.location[1] + self.size[1]//2 + self.fontSize//2))
    def onClick(self):
        self.callback()
    def onPress(self):
        super().onPress()
        if self.isHover():
            self.onClick()

class Label(Object):
    def __init__(self, scene, location, size = (400, 200)):
        super().__init__(scene, None, location, size)
        self.text = ''

    def draw(self, ctx):
        super().draw(ctx)
        Text(self.text, QFont('NotoMono', 48), QColor(255, 255, 255)).draw(ctx, self.location)

class Act(enum.IntEnum):
    IDLE = 0
    ATTACK = 1
    HATTACK = 2
    EVADE = 3
    HURT = 4
    DIE = 5

ActSprite = [[] for _ in range(len(Act))]
class Player(Object):
    first = True
    def __init__(self, scene, location, size):
        if Player.first:
            ActSprite[Act.IDLE] = [AnimatedImage(['./res/image/idle/0.png', './res/image/idle/1.png', './res/image/idle/2.png', './res/image/idle/3.png'])]
            ActSprite[Act.ATTACK] = [
                AnimatedImage(['./res/image/attack/00.png', './res/image/attack/01.png', './res/image/attack/02.png', './res/image/attack/03.png', './res/image/attack/04.png']),
                AnimatedImage(['./res/image/attack/10.png', './res/image/attack/11.png', './res/image/attack/12.png', './res/image/attack/13.png', './res/image/attack/14.png', './res/image/attack/15.png']),
                AnimatedImage(['./res/image/attack/20.png', './res/image/attack/21.png', './res/image/attack/22.png', './res/image/attack/23.png', './res/image/attack/24.png', './res/image/attack/25.png'])
                ]
            ActSprite[Act.HURT] = [
                AnimatedImage(['./res/image/hurt/0.png', './res/image/hurt/1.png', './res/image/hurt/2.png'])
                ]
            Player.first = False
        super().__init__(scene, ActSprite[Act.IDLE][0], location, size)
        self._health = 100
        self.reset()
        self.effectOffset = (size[0]/2, 0)
        self.hpbar = HpDrawable(150, 30)
        self.alive = True
        self.level = 1
        self.act = Act.IDLE
        self.seeingRight = True
    
    def getAttacked(self, damage):
        if self._evade>0:
            self.showEffect('evade', 'Evade!')
            self._evade -= 1
        else:
            if self._shield >= damage:
                self._shield -= damage
                self.showEffect('defence', '-' + str(damage))
            else:
                if self._shield > 0:
                    damage -= self._shield
                    self._shield = 0
                self.health -= max(damage-self._armor, 0)
    def reset(self):
        self._shield = 0
        self._armor = 0
        self._power = 0
        self._evade = 0

    @property
    def evade(self):
        return self._evade
    @evade.setter
    def evade(self, newval):
        if newval<self._evade:
            self.showEffect('evade', '👁-'+str(self._evade - newval))
            self._evade = newval
        elif newval>self._evade:
            self.showEffect('evade', '👁+' + str(newval - self._evade))
            self._evade = newval

    @property
    def power(self):
        return self._power
    @power.setter
    def power(self, newval):
        newval = newval if newval>0 else 0
        if newval<self._power:
            self.showEffect('power', '💪-'+str(self._power - newval))
            self._power = newval
        elif newval>self._power:
            self.showEffect('power', '💪+'+str(abs(self._power - newval)))
            self._power = newval

    @property
    def armor(self):
        return self._armor
    @armor.setter
    def armor(self, newval):
        newval = newval if newval>0 else 0
        if newval<self._armor:
            self.showEffect('armor', '🛡-'+str(self._armor - newval))
            self._armor = newval
        elif newval>self._armor:
            self.showEffect('armor', '🛡+'+str(abs(self._armor - newval)))
            self._armor = newval

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, newval):
        if newval>100: newval = 100
        if newval<self._health:
            self.showEffect('hurt', self._health - newval)
            self._health = newval
        elif newval>self._health:
            self.showEffect('heal', '+'+str(newval - self._health))
            self._health = newval
        else:
            self.showEffect('nothing', 0)
        if self._health < 0: self._health = 0

    @property
    def shield(self):
        return self._shield

    @shield.setter
    def shield(self, newval):
        if newval<self._shield:
            self.showEffect('defence', self._shield - newval)
            self._shield = newval
        elif newval>self._shield:
            self.showEffect('defence', '+'+str(abs(self._shield - newval)))
            self._shield = newval

    def showEffect(self, effect, text):
        if type(text) != str: text = str(text)
        if effect == 'hurt':
            dmg = Dmg(self.scene, (self.location[0]+32, self.location[1]-32), text, QColor(255, 40, 40), 48)
            dmg.objid = self.scene.addObject(dmg)
        elif effect == 'heal':
            dmg = Dmg(self.scene, (self.location[0]+32, self.location[1]-32), text, QColor(40, 255, 40), 48)
            dmg.objid = self.scene.addObject(dmg)
        elif effect == 'defence':
            dmg = Dmg(self.scene, (self.location[0]+32, self.location[1]-32), text, QColor(200, 200, 200), 48)
            dmg.objid = self.scene.addObject(dmg)
        elif effect == 'nothing':
            dmg = Dmg(self.scene, (self.location[0]+32, self.location[1]-32), text, QColor(170, 170, 170), 48)
            dmg.objid = self.scene.addObject(dmg)
        elif effect == 'power':
            dmg = Dmg(self.scene, (self.location[0]-24, self.location[1]-32), text, QColor(255, 100, 100), 48)
            dmg.objid = self.scene.addObject(dmg)
        elif effect == 'armor':
            dmg = Dmg(self.scene, (self.location[0]-24, self.location[1]-32), text, QColor(200, 200, 250), 48)
            dmg.objid = self.scene.addObject(dmg)
        elif effect == 'evade':
            dmg = Dmg(self.scene, (self.location[0]-24, self.location[1]-32), text, QColor(0, 100, 250), 48)
            dmg.objid = self.scene.addObject(dmg)
    
    def draw(self, ctx):
        xoffset = 50
        yoffset = 25
        location = [self.location[0] - xoffset, self.location[1]-yoffset]
        size = [self.size[0] + xoffset*2, self.size[1]+yoffset*2]
        
        if self.drawable != None:
            if self.seeingRight:
                self.drawable.draw(ctx, location, size)
            else:
                self.drawable.draw(ctx, location, size, False)

        if self.drawable.animate(8/60):
            if self.act == Act.IDLE:
                self.setAct(Act.IDLE)
            elif self.act == Act.ATTACK:
                self.setAct(Act.IDLE)

        self.hpbar.draw(ctx, (self.location[0]+50-75, self.location[1]-70), (150*self.health/100, None))
        Text(str(self.health), QFont('D2Coding', 24), QColor(255, 255, 255)).draw(ctx, (self.location[0]+50-75+10, self.location[1]-70+26))
        if self._shield>0: Text('+'+str(self._shield), QFont('D2Coding', 24), QColor(200, 200, 200)).draw(ctx, (self.location[0]+50-75+100, self.location[1]-70+26)) 

    def setAct(self, act):
        self.drawable = random.choice(ActSprite[act])
        self.drawable.reset()

class Scroll(Object):
    def __init__(self, scene,  location, size):
        super().__init__(scene, ScrollDrawable(), location, size)
        self.blocks = []
        self.nowblock = None
    
    def addBlock(self, block):
        block.makeCode()
        self.blocks.append(block)

    def draw(self, ctx):
        super().draw(ctx)
        i = 0
        ystack = 0
        for block in self.blocks:
            block.location = (self.location[0] + 20, self.location[1] + 20 + ystack)
            block.draw(ctx)
            if i == self.nowblock:
                block.drawWrap(ctx)
            ystack += block.size[1] + 20
            i += 1

class Dmg(Object):
    def __init__(self, scene, location, text, color, size):
        super().__init__(scene, Text(text, QFont('D2Coding', size), color), location, (100, 50))
        self.lifetime = -15
    def update(self):
        self.lifetime += 1
        if self.lifetime>0:
            self.location = (self.location[0], self.location[1]-(55 - self.lifetime)/7)
        if self.lifetime>40:
            self.scene.removeObject(self.objid)
    def draw(self, ctx):
        if self.lifetime>0:
            super().draw(ctx)

class Block(Object):
    def __init__(self, scene, location, code = []):
        super().__init__(scene, BlockDrawable(), location, (300, 180))
        self.code = code
        self.fontSize = 16
        self.lineSpace = 1.5
        self.text = ''
        self.codeDrawable = CodeDrawable()
        self.makeCode()

    def draw(self, ctx):
        super().draw(ctx)
        self.codeDrawable.draw(ctx, (self.location[0]+30, self.location[1]+40))
    
    def drawWrap(self, ctx):
        self.drawable.drawWrap(ctx, self.location, self.size)

    def makeCode(self):
        self.text = ''
        for c in self.code:
            self.text += '    ' * c[1] + c[0]+'\n'
        self.codeDrawable.setCode(self.text)
        self.size = (self.size[0], 80-self.fontSize + (len(self.code)-1)*self.fontSize*self.lineSpace)

class Shop(Object):
    def __init__(self, scene, location = (1600, 0), size = (980, 900)):
        super().__init__(scene, ShopDrawable(), location, size)
        self.originLocation = location[:]
        self.offset = (0, 0)
        self.nowIndent = 0
        self.newBlock = ShopBlock(self, (340, 444))
        self.buyButton = ShopBuyButton(self, (660, 444), 'append()')
        self.locked = False
        self.lockBlocks = []
        self.entities = [
            ShopMoney(self, (0, 0)),
            ShopCodeButton(self, (20, 120), [('hello', 0, 1)], 2),
            ShopCodeButton(self, (340, 120), [('hello', 0, 0)], 2),
            ShopCodeButton(self, (660, 120), [('hello', 0, 0)], 1),
            ShopCodeButton(self, (20, 228), [('hello', 0, 0)], 4),
            ShopCodeButton(self, (340, 228), [('hello', 0, 0)], 5),
            ShopCodeButton(self, (660, 228), [('hello', 0, 0)], 1),
            ShopCodeButton(self, (20, 336), [('hello', 0, 0)], 2),
            ShopCodeButton(self, (340, 336), [('hello', 0, 0)], 3),
            ShopCodeButton(self, (660, 336), [('hello', 0, 0)], 4),
            self.newBlock,
            self.buyButton,
            ShopIndentButton(self, (20, 444), '---->'),
            ShopUnindentButton(self, (20, 544), '<----'),
            ShopShiftButton(self, (20, 644), 'shift()'),
            ShopUnshiftButton(self, (340, 644), 'unshift()'),
            ShopResetButton(self, (660, 544), 'reset()'),
            ShopRerollButton(self, (20, 752), 'reroll()'),
            ShopLevelupButton(self, (340, 752), 'level++'),
            ShopPopButton(self, (660, 644), 'pop()'),
            ShopLockButton(self, (660, 752), 'lock()')
        ]
        self.nowMoney = 2
        self.maxMoney = 2
        self.reroll()
    def update(self):
        super().update()
        self.location = (self.originLocation[0]+self.offset[0], self.originLocation[1]+self.offset[1])
        if self.scene.shopping and self.offset[0] > -1000:
            self.offset = (max(self.offset[0] - (1000 + self.offset[0])//20, -1000), self.offset[1])
        elif not self.scene.shopping and self.offset[0] < 0:
            self.offset = (min(self.offset[0] + (-self.offset[0]+20)//20, 0), self.offset[1])
        for entity in self.entities:
            entity.update()
    def onPress(self):
        super().onPress()
        for entity in self.entities:
            entity.onPress()
    def draw(self, ctx):
        super().draw(ctx)
        for entity in self.entities:
            entity.draw(ctx)
    def reroll(self):
        codes = Codes.giveCode(self.scene.player.level)
        i=1;
        for c in codes:
            self.entities[i] = ShopCodeButton(self, self.entities[i].offset, c.code, c.cost, c.category)
            i+=1
    def reset(self):
        self.newBlock.code = []
        self.newBlock.makeCode()
        self.nowMoney += self.newBlock.nowCost
        self.newBlock.nowCost = 0
        self.nowIndent = 0
        self.buyButton.cost = 0
        if self.locked:
            self.unlock()

    def lock(self):
        self.locked = True
        self.lockBlocks = self.entities[1:10]
    
    def unlock(self):
        self.locked = False
        i=1;
        for c in self.lockBlocks:
            self.entities[i] = c
            c.selected = False
            #self.entities[i] = ShopCodeButton(self, self.entities[i].offset, c.code, c.cost)
            i+=1

class ShopEntity(Object):
    def __init__(self, parent, drawable, offset, size):
        super().__init__(parent.scene, ShopButtonDrawable(), (parent.location[0]+offset[0], parent.location[1]+offset[1]), size)
        self.parent = parent
        self.offset = offset
        self.cost = None
    def update(self):
        super().update()
        self.location = (self.parent.location[0]+self.offset[0], self.parent.location[1]+self.offset[1])
    def draw(self, ctx):
        super().draw(ctx)
        if self.cost != None:
            CostDrawable(self.cost).draw(ctx, self.location)
class ShopBlock(ShopEntity):
    def __init__(self, parent, offset):
        super().__init__(parent, BlockDrawable(), offset, (300, 180))
        self.code = []
        self.fontSize = 16
        self.lineSpace = 1.5
        self.text = ''
        self.codeDrawable = CodeDrawable()
        self.makeCode()
        self.nowCost = 0

    def onPress(self):
        super().onPress()
        if self.isHover() and self.parent.scene.shopping:
            self.onClick()
    def onClick(self):
        pass

    def makeCode(self):
        self.text = ''
        for c in self.code:
            self.text += '    ' * c[1] + c[0]+'\n'
        self.size = (self.size[0], 80-self.fontSize + (max(1, len(self.code))-1)*self.fontSize*self.lineSpace)
        self.codeDrawable.setCode(self.text if len(self.text)>0 else '#empty')

    def draw(self, ctx):
        super().draw(ctx)
        self.codeDrawable.draw(ctx, (self.location[0]+30, self.location[1]+40))
class ShopMoney(ShopEntity):
    def __init__(self, parent, offset):
        super().__init__(parent, None, (offset[0], offset[1]), (980, 99))
        
    def draw(self, ctx):
        super().draw(ctx)
        for i in range(self.parent.maxMoney):
            ShopMoneyDrawable().draw2(ctx, (self.location[0] + 98*i, self.location[1]), (98, 98))
            if i<self.parent.nowMoney:
                ShopMoneyDrawable().draw(ctx, (self.location[0] + 98*i, self.location[1]), (98, 98))

class ShopButton(ShopEntity):
    def __init__(self, parent, offset):
        super().__init__(parent, ShopButtonDrawable(), offset, (300, 88))
    def onPress(self):
        super().onPress()
        if self.isHover():
            self.onClick()
    def onClick(self):
        pass
class ShopCodeButton(ShopButton):
    def __init__(self, parent, offset, code, cost, category=10):
        super().__init__(parent, offset)
        self.drawable = ShopButtonDrawable(category)
        self.codeDrawable = CodeDrawable()
        self.code = code
        self.text = ''
        self.makeCode()
        self.lineSpace = 1.5
        self.cost = cost
        self.selected = False
        self.sold = False
        self.category = category
    def makeCode(self):
        self.text = ''
        for c in self.code:
            self.text += '    ' * c[1] + c[0] + '\n'
        self.codeDrawable.setCode(self.text)
    def draw(self, ctx):
        super().draw(ctx)
        self.codeDrawable.draw(ctx, (self.location[0]+30, self.location[1]+40))
        if self.sold:
            self.drawable.drawSold(ctx, self.location, self.size)
        elif self.selected:
            self.drawable.drawWrap(ctx, self.location, self.size)
        if self.cost != None:
            CostDrawable(self.cost).draw(ctx, self.location)
    def onClick(self):
        if self.parent.nowIndent != 0 or self.code[-1][2] == 1:
            if self.parent.nowMoney >= self.cost and not self.selected and not self.sold:
                self.parent.newBlock.nowCost += self.cost
                self.parent.nowMoney -= self.cost
                for code in self.code:
                    self.parent.newBlock.code.append((code[0], code[1]+self.parent.nowIndent))
                self.parent.newBlock.makeCode()
                self.parent.nowIndent = self.code[-1][1] + self.parent.nowIndent + code[2]
                self.parent.buyButton.cost = self.parent.newBlock.nowCost   
                self.parent.buyButton.selected.append(self)
                self.selected = True
class ShopTextButton(ShopButton):
    def __init__(self, parent, offset, text=''):
        super().__init__(parent, offset)
        self.size = (300, 88)
        self.text = text
        self.fontSize = 26
    def draw(self, ctx):
        super().draw(ctx)
        Text(self.text, QFont('NotoMono', self.fontSize), QColor(255, 255, 255)).draw(ctx, (30+self.location[0], self.location[1] + self.size[1]//2 + self.fontSize//2))
class ShopBuyButton(ShopTextButton):
    def __init__(self, parent, offset, text):
        super().__init__(parent, offset, text)
        self.cost = 0
        self.selected = []
    def onClick(self):
        super().onClick()
        if len(self.parent.newBlock.code)>0:
            self.parent.nowIndent = 0
            self.parent.newBlock.nowCost = 0
            self.scene.scroll.addBlock(Block(self.scene, (40, 40), self.parent.newBlock.code))
            
            self.scene.sock.send(json.dumps((0, self.parent.newBlock.code)))

            self.parent.newBlock.code = []
            while len(self.selected):
                self.selected.pop().sold = True
            self.parent.newBlock.makeCode()
            self.cost = 0
class ShopUnindentButton(ShopTextButton):
    def onClick(self):
        super().onClick()
        self.parent.nowIndent = max(0, self.parent.nowIndent-1)
class ShopIndentButton(ShopTextButton):
    def onClick(self):
        super().onClick()
        self.parent.nowIndent = self.parent.nowIndent+1
class ShopShiftButton(ShopTextButton):
    def onClick(self):
        super().onClick()
        scr = self.parent.scene.scroll.blocks
        if len(scr)>1:
            self.parent.scene.scroll.blocks = [scr[-1]] + scr[:-1]
            self.scene.sock.send(json.dumps((1, 0)))
class ShopUnshiftButton(ShopTextButton):
    def onClick(self):
        super().onClick()
        scr = self.parent.scene.scroll.blocks
        if len(scr)>1:
            self.parent.scene.scroll.blocks = scr[1:] + [scr[0]]
            self.scene.sock.send(json.dumps((2, 0)))
class ShopPopButton(ShopTextButton):
    def onClick(self):
        super().onClick()
        scr = self.parent.scene.scroll.blocks
        if len(scr)>0:
            self.parent.scene.scroll.blocks.pop(0)
            self.scene.sock.send(json.dumps((3, 0)))
class ShopResetButton(ShopTextButton):
    def __init__(self, parent, offset, text=''):
        super().__init__(parent, offset, text=text)
        self.size = (300, 80)
    def onClick(self):
        super().onClick()
        self.reset()
        while len(self.parent.buyButton.selected):
            self.parent.buyButton.selected.pop().selected = False
    def reset(self):
        self.parent.reset()
class ShopRerollButton(ShopTextButton):
    def __init__(self, parent, offset, text=''):
        super().__init__(parent, offset, text=text)
        self.cost = 1
    def onClick(self):
        super().onClick()
        if self.parent.nowMoney >= self.cost:
            self.parent.nowMoney -= self.cost
            self.parent.reroll()
class ShopLevelupButton(ShopTextButton):
    def __init__(self, parent, offset, text=''):
        super().__init__(parent, offset, text=text)
        self.cost = 1
    def onClick(self):
        super().onClick()
        if self.cost != None:
            if self.parent.nowMoney >= self.cost:
                self.parent.nowMoney -= self.cost
                self.parent.scene.player.level += 1
                self.cost = self.parent.scene.player.level * 2 - 1
                self.scene.sock.send(json.dumps((4, self.parent.scene.player.level)))
            if self.parent.scene.player.level>=5:
                self.cost = None
                self.text = "MAX"        
class ShopLockButton(ShopTextButton):
    def __init__(self, parent, offset, text=''):
        super().__init__(parent, offset, text=text)
    def onClick(self):
        super().onClick()
        if self.parent.locked:
            self.parent.unlock()
        else:
            self.parent.lock()
    def draw(self, ctx):
        super().draw(ctx)
        if self.parent.locked:
            self.drawable.drawWrap(ctx, self.location, self.size)
class Clock(Object):
    def __init__(self, scene, location, size = (400, 200)):
        super().__init__(scene, None, location, size)
        self.showTime = True
        self.message = 'Wait'
        self.time = 0

    def draw(self, ctx):
        super().draw(ctx)
        if self.showTime:
            Text(str(self.time), QFont('NotoMono', 48), QColor(255, 255, 255)).draw(ctx, self.location)
        else:
            Text(self.message, QFont('NotoMono', 48), QColor(255, 255, 255)).draw(ctx, self.location)