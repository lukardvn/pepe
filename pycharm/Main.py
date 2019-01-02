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

from MainMenu import Meni


class Frogger(QWidget):
    def __init__(self):
        super().__init__()
        Config.mainWindow = self #odma se postavi koji objekat je mainWindow da bi tamo u Rectangle.py Qlabeli znali gde treba da se nacrtaju. Lose je resenje, al radi bar za testiranje
        self.Map = [] #lista lejnova
        self.igrac1 = None
        self.igrac2 = None
        self.Menu = None #glavni meni
        self.GameOverBrojac = 0

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
        self.setMinimumHeight(Config.mapSize * Config.gridSize)
        self.setMinimumWidth(Config.mapSize * Config.gridSize)
        self.setMaximumHeight(Config.mapSize * Config.gridSize)
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

    def DisplayMap(self):
        self.Map.append(Lane.GenerateSafetyLane())
        self.Map.append(Lane.GenerateEasyLane(Config.laneTypeTrafficBottom))
        self.Map.append(Lane.GenerateMediumLane())
        self.Map.append(Lane.GenerateMediumLane())
        self.Map.append(Lane.GenerateMediumLane())
        self.Map.append(Lane.GenerateHardLane(Config.laneTypeTrafficTop))
        self.Map.append(Lane.GenerateSafetyLane())
        self.Map.append(Lane.GenerateEasyWaterLane())
        self.Map.append(Lane.GenerateMediumWaterLane())
        self.Map.append(Lane.GenerateMediumWaterLane())
        self.Map.append(Lane.GenerateHardLane())
        self.Map.append(Lane.GenerateMediumWaterLane())
        self.Map.append(Lane.GenerateHardWaterLane())
        self.Map.append(Lane.GenerateHardWaterLane())
        self.Map.append(Lane.GenerateFinalLane())

        self.startThreadForUpdatingObjects()

    def GameOverCheck(self, isPlayerTwo):
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
        self.stopThreadForUpdatingObjects()
        self.DeleteMap(isPlayerTwo)
        self.Menu.ShowMainMenu()
        Config.newLaneYIndex = 0
        self.GameOverBrojac = 0

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

        for rect in Rectangle.allRectangles[Config.layerZabe]:
            rect.Hide()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Frogger()
    sys.exit(app.exec_())
