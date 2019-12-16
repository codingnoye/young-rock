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
        self.backgroundPixmap = None

    def update(self):
        for obj in self.objects:
            if obj != None:
                obj.update()

    def draw(self, ctx):
        if self.backgroundPixmap != None: ctx[1].drawPixmap(0, 0, self.game.width(), self.game.height(), self.backgroundPixmap)
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

class IntroScene(Scene):
    def __init__(self):
        super().__init__()
        Scene.game.setStyleSheet("background-color:rgb(0, 0, 0);")
        n0 = IntroNaration(self, '영원한 젊음을 가져다 준다는 돌', (620, 500))
        self.addObject(n0)
        n1 = IntroNaration(self, 'Young Rock', (620, 500))
        n1.fontSize = 84
        self.addObject(n1)
        n2 = IntroNaration(self, '그 돌을 찾기 위해 온', (620, 500))
        self.addObject(n2)
        n3 = IntroNaration(self, '두 모험가의 승부가 시작된다.', (620, 500))
        self.addObject(n3)
        self.naration = [n0, n1, n2, n3]
        self.frame = 0

    def draw(self, ctx):
        super().draw(ctx)
        n0, n1, n2, n3 = self.naration
        timing = (300, 60, 90, 60, 60, 90, 60, 60, 90, 60, 60, 110, 90)
        now = 0
        if self.frame<sum(timing[:1]):
            pass

        elif self.frame<sum(timing[:2]):
            n0.alpha = min(n0.alpha+7, 255)
        elif self.frame<sum(timing[:3]):
            n0.alpha = 255
        elif self.frame<sum(timing[:4]):
            n0.alpha = max(n0.alpha-7, 0)

        elif self.frame<sum(timing[:5]):
            n1.alpha = min(n1.alpha+7, 255)
        elif self.frame<sum(timing[:6]):
            n1.alpha = 255
        elif self.frame<sum(timing[:7]):
            n1.alpha = max(n1.alpha-7, 0)
        
        elif self.frame<sum(timing[:8]):
            n2.alpha = min(n2.alpha+7, 255)
        elif self.frame<sum(timing[:9]):
            n2.alpha = 255
        elif self.frame<sum(timing[:10]):
            n2.alpha = max(n2.alpha-7, 0)
        
        elif self.frame<sum(timing[:11]):
            n3.alpha = min(n3.alpha+7, 255)
        elif self.frame<sum(timing[:12]):
            n3.alpha = 255
        elif self.frame<sum(timing[:13]):
            n3.alpha = max(n3.alpha-7, 0)

        else:
            Scene.game.setScene(TitleScene())

        self.frame+=1

    def event(self, e):
        super().event(e)
        if e=="press":
            Scene.game.setScene(TitleScene())

