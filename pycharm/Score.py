
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QPixmap
from Config import Config

class Scoreboard(QWidget):
    def __init__(self, QWidget):
        super().__init__()
        self.qWidget = QWidget
        self.allWidgets = []
        self.allWidgets = self.CreateWidgets()

        self.p1Lives = []
        self.p2Lives = []

    def AddLabel(self, objectName, x, y, text, color, hide=False):
        lbl = QLabel(self.qWidget)
        lbl.setObjectName(objectName)
        lbl.move(x, y)
        lbl.resize(50, 50)
        lbl.setStyleSheet(
            "QLabel#" + objectName + " {background: rgb(255, 255, 255) transparent; color: " + color + "; font-family: '" + Config.font_family + "'; font-size: 60px;}")
        lbl.setText(text)
        lbl.setFocusPolicy(QtCore.Qt.NoFocus)
        #print(lbl.text())
        if hide:
            lbl.hide()
        self.allWidgets.append(lbl)
        return lbl

    def CreateHeart(self, x, y, color):
        lbl = QLabel(self.qWidget)
        if color == "Green":
            pixmap = QPixmap(Config.spriteLocation + "greenHeart.png")
        elif color == "Pink":
            pixmap = QPixmap(Config.spriteLocation + "pinkHeart.png")
        pixmap = pixmap.scaled(50, 50)
        lbl.setPixmap(pixmap)
        lbl.move(x, y)
        lbl.resize(50, 50)
        lbl.setFocusPolicy(QtCore.Qt.NoFocus)
        return lbl

    def CreateNumOfLivesHearts(self, color, lives):
        widgets = []
        if color == "Green":
            x = 370
        else:
            x = 120

        for i in range(0, lives):
            widgets.append(self.CreateHeart(x, 750, color))
            x += 50
        return widgets

    def CreateGreenLives(self, lives):
        self.HideP1Lives()
        self.p1Lives = self.CreateNumOfLivesHearts("Green", lives)
        self.ShowP1Lives()

    def CreatePinkLives(self, lives):
        self.HideP2Lives()
        self.p2Lives = self.CreateNumOfLivesHearts("Pink", lives)
        self.ShowP2Lives()

    def CreateWidgets(self):
        widgets = []
        widgets.append(self.AddLabel("player1Score", 700, 750, "0", "Green",hide=True))
        widgets.append(self.AddLabel("player2Score", 40, 750, "0", "Red",hide=True))
        return widgets


    def updateP1Score(self, score):
        self.allWidgets[0].setText(str(score))

    def updateP2Score(self, score):
        self.allWidgets[1].setText(str(score))

    def HideScores(self):
        for widget in self.allWidgets:
            widget.hide()

    def ShowScore(self):
        self.allWidgets[0].show()

    def ShowScores(self):
        for widget in self.allWidgets:
            widget.show()

    def ShowP1Lives(self):
        for widget in self.p1Lives:
            widget.show()

    def ShowP2Lives(self):
        for widget in self.p2Lives:
            widget.show()

    def HideP1Lives(self):
        for widget in self.p1Lives:
            widget.hide()
        self.p1Lives.clear()

    def HideP2Lives(self):
        for widget in self.p2Lives:
            widget.hide()
        self.p2Lives.clear()

if __name__ == '__main__':
    pass