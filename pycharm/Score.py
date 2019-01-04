from Rectangle import Rectangle

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
        lbl.setStyleSheet(
            "QLabel#" + objectName + " {background: rgb(255, 255, 255) transparent; color: " + color + "; font-family: 'Ariel'; font-size: 50px;}")
        lbl.setText(text)
        #print(lbl.text())
        if hide:
            lbl.hide()
        self.allWidgets.append(lbl)
        return lbl

    def CreateWidgets(self):
        widgets = []
        widgets.append(self.AddLabel("player1Score", 650, 745, '  ', "Green"))
        widgets.append(self.AddLabel("player2Score", 70, 745, '  ', "Pink"))
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

    def ShowScores(self):
        for widget in self.allWidgets:
            widget.show()