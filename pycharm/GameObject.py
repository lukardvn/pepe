from Config import Config
from PyQt5 import QtCore
import time


class GameObject:
    allGameObjects = []

    def __init__(self):
        self.allGameObjects.append(self)

    def update(self):
        pass


class GOUpdater(QtCore.QThread):
    nekiObjekat = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.updaterThreadWork = True
        self.pause = False

    def PauseGame(self):
        self.pause = True

    def ResumeGame(self):
        self.pause = False

    def run(self):
        while self.updaterThreadWork:
            if not self.pause:
                self.nekiObjekat.emit(1)
            time.sleep(1 / Config.FPS)