from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from Config import Config

class Meni(QWidget):
    def __init__(self, QWidget, igrac1, igrac2):
        super().__init__()
        self.Widgets = []

        self.bgImg = QLabel(QWidget)
        pixmap = QPixmap(Config.spriteLocation + "MainMenu2.png") #prva verzija pozadine MainMenu.png
        pixmap = pixmap.scaled(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize)
        self.bgImg.setPixmap(pixmap)
        self.bgImg.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Widgets.append(self.bgImg)

        self.onePlayerWidget = QPushButton(QWidget)
        self.onePlayerWidget.setObjectName("1PlayerWidget")
        self.onePlayerWidget.setStyleSheet("QPushButton#1PlayerWidget { border-image: url('sprites/widgets1Player.png') 0 0 0 0 stretch stretch;} QPushButton#1PlayerWidget:hover { border-image: url('sprites/widgets1PlayerHover.png') 0 0 0 0 stretch stretch;}")
        self.onePlayerWidget.resize(400, 70)
        self.onePlayerWidget.move(5, 200)
        self.onePlayerWidget.clicked.connect(self.onePlayerClicked)
        self.onePlayerWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Widgets.append(self.onePlayerWidget)

        self.twoPlayerWidget = QPushButton(QWidget)
        self.twoPlayerWidget.setObjectName("2PlayerWidget")
        self.twoPlayerWidget.setStyleSheet("QPushButton#2PlayerWidget { border-image: url('sprites/widgets2Player.png') 0 0 0 0 stretch stretch;} QPushButton#2PlayerWidget:hover { border-image: url('sprites/widgets2PlayerHover.png') 0 0 0 0 stretch stretch;}")
        self.twoPlayerWidget.resize(400, 70)
        self.twoPlayerWidget.move(5, 300)
        self.twoPlayerWidget.clicked.connect(self.twoPlayerClicked)
        self.twoPlayerWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Widgets.append(self.twoPlayerWidget)

        self.highscoresWidget = QPushButton(QWidget)
        self.highscoresWidget.setObjectName("highscoresWidget")
        self.highscoresWidget.setStyleSheet("QPushButton#highscoresWidget { border-image: url('sprites/widgetsHighscores.png') 0 0 0 0 stretch stretch;} QPushButton#highscoresWidget:hover { border-image: url('sprites/widgetsHighscoresHover.png') 0 0 0 0 stretch stretch;}")
        self.highscoresWidget.resize(400, 70)
        self.highscoresWidget.move(5, 400)
        #self.highscoresWidget.clicked.connect(self.optionsClicked)
        self.highscoresWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Widgets.append(self.highscoresWidget)

        self.optionsWidget = QPushButton(QWidget)
        self.optionsWidget.setObjectName("optionsWidget")
        self.optionsWidget.setStyleSheet("QPushButton#optionsWidget { border-image: url('sprites/widgetsOptions.png') 0 0 0 0 stretch stretch;} QPushButton#optionsWidget:hover { border-image: url('sprites/widgetsOptionsHover.png') 0 0 0 0 stretch stretch;}")
        self.optionsWidget.resize(400, 70)
        self.optionsWidget.move(5, 500)
        #self.optionsWidget.clicked.connect(self.optionsClicked)
        self.optionsWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Widgets.append(self.optionsWidget)

        self.exitWidget = QPushButton(QWidget)
        self.exitWidget.setObjectName("exitWidget")
        self.exitWidget.setStyleSheet("QPushButton#exitWidget { border-image: url('sprites/widgetsExit.png') 0 0 0 0 stretch stretch;} QPushButton#exitWidget:hover { border-image: url('sprites/widgetsExitHover.png') 0 0 0 0 stretch stretch;}")
        self.exitWidget.resize(400, 70)
        self.exitWidget.move(5, 600)
        #self.exitWidget.clicked.connect(self.optionsClicked)
        self.exitWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Widgets.append(self.exitWidget)

        self.igrac1 = igrac1
        self.igrac2 = igrac2

    def onePlayerClicked(self):
        for widget in self.Widgets:
            widget.hide()
        self.igrac1.ShowFromMenu()

    def twoPlayerClicked(self):
        for widget in self.Widgets:
            widget.hide()
        self.igrac1.ShowFromMenu()
        self.igrac2.ShowFromMenu()
