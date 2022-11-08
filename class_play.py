class Shot():
    s = 1
    def __init__(self):
        self.os = self.s

myshot = Shot()
print(f"myshot.os {myshot.os}")
print(f"myshot.s {myshot.s}")
print(f"Shot.s {Shot.s}")
Shot.s = 2
myshot2 = Shot()
print(f"myshot.os {myshot2.os}")
print(f"myshot.s {myshot2.s}")
print(f"Shot.s {Shot.s}")


