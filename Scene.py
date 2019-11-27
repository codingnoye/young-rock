import time

from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint

from Object import *
from Drawable import *

import threading

class Scene:
    def __init__(self):
        self.objects = []
        self.mouse = (0, 0)
        self.dragging = False

    def update(self):
        for obj in self.objects:
            if obj != None:
                obj.update()

    def draw(self, ctx):
        for obj in self.objects:
            if obj != None:
                obj.draw(ctx)

    def addObject(self, obj):
        self.objects.append(obj)
        return len(self.objects)-1
    
    def removeObject(self, objid):
        if objid != None:
            self.objects[objid] = None

    def event(self, e):
        for obj in self.objects:
            if obj != None:
                obj.event(e)

class TestScene(Scene):
    def __init__(self):
        super().__init__()

        self.scroll = Scroll(self, (20, 20), (340, 860))
        self.scroll.objid = self.addObject(self.scroll)

        self.enemyScroll = Scroll(self, (1240, 20), (340, 860))
        self.enemyScroll.objid = self.addObject(self.enemyScroll)

        self.player = Player(self, (450, 700), (100, 100))
        self.player.objid = self.addObject(self.player)

        self.enemy = Player(self, (1050, 700), (100, 100))
        self.enemy.objid = self.addObject(self.enemy)

        self.shopping = True
        self.shop = Shop(self)
        self.shop.objid = self.addObject(self.shop)

        self.scroll.addBlock(Block(self, (40, 40), [
            ('for i in range(3):', 0),
            ('attack(3)', 1),
            ('player.health += 5', 0),
            ('player.evade = 2', 0)
            ]))

        self.scroll.addBlock(Block(self, (40, 40), [
            ('for i in range(2):', 0),
            ('defence(4)', 1)
            ]))
        
        self.enemyScroll.addBlock(Block(self, (40, 40), [
            ('for i in range(3):', 0),
            ('attack(3)', 1),
            ('player.health += 5', 0)
            ]))

        self.enemyScroll.addBlock(Block(self, (40, 40), [
            ('for i in range(2):', 0),
            ('attack(6)', 1)
            ]))

        self.goShopping()

    def goShopping(self):
        self.shopping = True
        self.shopClock = Clock(self, (400, 50))
        self.shopClockId = self.addObject(self.shopClock)
        self.shop.nowMoney = self.shop.maxMoney
        thread = threading.Thread(target=self.shoppingThread, args=())
        thread.start()

    # @thread
    def shoppingThread(self):
        starttime = time.time()
        nowtime = time.time()
        while nowtime - starttime < 15:
            nowtime = time.time()
            self.shopClock.time = int(15 - (nowtime - starttime))
            time.sleep(0.2)
        self.removeObject(self.shopClockId)
        self.shopping = False
        self.shop.resetButton.reset()
        self.startBattle(True)

    def draw(self, ctx):
        super().draw(ctx)
        Text(str(self.mouse), QFont('D2Coding', 32), QColor(255, 255, 255)).draw(ctx, (50, 50))

    def event(self, e):
        super().event(e)
    
    def blockUse(self, block, isMine):
        execText = ''
        for line in block.code:
            execText += '    '*line[1] + 'time.sleep(0.4)' + '\n'
            execText += '    '*line[1] + line[0] + '\n'
        
        if isMine:
            self.sandbox(self.player, self.enemy, execText)
        else:
            self.sandbox(self.enemy, self.player, execText)

    # @thread
    def sandbox(self, player, enemy, text):
        def attack(val):
            enemy.getAttacked(val)
        def defence(val):
            player.shield += val
        try:
            exec(text, globals(), locals())
        except SyntaxError:
            pass

    def startBattle(self, first):
        thread = threading.Thread(target=self.battle, args=([first]))
        thread.start()

    # @thread
    def battle(self, first):
        myturn = first
        blocki = [0, 0]
        while blocki[0] < len(self.scroll.blocks) or blocki[1] < len(self.enemyScroll.blocks):
            player = self.player if myturn else self.enemy
            scroll = self.scroll if myturn else self.enemyScroll
            pi = 0 if myturn else 1

            player.shield = 0
            player.evade = 0
            if blocki[pi] < len(scroll.blocks):
                i = blocki[pi]
                scroll.nowblock = i
                self.blockUse(scroll.blocks[i], myturn)
                time.sleep(1)
                scroll.nowblock = None

            blocki[pi] += 1
            myturn = not myturn
        #battle end
        self.goShopping()

