import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit,QVBoxLayout
from Config import Config


class Meni(QWidget):
    def __init__(self, QWidget, funcSinglePlayer, funcTwoPlayers, highscoresFunkc, funcHostGame, funcJoinGame, funcCloseWindow):
        super().__init__()
        self.allWidgets = []
        self.qWidget = QWidget

        self.funcCloseWindow = funcCloseWindow

        self.bgImg = QLabel(QWidget)
        pixmap = QPixmap(Config.spriteLocation + "MainMenu2.png")
        pixmap = pixmap.scaled(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize + 50)
        self.bgImg.setPixmap(pixmap)
        self.bgImg.setFocusPolicy(QtCore.Qt.NoFocus)
        self.bgImg.show()

        self.kisa = self.KreirajGif('kisa.gif') #label za kisu, koji ce se samo preko mape prikazivati i sklanjati
        self.sneg = self.KreirajGif('sneg.gif') #label za sneg, koji ce se samo preko mape prikazivati i sklanjati
        movie = self.sneg.movie()
        movie.setSpeed(200)
        self.mainButtons = self.GlavniMeniKojiSePrikazeNaPocetku(funcSinglePlayer, funcTwoPlayers, highscoresFunkc, funcHostGame)

        self.optionsElements = self.OptionsSubMenuInit(self.OptionsSubMenuHide)
        self.hsElements = []

        self.joinElements = self.JoinWidgetsInit(funcJoinGame)
        self.ipaddr = ""
        self.port = ""


    def KreirajGif(self, gif):  #kreira se Qlabel sa gif slikom u pozadini
        label = QLabel(self.qWidget)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.resize(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize)
        loading_movie = QMovie(Config.spriteLocation + gif)
        label.setMovie(loading_movie)
        size = QtCore.QSize(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize)
        label.movie().setScaledSize(size)
        loading_movie.start()
        label.hide()
        return label

    def PrikaziPadavinu(self, tip):
        if tip == 'kisa':
            self.kisa.show()
            self.kisa.raise_()
        elif tip == 'sneg':
            self.sneg.show()
            self.sneg.raise_()

    def GlavniMeniKojiSePrikazeNaPocetku(self, singlePlayerOnClick, twoPlayerOnClick, highscoresFunkc, hostOnClick):
        listaWidgeta = []
        listaWidgeta.append(self.AddButton("1PlayerWidget", "widgets1Player", 5, 170, 400, 70, singlePlayerOnClick))
        listaWidgeta.append(self.AddButton("2PlayerWidget", "widgets2Player", 5, 250, 400, 70, twoPlayerOnClick))
        listaWidgeta.append(self.AddButton("JoinGameWidget", "widgetsJoin", 5, 330, 400, 70, self.JoinWidgetsShow))
        listaWidgeta.append(self.AddButton("HostGameWidget", "widgetsHost", 5, 410, 400, 70, hostOnClick))
        listaWidgeta.append(self.AddButton("highscoresWidget", "widgetsHighscores", 5, 490, 400, 70, highscoresFunkc))
        listaWidgeta.append(self.AddButton("optionsWidget", "widgetsOptions", 5, 570, 400, 70, self.OptionsSubMenuShow))
        listaWidgeta.append(self.AddButton("exitWidget", "widgetsExit", 5, 650, 400, 70, self.exitClicked))
        return listaWidgeta

    def SakrijPadavinu(self, tip):
        if tip == 'kisa':
            self.kisa.hide()
        elif tip == 'sneg':
            self.sneg.hide()


    def OptionsSubMenuInit(self, exitMenuOnClick=None):
        optionsWidgets = []
        optionsWidgets.append(self.AddLabel("player1Name", 50, 200, "PLAYER 1:", hide=True))
        optionsWidgets.append(self.AddLabel("player2Name", 50, 300, "PLAYER 2:", hide=True))
        optionsWidgets.append(self.AddEditLine("player1NameTxt", 250, 185, 450, 95, "Player1", hide=True))
        optionsWidgets.append(self.AddEditLine("player2NameTxt", 250, 285, 450, 95, "Player2", hide=True))
        optionsWidgets.append(self.AddButton("okWidget", "widgetsOk", 50, 420, 400, 70, exitMenuOnClick, hide=True))
        return optionsWidgets

    def JoinWidgetsInit(self, joinGame=None):
        joinWidgets = []
        joinWidgets.append(self.AddLabel("ipAddress", 50, 200, "IP ADDRESS:", hide=True))
        joinWidgets.append(self.AddLabel("port", 50, 300, "PORT:", hide=True))
        joinWidgets.append(self.AddEditLine("ipAddressTxt", 250, 185, 450, 95, "", hide=True, OnJoin=self.SetIPAddress))
        joinWidgets.append(self.AddEditLine("portTxt", 250, 285, 450, 95, "", hide=True, OnJoin=self.SetPort))
        joinWidgets.append(self.AddButton("okWidget", "widgetsOk", 50, 420, 400, 70, joinGame, hide=True))
        return joinWidgets

    # def HsElementsInit(self, nizTop3):
    #     widgets = []
    #     y = 200
    #     for item in nizTop3:
    #         widgets.append(self.AddLabel("p1Score", 100, y, str(item[0]) + " :\t" + str(item[1]), hide=True))
    #         y += 100
    #     widgets.append(self.AddButton("okWidgt", "widgetsOk", 100, 500, 400, 70, self.HsElementsHide, hide=True))
    #     return widgets

    #isto radi kao ova funkcija iznad samo koristi YIELD, da naucite sta je yield (moze da se primeni na svaku funkciju koja vraca neki niz)
    def HsElementsInit(self, nizTop3):
        y = 200
        for item in nizTop3:
            yield self.AddLabel("p1Score", 100, y, str(item[0]) + " :\t" + str(item[1]))
            y += 100
        yield self.AddButton("okWidgt", "widgetsOk", 100, 500, 400, 70, self.HsElementsHide)

    def HsElementsShow(self, nizTop3):
        for widget in self.allWidgets:
            widget.hide()

        for elem in self.HsElementsInit(nizTop3): #evo primena funkcije koja koristi yield. TZV. funkcije generatori
            self.hsElements.append(elem)

    def HsElementsHide(self):
        for item in self.hsElements:
            item.hide()

        for btn in self.mainButtons:
            btn.show()

        self.hsElements.clear()

    def OptionsSubMenuShow(self):
        for btn in self.mainButtons:
            btn.hide()

        for element in self.optionsElements:
            element.show()

    def JoinWidgetsShow(self):
        for btn in self.mainButtons:
            btn.hide()

        for element in self.joinElements:
            element.show()

    #Fja koja se izvrsava prilikom klika na Ok button u okviru Options prozora
    def OptionsSubMenuHide(self):
        #uzima se ime iz textBoxa, znamo da je na ovoj poziciji plName
        if self.optionsElements[2] != None:
            Config.p1Name = self.optionsElements[2].text()
            self.optionsElements[2].clearFocus()

        # uzima se ime iz textBoxa, znamo da je na ovoj poziciji p2Name
        if self.optionsElements[3] != None:
            Config.p2Name = self.optionsElements[3].text()
            self.optionsElements[3].clearFocus()

        for element in self.optionsElements:
            element.hide()

        for btn in self.mainButtons:
            btn.show()

    def AddButton(self, objectName, sprite, x, y, width, height, onClick=None, hide=False):
        btn = QPushButton(self.qWidget)
        btn.setObjectName(objectName)
        btn.setStyleSheet(
            "QPushButton#" + objectName + " { border-image: url('sprites/" + sprite + ".png') 0 0 0 0 stretch stretch;} QPushButton#" + objectName + ":hover { border-image: url('sprites/" + sprite + "Hover.png') 0 0 0 0 stretch stretch;}")
        btn.resize(width, height)
        btn.move(x, y)
        if onClick != None:
            btn.clicked.connect(onClick)
        btn.setFocusPolicy(QtCore.Qt.NoFocus)

        if hide:
            btn.hide()
        else:
            btn.show()

        self.allWidgets.append(btn)
        return btn

    def AddLabel(self, objectName, x, y, text, hide=False):
        lbl = QLabel(self.qWidget)
        lbl.setObjectName(objectName)
        lbl.move(x, y)
        lbl.setStyleSheet("QLabel#" + objectName + " {background: rgb(255, 255, 255) transparent; color: 'White'; font-family: '" + Config.font_family + "'; font-size: 70px;}")
        lbl.setText(text)
        if hide:
            lbl.hide()
        else:
            lbl.show()

        self.allWidgets.append(lbl)
        return lbl

    def AddEditLine(self, objectName, x, y, width, height, text, hide=False, OnJoin=None):
        editLine = QLineEdit(self.qWidget)
        editLine.setObjectName(objectName)
        editLine.move(x, y)
        editLine.resize(width, height)
        editLine.setStyleSheet("QLineEdit#" + objectName + " {background: rgba(152, 193, 42, 0.5); border: 5px solid #98C12A; color: 'White'; font-family: '" + Config.font_family + "'; font-size: 70px;}")
        editLine.setText(text)
        # Widgets.append(player1NameTxt)
        if hide:
            editLine.hide()
        else:
            editLine.show()

        if OnJoin != None:
            editLine.textChanged.connect(OnJoin)

        self.allWidgets.append(editLine)
        return editLine

    def SetIPAddress(self):
        self.ipAddr = self.joinElements[2].text()
        print(self.ipAddr)
        #self.ipaddr = key

    def SetPort(self):
        self.port = self.joinElements[3].text()
        print(self.port)
        #self.port = key

    def HideMainMenu(self):
        for widget in self.allWidgets:
            widget.hide()
        self.bgImg.hide()

    def ShowMainMenu(self):
        self.OptionsSubMenuHide()
        self.bgImg.show()

    def exitClicked(self):
        self.funcCloseWindow()
        sys.exit(0)

if __name__ == '__main__':
    pass
