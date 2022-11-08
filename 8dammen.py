def kannSchlagen(dammen,position):
    dpos = dammen[position]
    for p in range(0,position):
        if dammen[p]==dpos or dammen[p]+(position-p)==dpos or dammen[p]-(position-p)==dpos:
            return True
    return False

print("start")
dammen = [0,0,0,0,0,0,0,0]
for d1 in range(0,8):
    dammen[0] = d1
    for d2 in range(0,8):
        dammen[1] = d2
        if kannSchlagen(dammen,1):
            continue
        for d3 in range(0,8):
            dammen[2] = d3
            if kannSchlagen(dammen,2):
                continue
            for d4 in range(0,8):
                dammen[3] = d4
                if kannSchlagen(dammen,3):
                    continue
                for d5 in range(0,8):
                    dammen[4] = d5
                    if kannSchlagen(dammen,4):
                        continue
                    for d6 in range(0,8):
                        dammen[5] = d6
                        if kannSchlagen(dammen,5):
                            continue
                        for d7 in range(0,8):
                            dammen[6] = d7
                            if kannSchlagen(dammen,6):
                                continue
                            for d8 in range(0,8):
                                dammen[7] = d8
                                if kannSchlagen(dammen,7):
                                    continue
                                else:
                                    print(f"found solution {dammen}")

print("fertig")
