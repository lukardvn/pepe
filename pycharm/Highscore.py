from Config import Config

class HighScore:
    def __init__(self):
        self.top3 = []

#lista tupli => tupla[0] -> name, tupla[1] -> score
#uvek se cuva top 3 rezultata

    def saveToFile(self):
        file = open(Config.highscore_filename, "w")
        for item in self.top3:
            file.write(str(item[0]) + ':' + str(item[1]) + '\n')
        file.close()

    def readFromFile(self):
        try:
            file = open(Config.highscore_filename, "r")
            for line in file:
                n, s = line.split(":")
                s = s.rstrip()
                item = []
                item.append(n)
                item.append(s)
                self.top3.append(item)
            self.top3 = sorted(self.top3, key=lambda item: item[1], reverse=True)
            file.close()
        except:
            print('ne postoji fajl ili je prvo kreiranje')

    def checkIfHighScore(self, n, s):
        newItem = []
        newItem.append(n)
        newItem.append(s)

        if len(self.top3) < 3:
            self.top3.append(newItem)
            print('<3')
        else:
            print('=3')
            minimalni = min(self.top3, key=lambda item: item[1])
            print(minimalni)
            if s > int(minimalni[1]):
                print('if prosao')
                self.top3.remove(minimalni)
                print('remove prosao')
                self.top3.append(newItem)

        self.top3 = sorted(self.top3, key=lambda item: item[1], reverse=True) #sortira od najboljeg ka najlosijem skoru
        self.saveToFile()




