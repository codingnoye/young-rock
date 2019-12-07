import sys
inp = input()
res = ''
nextUpper = False
isJava = None
def error():
    print('Error!')
    sys.exit(0)
if inp[0] == '_' or inp[0]<'a':
    error()
for c in inp:
    #print(c, isJava)
    if c<'A' or 'z'<c or ('Z'<c and c<'a' and c!='_'):
        error()
    elif c=='_':
        if isJava == True: error()
        if nextUpper == True: error()
        nextUpper = True
        isJava = False
    elif 'A'<=c and c<'a':
        if isJava == False: error()
        res+='_'+c.lower()
        isJava = True
    elif nextUpper:
        if isJava == True: error()
        res += c.upper()
        nextUpper = False
        isJava = False
    else:
        res+=c
if nextUpper:
    error()
print(res)