import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtGui
from key_notifier import KeyNotifier
from Config import Config
from Frog import Frog
from GameObject import GameObject, GOUpdater
from Lane import Lane
from Rectangle import Rectangle
from random import shuffle, randrange
from Score import Scoreboard
from MainMenu import Meni
from Highscore import HighScore
import time, random
from multiprocessing import Queue
import Zeus


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

        self.GameOverBrojac = 0 # za zivote, ako je 2PlayerMode, kad igrac izgubi sve zivote povecava brojac za 1, kad oba izgube sve zivote, brojac je 2 i tad je gameOver
        # ako je SinglePlayer mod onda je gameOver ako je brojac 1
        self.Level = 1 # za levele

        self.scoreboard = Scoreboard(self)
        self.highscore = HighScore()
        self.highscore.readFromFile()

        self.setWindowState(Qt.WindowNoState)
        self.__init_ui__()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

        self.queue = Queue()
        Zeus.PokreniZevsa(self.queue)


    def __init_ui__(self):
        self.DisplayMainMenu()
        self.setWindowTitle('Frogger')
        self.setWindowIcon(QtGui.QIcon(Config.spriteLocation+'iconFrog.png')) #ikonica
        self.resize(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize + 50)
        self.FixWindowSize()
        self.show()
        #self.startThreadForUpdatingObjects()

    def HsFunkc(self):
        self.Menu.HsElementsShow(self.highscore.top3)

    #obicna funkcija za fiksiranje velicine prozora
    def FixWindowSize(self):
        self.setMinimumHeight((Config.mapSize+1) * Config.gridSize)
        self.setMinimumWidth(Config.mapSize * Config.gridSize)
        self.setMaximumHeight((Config.mapSize+1) * Config.gridSize)
        self.setMaximumWidth(Config.mapSize * Config.gridSize)

    def DisplayMainMenu(self):
        self.Menu = None
        self.Menu = Meni(self, self.SinglePlayerMode, self.TwoPlayerMode, self.HsFunc, self.MainMenuHostClick,self.MainMenuJoinClick)

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
        self.ClearZeusQueue()
        self.Menu.HideMainMenu()
        self.updaterGameObjekataThread.start()
        self.DisplayMap()
        self.scoreboard.ShowScore()
        self.CreatePlayers()

    def ClearZeusQueue(self):
        while not self.queue.empty():
            self.queue.get()

    def TwoPlayerMode(self):
        self.ClearZeusQueue()
        self.Menu.HideMainMenu()
        self.updaterGameObjekataThread.start()
        self.DisplayMap()
        self.DisplayMap(TwoPlayers=True)
        self.scoreboard.ShowScores()
        self.CreatePlayers(TwoPlayers=True)

    def MainMenuHostClick(self):
        self.HostServer(Config.serverAddress, Config.serverPort)

    def MainMenuJoinClick(self):
        self.JoinServer(Config.serverAddress, Config.serverPort)

    def CreatePlayers(self, TwoPlayers=False):
        self.player1 = Frog(Config.player1StartPosition[0], Config.player1StartPosition[1], self.GameOverCheck, self.scoreboard.updateP1Score, self.scoreboard.CreateGreenLives)
        if TwoPlayers:
            self.player2 = Frog(Config.player2StartPosition[0], Config.player2StartPosition[1], self.GameOverCheck, self.scoreboard.updateP2Score, self.scoreboard.CreatePinkLives, isPlayerTwo=True)
            #Config.twoPl = TwoPlayers

    def DisplayMap(self, TwoPlayers=False):
        self.Map.append(Lane.GenerateSafetyLane())  #prvi je uvek sejf lejn
        self.GenerateLanes('Road')    #fja da generise lejnove za put
        #self.Map.append(Lane.GenerateSafetyLane())
        ##ovaj ce da bude uvek tu da bi se moglo duze igrati
        ##lejn sa zivotom
        self.Map.append(Lane.GenerateSafetyLaneWithDeus())
        self.GenerateLanes('Water')   #fja da generise lejnove za reku
        if TwoPlayers:
            self.Map.append(Lane.GenerateFinalLane(self.LevelPassed)) # zadnji je uvek finalLane
        else:
            self.Map.append(Lane.GenerateFinalLane(self.LevelPassed, lilyPadPattern=Config.lilypadPatternBO5Standard))  # zadnji je uvek finalLane

        self.startThreadForUpdatingObjects()

    def GameOverCheck(self, isPlayerTwo):
        #fja koja se poziva kada igrac ima 0 zivota, prosledjuje se igracima kroz konstruktor
        self.GameOverBrojac += 1
        if self.player1 != None and self.player2 != None:
            if self.GameOverBrojac == 1:
                if isPlayerTwo:
                    self.highscore.checkIfHighScore(self.player2.playerName, self.player2.score)
                    self.player2.Hide()
                    self.player2 = None
                    Config.p2Lives = 0
                else:
                    self.highscore.checkIfHighScore(self.player1.playerName, self.player1.score)
                    self.player1.Hide()
                    self.player1 = None
                    Config.p1Lives = 0
        elif self.player1 != None:
            self.highscore.checkIfHighScore(self.player1.playerName, self.player1.score)
            self.GameOver()
        elif self.player2 != None:
            self.highscore.checkIfHighScore(self.player2.playerName, self.player2.score)
            self.GameOver()

    def GameOver(self):
        #fja koja se poziva kad su svi igraci igraci ostali bez zivota
        self.stopThreadForUpdatingObjects()
        self.DeleteMap(deleteP1=True, deleteP2=True)
        self.Menu.ShowMainMenu()
        Lane.ResetLaneStartingIndex()
        self.GameOverBrojac = 0
        self.Level = 1
        self.scoreboard.HideScores()
        Config.p1Score = 0
        Config.p2Score = 0
        Config.p1Lives = 5
        Config.p2Lives = 5
        self.Menu.kisa.hide()
        self.Menu.sneg.hide()

    def LevelPassed(self):
        #fja koja se poziva kad su svih 5 Lilypada popunjena, prosledjuje se u konstruktoru, prvo finalLejnu pa samim objektima
        self.stopThreadForUpdatingObjects()
        self.Level += 1
        Lane.ResetLaneStartingIndex()
        self.GameOverBrojac = 0
        if self.player1 != None and self.player2 != None:
            Config.p1Score = self.player1.score
            Config.p2Score = self.player2.score
            Config.p1Lives = self.player1.lives
            Config.p2Lives = self.player2.lives
            self.DeleteMap()
            self.DisplayMap(TwoPlayers=True)
            self.CreatePlayers(TwoPlayers=True)
        elif self.player1 != None:
            Config.p1Score = self.player1.score
            Config.p1Lives = self.player1.lives
            self.DeleteMap()
            self.DisplayMap()
            self.CreatePlayers()
        elif self.player2 != None:
            Config.p2Score = self.player2.score
            Config.p2Lives = self.player2.lives
            self.DeleteMap()
            self.DisplayMap()
            self.CreatePlayers(TwoPlayers=True)
            self.player1.Hide()
            self.player1 = None

    def DeleteMap(self, deleteP1=False, deleteP2=False):
        if deleteP1:
            try:
                self.player1.Hide()
                self.player1 = None
            except:
                print('P1 vec postavljen na None')

        if deleteP2:
            try:
                self.player2.Hide()
                self.player2 = None
            except:
                print('P2 vec postavljen na None')

        for lane in self.Map:
            for obs in lane.obstacles:
                obs.Hide()
            lane.obstacles.clear()
            lane.Hide()

        for rect in Rectangle.allRectangles[Config.layerLilypad]:
            rect.Hide()
        Rectangle.allRectangles[Config.layerLilypad].clear()

        for rect in Rectangle.allRectangles[Config.layerZabe]:
            rect.Hide()
        Rectangle.allRectangles[Config.layerZabe].clear()

        for rect in Rectangle.allRectangles[Config.layerDefault]:
            rect.Hide()
        Rectangle.allRectangles[Config.layerDefault].clear()

        self.Map.clear()

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
        self.padavina = 'n'

    def stopThreadForUpdatingObjects(self):
        self.updaterGameObjekataThread.updaterThreadWork = False

    def updateAllGameObjects(self, dummy):
        for gameObject in GameObject.allGameObjects:
            gameObject.update()

        # ako je instanca server i postoje gameobjekti onda da salje klijentu pozicije tih objekata
        if self.isHost and len(GameObject.allGameObjects) > 0:
            self.SendUpdateToClient()

        if not self.queue.empty():
            vremenskiUslov = self.queue.get()
            print(vremenskiUslov)
        else:
            return

        if vremenskiUslov == 'k':
            if self.padavina == 's':
                self.ZaustaviSneg()
            self.PokreniKisu()
            self.padavina = 'k'
        elif vremenskiUslov == 's':
            if self.padavina == 'k':
                self.ZaustaviKisu()
            self.PokreniSneg()
            self.padavina = 's'
        elif vremenskiUslov == 'n':
            if self.padavina == 'k':
                self.ZaustaviKisu()
            elif self.padavina == 's':
                self.ZaustaviSneg()
            self.padavina = 'n'

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

    def createLanes(self, niz, type):
        #funkcija koja generise lejnove u zavisnosti od prosledjenog niza i karaktera u njemu
        if type == 'Road':
            for i in range(len(niz)):
                if niz[i] == 'e':
                    self.Map.append(Lane.GenerateEasyLane())
                elif niz[i] == 'm':
                    self.Map.append(Lane.GenerateMediumLane())
                elif niz[i] == 'h':
                    self.Map.append(Lane.GenerateHardLane())
        elif type == 'Water':
            for i in range(len(niz)):
                if niz[i] == 'e':
                    self.Map.append(Lane.GenerateEasyWaterLane())
                elif niz[i] == 'm':
                    self.Map.append(Lane.GenerateMediumWaterLane())
                elif niz[i] == 'h':
                    self.Map.append(Lane.GenerateHardWaterLane())
        elif type == 'Random':
            for letter in niz:
                if letter == 's':  # safe lane
                    self.Map.append(Lane.GenerateSafetyLane())
                elif letter == 'e':  # easy lane, if generated -1 -> easyWaterLane if 1 easyTrafficLane, isto vazi za ostale samo se menja tezina s,m,h...
                    if [-1, 1][randrange(2)] == -1:
                        self.Map.append(Lane.GenerateEasyWaterLane())
                    else:
                        self.Map.append(Lane.GenerateEasyLane())
                elif letter == 'm':
                    if [-1, 1][randrange(2)] == -1:
                        self.Map.append(Lane.GenerateMediumWaterLane())
                    else:
                        self.Map.append(Lane.GenerateMediumLane())
                elif letter == 'h':
                    if [-1, 1][randrange(2)] == -1:
                        self.Map.append(Lane.GenerateHardWaterLane())
                    else:
                        self.Map.append(Lane.GenerateHardLane())

    def GenerateLanes(self, type):
        # 6 lejnova, fja u kojoj se odlucuje tezina po levelima, moze da se menja po volji
        nizTezine = []
        if self.Level <= 2:
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
        elif self.Level > 2 and self.Level <= 4:
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            type = 'Random'
        elif self.Level > 4 and self.Level <= 6:
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
        elif self.Level > 6 and self.Level <= 8:
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('e')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            type = 'Random'
        elif self.Level > 8 and self.Level <= 10:
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
        elif self.Level > 10 and self.Level <= 12:
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            type = 'Random'
        elif self.Level > 12 and self.Level <= 14:
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
        elif self.Level > 12 and self.Level <= 14:
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('m')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            type = 'Random'
        elif self.Level > 14 and self.Level <= 16:
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
        elif self.Level > 16:
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            nizTezine.append('h')
            type = 'Random'

        shuffle(nizTezine)  #permutuj niz da lejnovi budu random
        self.createLanes(nizTezine, type)

    def PokreniKisu(self):  #Fja da se prikaze kisa
        self.Menu.PrikaziPadavinu('kisa')
        for lane in self.Map:
            if lane.laneType == Config.laneTypeWater:
                lane.ChangeSpeed(Config.speedChange)    #brzina drveca se povecava kad je kisa
            elif lane.laneType == Config.laneTypeTraffic or lane.laneType == Config.laneTypeTrafficTop or lane.laneType == Config.laneTypeTrafficBottom:
                lane.ChangeSpeed(-Config.speedChange)   #brzina automobila se smanjuje kad je kisa

    def PokreniSneg(self): #Fja da se prikaze sneg
        self.Menu.PrikaziPadavinu('sneg')
        for lane in self.Map:
            if lane.laneType == Config.laneTypeWater:
                lane.ChangeSpeed(-Config.speedChange)   #brzina drveca se smanjuje kad je sneg
            elif lane.laneType == Config.laneTypeTraffic or lane.laneType == Config.laneTypeTrafficTop or lane.laneType == Config.laneTypeTrafficBottom:
                lane.ChangeSpeed(Config.speedChange)    #brzina automobila se povecava kad je sneg

    def ZaustaviKisu(self): #Fja da se zaustavi kisa
        self.Menu.SakrijPadavinu('kisa')
        for lane in self.Map:
            if lane.laneType == Config.laneTypeWater:
                lane.ChangeSpeed(-Config.speedChange)   #obrnuto, ako smo bili povecali brzinu drveca kad je kisa pocela, sad je smanjujemo, vracamo na default
            elif lane.laneType == Config.laneTypeTraffic or lane.laneType == Config.laneTypeTrafficTop or lane.laneType == Config.laneTypeTrafficBottom:
                lane.ChangeSpeed(Config.speedChange)    #obrnuto, ako smo bili smanjili brzinu automobila kad je kisa pocela, sad je povecavamo, vracamo na default

    def ZaustaviSneg(self): #Fja da se zaustavi sneg
        self.Menu.SakrijPadavinu('sneg')
        for lane in self.Map:
            if lane.laneType == Config.laneTypeWater:
                 lane.ChangeSpeed(Config.speedChange)   #obrnuto, ako smo bili smanjili brzinu drveca kad je poceo sneg, sad je povecavamo, vracamo na default
            elif lane.laneType == Config.laneTypeTraffic or lane.laneType == Config.laneTypeTrafficTop or lane.laneType == Config.laneTypeTrafficBottom:
                lane.ChangeSpeed(-Config.speedChange)   #obrnuto, ako smo bili povecali brzinu automobila kad je poceo sneg, sad je smanjujemo, vracamo na default

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Frogger()
    sys.exit(app.exec_())
