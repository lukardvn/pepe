import sys
import PyQt5

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets

from key_notifier import KeyNotifier

from Config import Config
from Frog import Frog
from GameObject import GameObject, GOUpdater
from Lane import Lane
import datetime
from Lilypad import Lilypad
from Rectangle import Rectangle
from random import shuffle, randrange

from MainMenu import Meni


class Frogger(QWidget):
    def __init__(self):
        super().__init__()
        Config.mainWindow = self #odma se postavi koji objekat je mainWindow da bi tamo u Rectangle.py Qlabeli znali gde treba da se nacrtaju. Lose je resenje, al radi bar za testiranje
        self.Map = [] #lista lejnova
        self.igrac1 = None
        self.igrac2 = None
        self.Menu = None #glavni meni
        self.GameOverBrojac = 0 # za zivote, ako je 2PlayerMode, kad igrac izgubi sve zivote povecava brojac za 1, kad oba izgube sve zivote, brojac je 2 i tad je gameOver
        # ako je SinglePlayer mod onda je gameOver ako je brojac 1
        self.Level = 1 # za levele

        self.setWindowState(Qt.WindowNoState)
        self.__init_ui__()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

    def __init_ui__(self):
        self.Menu = Meni(self, self.SinglePlayerMode, self.TwoPlayerMode)
        self.setWindowTitle('Frogger')
        self.setWindowIcon(QtGui.QIcon(Config.spriteLocation+'iconFrog.png')) #ikonica
        self.resize(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize + 50)
        self.FixWindowSize()
        self.show()
        #self.startThreadForUpdatingObjects()

    #obicna funkcija za fiksiranje velicine prozora
    def FixWindowSize(self):
        self.setMinimumHeight((Config.mapSize+1) * Config.gridSize)
        self.setMinimumWidth(Config.mapSize * Config.gridSize)
        self.setMaximumHeight((Config.mapSize+1) * Config.gridSize)
        self.setMaximumWidth(Config.mapSize * Config.gridSize)

    def SinglePlayerMode(self):
        self.Menu.HideMainMenu()
        self.DisplayMap()
        self.CreatePlayers()

    def TwoPlayerMode(self):
        self.Menu.HideMainMenu()
        self.DisplayMap()
        self.CreatePlayers(TwoPlayers=True)

    def CreatePlayers(self, TwoPlayers=False):
        self.igrac1 = Frog(Config.player1StartPosition[0], Config.player1StartPosition[1], self.GameOverCheck)
        if TwoPlayers:
            self.igrac2 = Frog(Config.player2StartPosition[0], Config.player2StartPosition[1], self.GameOverCheck, isPlayerTwo=True)
            Config.twoPl = TwoPlayers

    def DisplayMap(self):
        self.Map.append(Lane.GenerateSafetyLane())  #prvi je uvek sejf lejn
        self.GenerateLanes('Road')    #fja da generise lejnove za put
        self.Map.append(Lane.GenerateSafetyLane())
        self.GenerateLanes('Water')   #fja da generise lejnove za reku
        self.Map.append(Lane.GenerateFinalLane(self.LevelPassed)) # zadnji je uvek finalLane

        self.startThreadForUpdatingObjects()

    def GameOverCheck(self, isPlayerTwo):
        #fja koja se poziva kada igrac ima 0 zivota, prosledjuje se igracima kroz konstruktor
        self.GameOverBrojac += 1
        if self.igrac1 != None and self.igrac2 != None:
            if self.GameOverBrojac == 1:
                if isPlayerTwo:
                    self.igrac2.Hide()
                    self.igrac2 = None
                else:
                    self.igrac1.Hide()
                    self.igrac1 = None
        elif self.igrac1 != None:
            if self.GameOverBrojac == 1:
                self.GameOver(False)
            elif self.GameOverBrojac == 2:
                self.GameOver(True)
        elif self.igrac2 != None:
            if self.GameOverBrojac == 2:
                self.GameOver(True)

    def GameOver(self, isPlayerTwo):
        #fja koja se poziva kad su svi igraci igraci ostali bez zivota
        self.stopThreadForUpdatingObjects()
        self.DeleteMap(isPlayerTwo)
        self.Menu.ShowMainMenu()
        Config.newLaneYIndex = 0
        self.GameOverBrojac = 0
        self.Level = 1

    def LevelPassed(self):
        #fja koja se poziva kad su svih 5 Lilypada popunjena, prosledjuje se u konstruktoru, prvo finalLejnu pa samim objektima
        self.stopThreadForUpdatingObjects()
        self.Level += 1
        #print(self.Level)
        Config.newLaneYIndex = 0
        self.GameOverBrojac = 0
        if self.igrac1 != None and self.igrac2 != None:
            self.DeleteMap(True)
            self.DisplayMap()
            self.CreatePlayers(TwoPlayers=True)
        elif self.igrac1 != None:
            self.DeleteMap(False)
            self.DisplayMap()
            self.CreatePlayers()
        elif self.igrac2 != None:
            self.DeleteMap(True)
            self.DisplayMap()
            self.CreatePlayers(TwoPlayers=True)
            self.igrac1.Hide()
            self.igrac1 = None

    def DeleteMap(self, TwoPlayers):
        try:
            self.igrac1.Hide()
            self.igrac1 = None
        except:
            print('vec postavljen na None')

        if TwoPlayers:
            try:
                self.igrac2.Hide()
                self.igrac2 = None
            except:
                print('vec postavljen na None')

        for lane in self.Map:
            for obs in lane.obstacles:
                obs.Hide()
            lane.obstacles.clear()
            lane.Hide()

        for rect in Rectangle.allRectangles[Config.layerLilypad]:
            rect.Hide()
        Rectangle.allRectangles[Config.layerLilypad].clear()

        for rect in Rectangle.allRectangles[Config.layerZabe]:
            rect.Hide()
        Rectangle.allRectangles[Config.layerZabe].clear()

        self.Map.clear()

    def DisplayTestMap(self):
        self.Map.append(Lane.GenerateSafetyLane())
        self.Map.append(Lane.GenerateEasyLane())
        self.Map.append(Lane.GenerateEasyLane())
        self.Map.append(Lane.GenerateEasyLane())
        self.Map.append(Lane.GenerateSafetyLane())
        self.Map.append(Lane.GenerateFinalLane())
        self.Map.append(Lane.GenerateFinalLane(lilyPadPattern=Config.lilypadPatternBO3))
        self.Map.append(Lane.GenerateFinalLane(lilyPadPattern=Config.lilypadPatternBO5V2))
        self.Map.append(Lane.GenerateFinalLane(randomPatternBO5=True))

    def keyPressEvent(self, event):
        if not event.isAutoRepeat():
            self.key_notifier.add_key(event.key())

    def __update_position__(self, key):
        if self.igrac1 != None:
            self.igrac1.KeyPress(key)
        if self.igrac2 != None:
            self.igrac2.KeyPress(key)

    def closeEvent(self, event):
        self.updaterGameObjekataThread.updaterThreadWork = False
        self.key_notifier.die()

    def startThreadForUpdatingObjects(self):
        self.updaterGameObjekataThread = GOUpdater()
        self.updaterGameObjekataThread.nekiObjekat.connect(self.updateAllGameObjects)
        self.updaterGameObjekataThread.start()

    def stopThreadForUpdatingObjects(self):
        self.updaterGameObjekataThread.updaterThreadWork = False

    def updateAllGameObjects(self, dummy):
        for gameObject in GameObject.allGameObjects:
            gameObject.update()

    def createLanes(self, niz, type):
        #funkcija koja generise lejnove u zavisnosti od prosledjenog niza i karaktera u njemu
        if type == 'Road':
            for i in range(len(niz)):
                if niz[i] == 'e':
                    self.Map.append(Lane.GenerateEasyLane())
                elif niz[i] == 'm':
                    self.Map.append(Lane.GenerateMediumLane())
                elif niz[i] == 'h':
                    self.Map.append(Lane.GenerateHardLane())
        elif type == 'Water':
            for i in range(len(niz)):
                if niz[i] == 'e':
                    self.Map.append(Lane.GenerateEasyWaterLane())
                elif niz[i] == 'm':
                    self.Map.append(Lane.GenerateMediumWaterLane())
                elif niz[i] == 'h':
                    self.Map.append(Lane.GenerateHardWaterLane())
        elif type == 'Random':
            for letter in niz:
                if letter == 's':  # safe lane
                    self.Map.append(Lane.GenerateSafetyLane())
                elif letter == 'e':  # easy lane, if generated -1 -> easyWaterLane if 1 easyTrafficLane, isto vazi za ostale samo se menja tezina s,m,h...
                    if [-1, 1][randrange(2)] == -1:
                        self.Map.append(Lane.GenerateEasyWaterLane())
                    else:
                        self.Map.append(Lane.GenerateEasyLane())
                elif letter == 'm':
                    if [-1, 1][randrange(2)] == -1:
                        self.Map.append(Lane.GenerateMediumWaterLane())
                    else:
                        self.Map.append(Lane.GenerateMediumLane())
                elif letter == 'h':
                    if [-1, 1][randrange(2)] == -1:
                        self.Map.append(Lane.GenerateHardWaterLane())
                    else:
                        self.Map.append(Lane.GenerateHardLane())

    def GenerateLanes(self, type):
        # 6 lejnova, fja u kojoj se odlucuje tezina po levelima, moze da se menja po volji
        nizTezine = []
        if self.Level <= 2:
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
        elif self.Level > 2 and self.Level <= 4:
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            type = 'Random'
        elif self.Level > 4 and self.Level <= 6:
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
        elif self.Level > 6 and self.Level <= 8:
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            type = 'Random'
        elif self.Level > 8 and self.Level <= 10:
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
        elif self.Level > 10 and self.Level <= 12:
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            type = 'Random'
        elif self.Level > 12 and self.Level <= 14:
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
        elif self.Level > 12 and self.Level <= 14:
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            type = 'Random'
        elif self.Level > 14 and self.Level <= 16:
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
        elif self.Level > 16:
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            type = 'Random'

        shuffle(nizTezine)  #permutuj niz da lejnovi budu random
        self.createLanes(nizTezine, type)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Frogger()
    sys.exit(app.exec_())
