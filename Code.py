class Code:
    codelist = []
    def __init__(self, code, cost):
        self.code = code
        self.cost = cost
        self.id = len(Code.codelist)
        Code.codelist.append(self)
    def __repr__(self):
        return f'Code({self.code}, {self.cost})'


Code([('attack(1)', 0, 0)], 0)      
Code([('player.power+=1', 0, 0)], 1)
Code([('player.power-=1', 0, 0),('player.armor+=1', 0, 0)], 1)
Code([('defence(2)', 0, 0)], 1)
Code([('attack(player.power)', 0, 0)], 2)
Code([('attack(3)', 0, 0)], 2)
Code([('player.power, player.armor = player.armor, player.power', 0, 0)], 2)
Code([('player.power = 3', 0, 0)], 2)
Code([('attack(player.armor*2)', 0, 0)], 2)
Code([('defence(player.power)', 0, 0)], 2)
Code([('defence(4)', 0, 0)], 2)
Code([('player.power+=1', 0, 0)], 2)
Code([('enemy.power = player.power', 0, 0)], 3)
Code([('player.armor+=1', 0, 0)], 3)
Code([('defence(player.shield)', 0, 0)], 3)
Code([('player.armor = 3', 0, 0)], 3) 
Code([('attack(player.power*2)', 0, 0)], 3)
Code([('player.power+=player.power', 0, 0)], 4)
Code([('attack(enemy.power*2)', 0, 0)], 4)
Code([('defence(10-player.power)', 0, 0)], 4)
Code([('defence(player.power**2)', 0, 0), ('player.power-=1', 0, 0)], 4)
Code([('player.power *= 2', 0, 0)], 5)
Code([('attack(i*2)', 0, 0)], 5)
Code([('defence(i*3)', 0, 0), ('player.health-=1', 0, 0)], 5)
Code([('player.power, player.armor = int(2.5*armor), 0', 0, 0)], 5)
Code([('enemy.health-=5', 0, 0)], 5)  

Code([('if player.health>90:', 0, 1)], 0)  
Code([('if player.level==1:', 0, 1)], 0)
Code([('if player.power==0:', 0, 1)], 1)
Code([('if enemy.health%2==0:', 0, 1)], 1)
Code([('if player.power>2:', 0, 1)], 1)
Code([('if enemy.health<90:', 0, 1)], 1)
Code([('for i in range(2):', 0, 1)], 2)
Code([('else:', 0, 1)], 2)
Code([('if True:', 0, 1)], 2)
Code([('for i in range(enemy.level):', 0, 1)], 3)
Code([('for i in range(palyer.level):', 0, 1)], 3)
Code([('for i in range(4):', 0, 1),('if player.health<50:', 1, 2)], 3)
Code([('for j in range(i):', 0, 1)], 3)
Code([('for i in range(3):', 0, 1)], 4)
Code([('if player.power<3:', 0, 1), ('for i in range(5):', 0, 1)], 4)
Code([('for i in range(5):', 0, 1), ('enemy.health -= 2', 0, 0)], 4)
Code([('for i in range(3, 6):', 0, 1)], 5)
Code([('for i in range(player.level):', 0, 1)], 4)
Code([('if enemy.shield>10:', 0, 1), ('for i in range(6):', 0, 1)], 5)
Code([('while enemy.health%7==0:', 0, 1)], 5)

if __name__ == "__main__":
    print(Code.codelist)