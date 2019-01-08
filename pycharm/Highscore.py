import json
from Config import Config

class HighScore:
    def __init__(self):
        self.top3 = []

#lista tupli => tupla[0] -> name, tupla[1] -> score
#uvek se cuva top 3 rezultata

    def saveToFile(self):
        try:
            with open(Config.highscore_filename, 'w') as outfile:
                json.dump(self.top3, outfile)
            outfile.close()
        except:
            print('failed to save score to file')

    def readFromFile(self):
        try:
            file_object = open(Config.highscore_filename, 'r')
            self.top3 = json.load(file_object) #ucitaj hs
            file_object.close()
        except:
            print('empty file')

    def checkIfHighScore(self, n, s):
        if s > 0:
            self.top3.append([n, s])
            niz = []
            try:
                niz = sorted(self.top3, key=lambda x: x[1], reverse=True)
            except:
                print('sort pukao')
            self.top3.clear()
            for i in range(0, len(niz)):
                if i >= 3:
                    break
                else:
                    self.top3.append(niz[i])

            self.saveToFile()

if __name__ == '__main__':
    pass