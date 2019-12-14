import random

class Code:
    codelist = []
    def __init__(self, code, cost, category = 10):
        self.code = code
        self.cost = cost
        self.category = category
        self.id = len(Code.codelist)
        Code.codelist.append(self)
    def __repr__(self):
        return f'Code({self.code}, {self.cost})'

def giveCode(cost):
    return sorted(random.sample(list(filter(lambda c: c.cost<=cost, Code.codelist)), 9), key=lambda x:x.category)
# 0코
Code([('attack(1)', 0, 0)], 0)
Code([('defence(1)', 0, 0)], 0)
# 1코
Code([('player.power=1', 0, 0)], 1)
Code([('player.power-=1', 0, 0), ('player.armor+=1', 0, 0)], 1)
Code([('player.armor-=1', 0, 0), ('player.power+=1', 0, 0)], 1)
Code([('attack(2)', 0, 0)], 1)
Code([('defence(2)', 0, 0)], 1)
Code([('attack(2)', 0, 0)], 1)
Code([('defence(2)', 0, 0)], 1)
# 2코
Code([('attack(player.power)', 0, 0)], 2)
Code([('attack(player.power)', 0, 0)], 2)
Code([('player.evade=1', 0, 0)], 2)
Code([('attack(3)', 0, 0)], 2)
Code([('attack(2, 2)', 0, 0)], 2)
Code([('swap=player.armor', 0, 0), ('player.power=player.armor', 0, 0), ('player.armor=swap', 0, 0)], 2, 11)
Code([('player.power=3', 0, 0)], 2)
Code([('defence(player.power)', 0, 0)], 2)
Code([('defence(3)', 0, 0)], 2)
Code([('player.power+=1', 0, 0)], 2)
Code([('player.armor+=1', 0, 0)], 2)
Code([('attack(j)', 0, 0)], 4, 11)
# 3코
Code([('attack(1, 1)', 0, 0), ('attack(1, 1)', 0, 0)], 3)
Code([('player.armor+=2', 0, 0)], 3)
Code([('player.power+=2', 0, 0)], 3)
Code([('player.evade=2', 0, 0)], 3)
Code([('defence(player.shield)', 0, 0)], 3)
Code([('enemy.power = player.power', 0, 0)], 3, 11)
Code([('player.power = enemy.power', 0, 0)], 3, 11)
Code([('attack(enemy.power*2)', 0, 0)], 3, 11)
Code([('attack(player.power)', 0, 0), ('attack(player.power)', 0, 0)], 3)
Code([('enemy.health-=1', 0, 0)], 3)
# 4코
Code([('player.power+=3', 0, 0)], 4)
Code([('player.armor+=3', 0, 0)], 4)
Code([('player.evade+=1', 0, 0)], 4)
Code([('attack(enemy.shield)', 0, 0)], 4, 11)
Code([('defence(10-player.power)', 0, 0)], 4)
Code([('defence(player.power**2)', 0, 0), ('player.power-=1', 0, 0)], 4, 11)
Code([('attack(j*2)', 0, 0)], 4, 11)
Code([('player.power=2*player.armor', 0, 0), ('player.armor=0', 0, 0)], 4, 11)
Code([('attack(player.power*2)', 0, 0)], 4)
Code([('enemy.health-=2', 0, 0)], 4)
Code([('player.evade+=1', 0, 0), ('player.shield=0', 0, 0)], 4)
# 5코
Code([('player.power*=2', 0, 0)], 5, 11)
Code([('player.armor+=5', 0, 0)], 5)
Code([('attack(i*2)', 0, 0)], 5)
Code([('defence(i*3)', 0, 0), ('player.health-=1', 0, 0)], 5)
Code([('enemy.health-=4', 0, 0)], 5)
Code([('player.armor=6', 0, 0)], 5)  
Code([('enemy.health=', 0, 0)], 5, 11)  

# 0코
Code([('if player.health<50:', 0, 1)], 0, 0)
Code([('if player.health==100:', 0, 1)], 0, 0)
# 1코
Code([('if player.health>90:', 0, 1)], 1, 0)
Code([('if player.power==0:', 0, 1)], 1, 0)
Code([('if enemy.health<90:', 0, 1)], 1, 0)
Code([('if player.power>=1:', 0, 1)], 1, 0)
Code([('else:', 0, 1)], 2, 1)
# 2코
Code([('for i in range(2):', 0, 1)], 2, 1)
Code([('for j in range(2):', 0, 1)], 2, 1)
Code([('if True:', 0, 1)], 2, 0)
# 3코
Code([('for j in range(i):', 0, 1)], 3, 1)
Code([('for i in range(3):', 0, 1)], 3, 1)
Code([('for j in range(3, 5):', 0, 1)], 3, 1)
Code([('for i in range(4):', 0, 1), ('if player.health<50:', 1, 1)], 3, 2)
# 4코
Code([('for i in range(4):', 0, 1)], 4, 2)
Code([('for i in range(enemy.level):', 0, 1)], 4, 1)
Code([('for i in range(player.level):', 0, 1)], 4, 1)
Code([('if player.power<3:', 0, 1), ('for i in range(5):', 1, 1)], 4, 2)
Code([('for i in range(5):', 0, 1), ('player.health -= 2', 1, 0)], 4, 2)
# 5코
Code([('for i in range(5):', 0, 1)], 5, 2)
Code([('for i in range(3, 6):', 0, 1)], 5, 1)
Code([('if enemy.shield>10:', 0, 1), ('for i in range(6):', 1, 1)], 5, 2)
Code([('while enemy.health%7==0:', 0, 1), ('player.health-=2', 1, 0)], 5, 3)
if __name__ == "__main__":
    print(giveCode(5))