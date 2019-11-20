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

        self.block = Block(self, (40, 40), [
            ('for i in range(3):', 0),
            ('attack(3)', 1),
            ('player.health += 5', 0)
            ])
        self.block.objid = self.addObject(self.block)
    
    def draw(self, ctx):
        super().draw(ctx)
        Text(str(self.mouse), QFont('D2Coding', 32), QColor(255, 255, 255)).draw(ctx, (50, 50))
    
    def blockUse(self, block, isMine):
        execText = ''
        for line in block.code:
            execText += '    '*line[1] + 'time.sleep(0.15)' + '\n'
            execText += '    '*line[1] + line[0] + '\n'
        thread = threading.Thread(target=self.sandbox, args=([self.player, self.enemy, execText] if isMine else [self.enemy, self.player, execText]))
        thread.start()

    # @thread
    def sandbox(self, player, enemy, text):
        def attack(val):
            enemy.getAttacked(val)
        def defence(val):
            enemy.getAttacked(val)
        exec(text, globals(), locals())

    # @thread
    def battle(self, first):
        myturn = first
        blocki = [-1, -1]
        while blocki[0] < len(self.player.blocks) or blocki[1] < len(self.enemy.blocks):
            player = self.player if myturn else self.enemy
            pi = 0 if myturn else 1

            player.shield = 0
            if blocki[pi] < len(player.blocks):
                blocki[pi] += 1
                i = blocki[pi]
                player.nowblock = i
                self.blockUse(player.blocks[i], myturn)
                player.nowblock = None
            myturn = not myturn
            
