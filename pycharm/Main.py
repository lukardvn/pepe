import sys
import threading
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QApplication

from key_notifier import KeyNotifier

from Config import Config
from Frog import Frog
from GameObject import GameObject, GOUpdater
from Obstacle import Obstacle
from Lane import Lane
from Rectangle import Rectangle

class Frogger(QWidget):
    def __init__(self):
        super().__init__()
        Config.mainWindow = self #odma se postavi koji objekat je mainWindow da bi tamo u Rectangle.py Qlabeli znali gde treba da se nacrtaju. Lose je resenje, al radi bar za testiranje
        self.traka = Lane(0, 0, 0, 0, "")
        self.traka2 = Lane(5, -7, 170, 1, "")

        self.igrac1 = Frog(Config.player1StartPosition[0], Config.player1StartPosition[1])
        self.igrac2 = Frog(Config.player2StartPosition[0], Config.player2StartPosition[1], isPlayerTwo=True)

        #self.traka = Lane(3, 5, 70, 0, "vula ne zna")

        #self.obs = Rectangle(0,50,50,750,"trava.png")

        self.setWindowState(Qt.WindowNoState)
        self.__init_ui__()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

    def __init_ui__(self):


        #self.traka.Show()
        #self.traka2.Show()

        ###
        self.igrac1.Show()
        self.igrac2.Show()

        self.setWindowTitle('Frogger')
        self.resize(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize)
        self.show()
        self.startThreadForUpdatingObjects()

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            self.key_notifier.add_key(event.key())


    def __update_position__(self, key):
        self.igrac1.KeyPress(key)
        self.igrac2.KeyPress(key)

        if key == Qt.Key_Space:
            if self.igrac1.Collision(self.igrac2):
                print("Sudarili se :(")
            else:
                print("Nisu se sudarili")

        if key == Qt.Key_G:
            print("Razdaljina je: " + str(self.igrac1.Distance(self.igrac2)))

    def closeEvent(self, event):
        self.updaterGameObjekataThread.updaterThreadWork = False
        self.key_notifier.die()

    def startThreadForUpdatingObjects(self):
        self.updaterGameObjekataThread = GOUpdater()
        self.updaterGameObjekataThread.nekiObjekat.connect(self.updateAllGameObjects)
        self.updaterGameObjekataThread.start()


    def updateAllGameObjects(self, gameObj):
        gameObj.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Frogger()
    sys.exit(app.exec_())
