import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QApplication

from key_notifier import KeyNotifier

from Config import Config
from Frog import Frog
from GameObject import GameObject, GOUpdater
from Lane import Lane
from Rectangle import Rectangle
from NetworkCommunication import Host, Client

from MainMenu import Meni
class Frogger(QWidget):
    def __init__(self):
        super().__init__()
        Config.mainWindow = self #odma se postavi koji objekat je mainWindow da bi tamo u Rectangle.py Qlabeli znali gde treba da se nacrtaju. Lose je resenje, al radi bar za testiranje
        self.Map = [] #lista lejnova
        self.player1 = None
        self.player2 = None
        self.Menu = None #glavni meni
        self.isHost = False
        self.isClient = False
        self.host = None
        self.client = None
        self.gamePaused = False

        self.setWindowState(Qt.WindowNoState)
        self.__init_ui__()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

    def __init_ui__(self):
        self.DisplayMainMenu()
        self.setWindowTitle('Frogger')
        self.resize(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize + 50)
        self.show()
        self.startThreadForUpdatingObjects()

    def DisplayMainMenu(self):
        self.Menu = None
        self.Menu = Meni(self, self.SinglePlayerMode, self.TwoPlayerMode, self.MainMenuHostClick,self.MainMenuJoinClick)

    def PauseGame(self):
        self.gamePaused = True
        self.updaterGameObjekataThread.PauseGame()

    def ResumeGame(self):
        self.gamePaused = False
        self.updaterGameObjekataThread.ResumeGame()

    def RemoveAllGameUIObjects(self):
        for lejer,lista in Rectangle.allRectangles.items():
            for rect in lista:
                rect.RemoveFromScreen()
        GameObject.allGameObjects = []
        Rectangle.allRectangles = {}
        Rectangle.ResetId()

    def SinglePlayerMode(self):
        self.Menu.HideMainMenu()
        self.updaterGameObjekataThread.start()
        self.DisplayMap()
        self.CreatePlayers()

    def TwoPlayerMode(self):
        self.Menu.HideMainMenu()
        self.updaterGameObjekataThread.start()
        self.DisplayMap()
        self.CreatePlayers(TwoPlayers=True)

    def MainMenuHostClick(self):
        self.HostServer(Config.serverAddress, Config.serverPort)

    def MainMenuJoinClick(self):
        self.JoinServer(Config.serverAddress, Config.serverPort)

    def CreatePlayers(self, TwoPlayers=False):
        self.player1 = Frog(Config.player1StartPosition[0], Config.player1StartPosition[1])
        if TwoPlayers:
            self.player2 = Frog(Config.player2StartPosition[0], Config.player2StartPosition[1], isPlayerTwo=True)

    def DisplayMap(self):
        Lane.ResetLaneStartingIndex()
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

    def DisplayTestMap(self):
        Lane.ResetLaneStartingIndex()
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
        if not (self.isClient or self.isHost):
            if key == Qt.Key_Escape and self.gamePaused:
                self.ResumeGame()
            elif key == Qt.Key_Escape and not self.gamePaused:
                self.PauseGame()

        if self.isClient:   #ako sam klijent onda pored pomeranja zabe, hocu da posaljem INPUT serveru
            if key == Qt.Key_Right:
                self.client.SendToServer(Config.inputKlijentaPrefix + "DESNO")
            elif key == Qt.Key_Down:
                self.client.SendToServer(Config.inputKlijentaPrefix + "DOLE")
            elif key == Qt.Key_Up:
                self.client.SendToServer(Config.inputKlijentaPrefix + "GORE")
            elif key == Qt.Key_Left:
                self.client.SendToServer(Config.inputKlijentaPrefix + "LEVO")

        if key == Qt.Key_T:
            for go in GameObject.allGameObjects:
                print(str(go.id) +"__"+ str(go.loadedSprite))

        if self.gamePaused: #sve sto je ispod nece biti odradjeno kad je game pauziran
            return

        if self.player1 != None:
            self.player1.KeyPress(key)
        if self.player2 != None:
            self.player2.KeyPress(key)


    def closeEvent(self, event):
        self.updaterGameObjekataThread.updaterThreadWork = False
        self.key_notifier.die()

    def startThreadForUpdatingObjects(self):
        self.updaterGameObjekataThread = GOUpdater()
        self.updaterGameObjekataThread.nekiObjekat.connect(self.updateAllGameObjects)
        #self.updaterGameObjekataThread.start() #OVO SE POKRECE KAD KLIJENT BUDE SPREMAN, ili kad pocne neki od lokalnih game modova

    def updateAllGameObjects(self, dummy):
        for gameObject in GameObject.allGameObjects:
            gameObject.update()

        # ako je instanca server i postoje gameobjekti onda da salje klijentu pozicije tih objekata
        if self.isHost and len(GameObject.allGameObjects) > 0:
            self.SendUpdateToClient()

    ################################################################################
    #FUNKCIJE ISPOD SE KORISTE SAMO ZA MULITPLAYER
    ################################################################################

    def HostServer(self, address, port):
        self.isHost = True
        self.host = Host(address, port)
        self.host.receiveCallBack.connect(self.ReceiveFromClient)
        self.host.start()

    def JoinServer(self, address, port):
        self.isClient = True
        self.client = Client(address, port)
        self.client.receiveCallBack.connect(self.ReceiveFromServer)
        self.client.start()

    # ovo ce biti pozvano kad server primi poruku od klijenta
    def ReceiveFromClient(self, data):
        # print("Primio od klijenta: " + str(data))
        if data == Config.clientIsReady:  # kad primi ovo znaci da se klijent povezao
            self.TwoPlayerMode()
            self.player2.keyBoardInputEnabled = False
            self.host.SendToClient(Config.kreirajSveObjekteNaKlijentu + ":" + self.CreateInitObjectsString())
        elif data == Config.potvrdaKlijentaDaJeNapravioSveObjekte:  # klijent je potvrdio da je napravio sve objekte i sad pokrecemo igru (pokrecemo thread koji updateuje igru)
            self.updaterGameObjekataThread.start()
        elif Config.inputKlijentaPrefix in data:
            if Config.inputKlijentaPrefix + "DESNO" == data:
                self.player2.GoRight()
            elif Config.inputKlijentaPrefix + "DOLE" == data:
                self.player2.GoDown()
            elif Config.inputKlijentaPrefix + "GORE" == data:
                self.player2.GoUp()
            elif Config.inputKlijentaPrefix + "LEVO" == data:
                self.player2.GoLeft()

    # ovo ce biti pozvano kad klijent primi poruku od servera
    def ReceiveFromServer(self, data):
        #print("Primio od servera: " + str(data))
        if data == Config.serverWelcomeMsg:  # znaci da smo se uspesno povezali sa serverom i inicijalizujemo gejm
            self.InitNetworkGame()
        elif Config.kreirajSveObjekteNaKlijentu in data:
            self.GenerateObjects(data.split(":")[1])
            self.client.SendToServer(Config.potvrdaKlijentaDaJeNapravioSveObjekte)
        elif Config.updateSveObjekteNaKlijentu in data:
            self.UpdateObjectsPosition(data.split(":")[1])
        elif "CONN_ERROR" == data:
            self.ResetGameStateOnError()

    #ovo se poziva na klijentu.
    def InitNetworkGame(self):
        self.TwoPlayerMode()

        #sklanjamo sve objekte, jer ce nam server poslati sta je on generisao (velicine, pozicije, sprajtove)
        for go in GameObject.allGameObjects:
            go.RemoveFromScreen()
        GameObject.allGameObjects.clear()
        #klijent javi serveru da je spreman (spreman da primi podatke o svim objektima)
        self.client.SendToServer(Config.clientIsReady)

    def ResetGameStateOnError(self):
        self.isClient = False
        self.isHost = False
        if self.host != None:
            self.host.radi = False
            self.host = None
        if self.client != None:
            self.client.radi = False
            self.client = None
        self.RemoveAllGameUIObjects()
        self.DisplayMainMenu()

    #poziva se samo na serveru
    def SendUpdateToClient(self):
        self.host.SendToClient(Config.updateSveObjekteNaKlijentu + ":" + self.CreateUpdateObjectsString())

    #ova metoda moze ici u GameObject Klasu
    def CreateInitObjectsString(self):
        objektiUString = []
        for go in GameObject.allGameObjects: #saljemo podatke koji su potrebni da bi se napravili objekti na klijentu
            objektiUString.append(str(go.id) + "%" + go.loadedSprite + "%" + str(go.x) + "%" + str(go.y) + "%" + str(go.w) + "%" + str(go.h))
        return "#".join(objektiUString)

    # ova metoda moze ici u GameObject Klasu
    def CreateUpdateObjectsString(self):
        objektiUString = []
        for go in GameObject.allGameObjects: #saljemo podatke koji su potrebni da bi se updateovale pozicije objekata na klijentu

            #optimizovano, ne saljem update za sve gameObjecte vec samo one koji su u lejeru prepreke i imaju neku brzinu
            if go.layer == Config.layerPrepreke and go.speed != 0:
                objektiUString.append(str(go.id) + "%" + str(go.x) + "%" + str(go.y))
            elif go.layer == Config.layerZabe or go.layer == Config.layerLilypad: #igraci i lokvanji mogu da promene sprite i zato saljem i sprite :D
                objektiUString.append(str(go.id) + "%" + str(go.x) + "%" + str(go.y) + "%" + str(go.loadedSprite))

        return "#".join(objektiUString)

    #ova funkcija se poziva na klijentu, da napravi objekte iste kao sto su na serveru. Pozove se samo na pocetku
    def GenerateObjects(self, data):
        objs = data.split("#")
        Rectangle.ResetId()
        for obj in objs:
            objData = obj.split("%")
            r = Rectangle(int(objData[2]), int(objData[3]), int(objData[4]), int(objData[5]), objData[1], layer=objData[0])
            r.Show()

    #ova funkcija se poziva na klijentu, sluzi za updateovanje (samo X i Y kordinate) svih rectanglova na klijentu.
    #server ce ovo slati klijentu svaki frejm (30 puta u sekundi)
    def UpdateObjectsPosition(self, data):
        objs = data.split("#")
        dictObj = {}
        for obj in objs:
            objData = obj.split("%")

            if len(objData) == 4:
                dictObj[objData[0]] = (float(objData[1]), float(objData[2]), objData[3])
            elif len(objData) == 3:
                dictObj[objData[0]] = (float(objData[1]), float(objData[2]))

        for go in GameObject.allGameObjects:
            strId = str(go.id)
            if strId in dictObj.keys():
                go.SetPosition(dictObj[strId][0], dictObj[strId][1])
                if len(dictObj[strId]) == 3: #ako je 3 znaci da imamo i sprite poslat
                    go.ChangeSprite(dictObj[strId][2])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Frogger()
    sys.exit(app.exec_())
