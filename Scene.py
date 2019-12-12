import time

from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QPen, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint

from Object import *
from Drawable import *

import threading
import Socket

import json

ctx = dict()

class Scene:
    game = None
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

class TitleScene(Scene):
    def __init__(self):
        super().__init__()
        Scene.game.setStyleSheet("background-color:rgb(150, 150, 150);");
        self.status = ""
        self.addObject(Button(self, "HOST", self.host, (400, 500)))
        self.addObject(Button(self, "JOIN", self.join, (900, 500)))

    def host(self):
        sock = Socket.Server()
        print('i am server')
        self.sock = sock
        ctx['imHost'] = True
        ctx['sock'] = sock
        sock.connect()
        Scene.game.setScene(MainScene())
    
    def join(self):
        sock = Socket.Client()
        print('i am client')
        self.sock = sock
        ctx['imHost'] = False
        ctx['sock'] = sock
        sock.connect()
        Scene.game.setScene(MainScene())

class MainScene(Scene):
    def __init__(self):
        super().__init__()
        #Scene.game.setStyleSheet("background-color:rgb(150, 150, 150);");
        #Scene.game.setStyleSheet("background-image: url(:./res/image/background.png);");
        self.backgroundPixmap = QPixmap('./res/image/background.png')

        self.sock = ctx['sock']
        self.sock.recv(self.sockRecv)

        self.scroll = Scroll(self, (20, 20), (340, 860))
        self.scroll.objid = self.addObject(self.scroll)

        self.enemyScroll = Scroll(self, (1240, 20), (340, 860))
        self.enemyScroll.objid = self.addObject(self.enemyScroll)

        self.player = Player(self, (450, 700), (100, 100))
        self.player.objid = self.addObject(self.player)

        self.enemy = Player(self, (1050, 700), (100, 100))
        self.enemy.seeingRight = False
        self.enemy.objid = self.addObject(self.enemy)
        self.enemyOrigin = self.enemy.location[:]

        self.shopping = True
        self.shop = Shop(self)
        self.shop.objid = self.addObject(self.shop)
        
        self.turn = 0

        self.goShopping()

    def goShopping(self):
        self.shopping = True
        self.shopClock = Clock(self, (400, 50))
        self.shopClockId = self.addObject(self.shopClock)
        self.shop.reroll()
        self.shop.reset()
        self.shop.buyButton.selected = []
        self.shop.maxMoney += 1 if self.shop.maxMoney<10 else 0
        self.shop.nowMoney = self.shop.maxMoney
        thread = threading.Thread(target=self.shoppingThread, args=())
        thread.start()

    # @thread
    def shoppingThread(self):
        starttime = time.time()
        nowtime = time.time()
        timeLimit = 15 + min(20, 4*self.turn)

        while nowtime - starttime < timeLimit:
            nowtime = time.time()
            self.shopClock.time = int(timeLimit - (nowtime - starttime))
            if self.turn != 0:
                self.enemy.setAct(Act.RUN)
                self.enemy.seeingRight = True
                self.enemy.location = (self.enemy.location[0] + 7, self.enemy.location[1])
            time.sleep(1/60)
        self.enemy.seeingRight = False
        self.removeObject(self.shopClockId)
        self.shopping = False
        self.turn += 1
        self.startBattle(ctx['imHost'])

    def draw(self, ctx):
        ctx[1].drawPixmap(0, 0, self.game.width(), self.game.height(), self.backgroundPixmap)
        super().draw(ctx)
        Text(str(self.mouse), QFont('D2Coding', 32), QColor(255, 255, 255)).draw(ctx, (50, 50))

    def event(self, e):
        super().event(e)
    
    def blockUse(self, block, isMine):
        execText = ''
        for line in block.code:
            execText += '    '*line[1] + line[0] + '\n'
        
        if isMine:
            self.sandbox(self.player, self.enemy, execText)
        else:
            self.sandbox(self.enemy, self.player, execText)

    # @thread
    def sandbox(self, player, enemy, text):
        def attack(val):
            player.setAct(Act.ATTACK) if val<10 else player.setAct(Act.HATTACK)
            time.sleep(player.df*3)
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
        self.enemy.setAct(Act.RUN)
        self.enemy.location = self.enemyOrigin[:]
        
        for i in range(60):
            self.enemy.location = (self.enemy.location[0] - 7, self.enemy.location[1])
            time.sleep(1/60)
        myturn = first
        blocki = [0, 0]
        while blocki[0] < len(self.scroll.blocks) or blocki[1] < len(self.enemyScroll.blocks):
            player = self.player if myturn else self.enemy
            scroll = self.scroll if myturn else self.enemyScroll
            pi = 0 if myturn else 1

            if blocki[pi] < len(scroll.blocks):
                i = blocki[pi]
                scroll.nowblock = i
                self.blockUse(scroll.blocks[i], myturn)
                time.sleep(1)
                scroll.nowblock = None

            blocki[pi] += 1
            myturn = not myturn
        #battle end
        self.player.reset()
        self.enemy.reset()
        self.goShopping()

    def sockRecv(self, recv):
        code, data = json.loads(recv)
        if code == 0: # buy
            self.enemyScroll.addBlock(Block(self, (40, 40), data))
        elif code == 1: # shift
            scr = self.enemyScroll.blocks
            self.enemyScroll.blocks = [scr[-1]] + scr[:-1]
        elif code == 2: # unshift
            scr = self.enemyScroll.blocks
            self.enemyScroll.blocks = scr[1:] + [scr[0]]
        elif code == 3: # pop
            self.enemyScroll.blocks.pop(0)
        elif code == 4: # level
            self.enemy.level = data