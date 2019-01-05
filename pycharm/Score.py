
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QWidget
from Config import Config

class Scoreboard(QWidget):
    def __init__(self, QWidget):
        super().__init__()
        self.qWidget = QWidget
        self.allWidgets = []

        self.allWidgets = self.CreateWidgets()

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

    def CreateWidgets(self):
        widgets = []
        widgets.append(self.AddLabel("player1Score", 650, 750, "0", "Green"))
        widgets.append(self.AddLabel("player2Score", 70, 750, "0", "Red"))
        return widgets


    def updateP1Score(self, score):
        #print('Pozvao P1')
        self.allWidgets[0].setText(str(score))

    def updateP2Score(self, score):
        #print('Pozvao P2')
        self.allWidgets[1].setText(str(score))

    def HideScores(self):
        for widget in self.allWidgets:
            widget.hide()

    def ShowScore(self):
        self.allWidgets[0].show()

    def ShowScores(self):
        for widget in self.allWidgets:
            widget.show()