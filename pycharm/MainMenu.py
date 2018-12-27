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
        self.onePlayerWidget.setStyleSheet("border-image: url('sprites/widgets1Player.png') 0 0 0 0 stretch stretch;")
        self.onePlayerWidget.resize(400, 70)
        self.onePlayerWidget.move(5, 200)
        self.onePlayerWidget.clicked.connect(self.onePlayerClicked)
        self.onePlayerWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Widgets.append(self.onePlayerWidget)

        self.twoPlayerWidget = QPushButton(QWidget)
        self.twoPlayerWidget.setStyleSheet("border-image: url('sprites/widgets2Player.png') 0 0 0 0 stretch stretch;")
        self.twoPlayerWidget.resize(400, 70)
        self.twoPlayerWidget.move(5, 300)
        self.twoPlayerWidget.clicked.connect(self.twoPlayerClicked)
        self.twoPlayerWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Widgets.append(self.twoPlayerWidget)

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