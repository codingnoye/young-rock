class Lobby:
    def __init__(self):
        self.players = 0
    def join(self):
        self.players += 1
        return self.players-1

class Player:
    def __init__(self):
        self.hp = 100
        self.blocks = []
    def addBlock(self, block):
        self.blocks.append(block)
        return len(self.blocks)-1
    def popBlock(self, blockid):
        self.blocks.pop(blockid)

class Game:
    def __init__(self, lobby):
        self.players = [Player() for _ in range(8)]
