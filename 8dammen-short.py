def kannSchlagen(dammen,position):
    dpos = dammen[position]
    for p in range(0,position):
        if dammen[p]==dpos or dammen[p]+(position-p)==dpos or dammen[p]-(position-p)==dpos:
            return True
    return False

def testPos(dammen,pos):
    for i in range(0,8):
        dammen[pos] = i
        if pos>0 and kannSchlagen(dammen,pos):
            continue
        else:
            if pos==7:
                print(f"found solution {dammen}")
            else:
                testPos(dammen,pos+1)


print("start")
dammen = [0,0,0,0,0,0,0,0]
testPos(dammen,0)
print("fertig")
