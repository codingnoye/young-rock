power = 10

def attack(dmg):
    print(f'attack {dmg}dmg')

def executer(lines):
    # return isleft
    pended = []
    lastindent = 0
    for i in range(len(lines)):
        line = lines[i]
        if lastindent != 0 and line[1] == 0:
            source = ''
            for pline in pended:
                source += ('    ' * pline[1]) + pline[0] + '\n'
            exec(source, globals(), locals())
            pended = []
            yield True
        pended.append(line)
        lastindent = line[1]
    source = ''
    for pline in pended:
        source += '    ' * pline[1] + pline[0] + '\n'
    exec(source, globals(), locals())
    yield False

lines = [
    ('for i in range(3):', 0),
    ('attack(5)', 1),
    ('attack(3)', 1),
    ('attack(4)', 0)
]

for more in executer(lines):
    if not more: break
    input()