class TitleScene(Scene):
    def __init__(self):
        super().__init__()
        self.backgroundPixmap = QPixmap('./res/image/background.png')
        self.status = ""
        self.t = time.time()
        self.i = 0
        self.phase = 0
        self.ani = self.animate()
        threading.Thread(target=self.thread, daemon=True).start()

    def animate(self):
        self.playerImage = Object(self, Image('./res/image/idle/0.png'), (-100-700, 250), (800, 600))
        self.addObject(self.playerImage)
        self.titleImage = Object(self, Image('./res/image/title2.png'), (850, 80-480), (650, 400))
        def debugOn():
            if self.titleImage.isHover(): Scene.game.debug = True
        self.titleImage.onPress = debugOn
        self.addObject(self.titleImage)
        self.phase = 1
        yield None
        self.playerImage.location = (-100, 250)
        self.titleImage.location = (850,80)
        host = threading.Thread(target=self.host, daemon=True).start
        join = threading.Thread(target=self.join, daemon=True).start
        self.hostButton = TitleButton(self, "HOST", host, (1320+600, 550))
        self.addObject(self.hostButton)
        self.joinButton = TitleButton(self, "JOIN", join, (1320+600, 650))
        self.addObject(self.joinButton)
        self.phase = 2
        yield None
        self.phase = 3
        yield None
        self.hostButton.location = (1320, 550)
        self.joinButton.location = (1320, 650)
        self.phase = 4
        yield None

    def thread(self):
        ani = self.ani
        while True:
            if self.phase==0:
                ani.__next__()
            elif self.phase==1:
                self.i = max(0, self.i)
                self.playerImage.location = (self.playerImage.location[0] + 700/90, 250)
                self.titleImage.location = (850, self.titleImage.location[1] + 480/90)
                self.i+=1
                if self.i>=90:
                    ani.__next__()
            elif self.phase==2:
                self.i = max(90, self.i)
                self.i+=1
                if self.i>=120:
                    ani.__next__()
            elif self.phase==3:
                self.i = max(120, self.i)
                self.hostButton.location = (self.hostButton.location[0] - 600/60, 550)
                self.joinButton.location = (self.joinButton.location[0] - 600/60, 650)
                self.i+=1
                if self.i>=180:
                    ani.__next__()
                    break
            time.sleep(1/60)

    def event(self, e):
        super().event(e)
        if e=="press":
            if self.phase==1:
                self.ani.__next__()
                self.ani.__next__() 
            elif self.phase<4:
                self.ani.__next__() 

    def host(self):
        self.hostButton.text = "WAITING"
        self.hostButton.callback = None
        sock = Socket.Server()
        print('i am server')
        self.sock = sock
        ctx['imHost'] = True
        ctx['sock'] = sock
        sock.connect()
        Scene.game.setScene(MainScene())
    
    def join(self):
        self.joinButton.text = "WAITING"
        self.joinButton.callback = None
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
        self.backgroundPixmap = QPixmap('./res/image/background.png')

        self.sock = ctx['sock']
        self.sock.recv(self.sockRecv)

        self.scroll = Scroll(self, (20, 20), (340, 860))
        self.scroll.objid = self.addObject(self.scroll)

        self.enemyScroll = Scroll(self, (1240, 20), (340, 860))
        self.enemyScroll.objid = self.addObject(self.enemyScroll)

        if Scene.game.debug:
            #self.scroll.addBlock(Block(self, (0, 0), [('player.power=3', 0), ('player.evade=3', 0), ('player.armor=3', 0)]))
            self.scroll.addBlock(Block(self, (0, 0), [('for i in range(3):', 0), ('attack(2)', 1)]))
            self.scroll.addBlock(Block(self, (0, 0), [('for i in range(3):', 0), ('player.power+=3', 1), ('attack(player.power)', 1)]))
            self.scroll.addBlock(Block(self, (0, 0), [('for i in range(2):', 0), ('enemy.health-=4', 1)]))

            self.enemyScroll.addBlock(Block(self, (0, 0), [('if enemy.health>90:', 0), ('player.evade = 1', 1), ('defence(2)', 1)]))
            self.enemyScroll.addBlock(Block(self, (0, 0), [('for i in range(2):', 0), ('player.armor+=2', 1), ('player.power+=1', 1)]))
            self.enemyScroll.addBlock(Block(self, (0, 0), [('for i in range(3,5):', 0), ('for j in range(i):', 1), ('defence(4)', 2)]))
            

        self.player = Player(self, (450, 700), (100, 100))
        self.player.objid = self.addObject(self.player)

        self.enemy = Player(self, (1050, 700), (100, 100))
        self.enemy.seeingRight = False
        self.enemy.objid = self.addObject(self.enemy)
        self.enemyOrigin = self.enemy.location[:]

        self.player.enemy = self.enemy
        self.enemy.enemy = self.player

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
        if Scene.game.debug: self.shop.maxMoney = 100
        self.shop.nowMoney = self.shop.maxMoney
        thread = threading.Thread(target=self.shoppingThread, args=(), daemon=True)
        thread.start()

    # @thread
    def shoppingThread(self):
        starttime = time.time()
        nowtime = time.time()
        timeLimit = 15 + min(25, 5*self.turn)

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
        super().draw(ctx)
        #if Scene.game.debug: Text(str(self.mouse), QFont('D2Coding', 32), QColor(255, 255, 255)).draw(ctx, (50, 50))

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
        
        if self.player.health == 0:
            Scene.game.won = False
            Scene.game.setScene(GameOverScene())
        elif self.enemy.health == 0:
            Scene.game.won = True
            Scene.game.setScene(GameOverScene())

    # @thread
    def sandbox(self, player, enemy, text):
        player.nowTurn = True
        def attack(*vals):
            if len(vals) == 1:
                val = vals[0]
                player.setAct(Act.ATTACK) if val<10 else player.setAct(Act.HATTACK)
                time.sleep(player.df*3)
                enemy.getAttacked(val)
            else: 
                for val in vals: attack(val)
        def defence(val):
            player.shield += val
        try:
            exec(text, globals(), locals())
        except:
            player.setHealth(player.health - 10, False)
        player.nowTurn = False

    def startBattle(self, first):
        thread = threading.Thread(target=self.battle, args=([first]), daemon=True)
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
        #print('"'+recv+'"')
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

class GameOverScene(Scene):
    def __init__(self):
        super().__init__()
        Scene.game.setStyleSheet("background-color:rgb(0, 0, 0);")
        won = IntroNaration(self, '이겼다' if Scene.game.won else '졌다', (620, 500))
        self.addObject(won)
        won.alpha = 255
