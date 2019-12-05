import random

class Code:
    codelist = []
    def __init__(self, code, cost):
        self.code = code
        self.cost = cost
        self.id = len(Code.codelist)
        Code.codelist.append(self)
    def __repr__(self):
        return f'Code({self.code}, {self.cost})'

def giveCode(cost):
    return random.sample(list(filter(lambda c: c.cost<=cost, Code.codelist)), 9)

Code([('attack(2)', 0, 0)], 1)
Code([('defence(2)', 0, 0)], 1)
Code([('attack(2)', 0, 0)], 1)
Code([('defence(2)', 0, 0)], 1)
Code([('attack(player.power)', 0, 0)], 2)
Code([('attack(3)', 0, 0)], 2)
Code([('defence(player.power)', 0, 0)], 2)
Code([('defence(4)', 0, 0)], 2)
Code([('player.power+=1', 0, 0)], 2)
Code([('player.armor+=1', 0, 0)], 3)
Code([('player.power+=2', 0, 0)], 3)
Code([('defence(player.shield)', 0, 0)], 3)
Code([('attack(player.power*2)', 0, 0)], 3)
Code([('player.power+=3', 0, 0)], 4)
Code([('attack(enemy.power*2)', 0, 0)], 4)
Code([('defence(10-player.power)', 0, 0)], 4)
Code([('defence(player.power**2)', 0, 0), ('player.power-=1', 0, 0)], 4)
Code([('player.power *= 2', 0, 0)], 5)
Code([('attack(i*2)', 0, 0)], 5)
Code([('defence(i*3)', 0, 0), ('player.health-=1', 0, 0)], 5)

Code([('if player.health<50:', 0, 1)], 0)
Code([('if player.health==100:', 0, 1)], 0)
Code([('if player.health>90:', 0, 1)], 1)
Code([('if player.power==0:', 0, 1)], 1)
Code([('if enemy.health<90:', 0, 1)], 1)
Code([('for i in range(2):', 0, 1)], 2)
Code([('if True:', 0, 1)], 2)
Code([('for j in range(i):', 0, 1)], 3)
Code([('for i in range(3):', 0, 1)], 4)
Code([('if player.power<3:', 0, 1), ('for i in range(5):', 1, 1)], 4)
Code([('for i in range(5):', 0, 1), ('player.health -= 2', 1, 0)], 4)
Code([('for i in range(3, 6):', 0, 1)], 5)
Code([('if enemy.shield>10:', 0, 1), ('for i in range(6):', 1, 1)], 5)

if __name__ == "__main__":
    print(giveCode(5))