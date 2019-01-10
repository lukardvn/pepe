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
from NetworkCommunication import Client, Host
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QDir, Qt, QUrl

class Frogger(QWidget):
    def __init__(self):
        super().__init__()
        Config.mainWindow = self #odma se postavi koji objekat je mainWindow da bi tamo u Rectangle.py Qlabeli znali gde treba da se nacrtaju. Lose je resenje, al radi bar za testiranje
        self.Menu = None  # glavni meni
        self.InitFlagsAndVariables();

        self.scoreboard = Scoreboard(self)
        self.highscore = HighScore()
        self.highscore.readFromFile()

        ###############################################
        #self.videoWidget = QVideoWidget(self)
        #self.videoWidget.resize(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize)
        #self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        ###############################################

        self.setWindowState(Qt.WindowNoState)
        self.__init_ui__()

        self.key_notifier = KeyNotifier()
        self.key_notifier.key_signal.connect(self.__update_position__)
        self.key_notifier.start()

        self.queue = Queue()
        self.procUKomZiviZevs = Zeus.PokreniZevsa(self.queue) #pokrece proces koji u kju stavlja kakvo vreme treba da bude (sunce, kisa, sneg)

    def InitFlagsAndVariables(self):
        self.Map = []  # lista lejnova
        self.previousWeather = 'n'
        self.player1 = None
        self.player2 = None
        self.player1RectId = -1  # ovo je potrebno za mrezu
        self.player2RectId = -1  # ovo je potrebno za mrezu

        self.isHost = False
        self.isClient = False
        self.host = None
        self.client = None

        self.gamePaused = False

        self.GameOverBrojac = 0  # za zivote, ako je 2PlayerMode, kad igrac izgubi sve zivote povecava brojac za 1, kad oba izgube sve zivote, brojac je 2 i tad je gameOver
        # ako je SinglePlayer mod onda je gameOver ako je brojac 1
        self.Level = 1  # za levele

        Config.p1Score = 0
        Config.p2Score = 0
        Config.p1Lives = 5
        Config.p2Lives = 5

    # def initVideo(self):
    #     self.mediaPlayer.setVideoOutput(self.videoWidget)
    #     self.mediaPlayer.setMedia(QMediaContent(QUrl(Config.spriteLocation + "Intro.wmv")))
    #     self.mediaPlayer.setVideoOutput(self.videoWidget)
    #     self.videoWidget.show()
    #     self.mediaPlayer.play()

    def __init_ui__(self):
        self.DisplayMainMenu()
        self.setWindowTitle('Frogger')
        self.setWindowIcon(QtGui.QIcon(Config.spriteLocation+'iconFrog.png')) #ikonica
        self.resize(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize + 50)
        self.FixWindowSize()
        #self.initVideo()
        #q = QTimer()
        #q.singleShot(6000, self.DisplayMainMenu)
        self.show()

    def HsFunkc(self):
        self.Menu.HsElementsShow(self.highscore.top3)

    #obicna funkcija za fiksiranje velicine prozora
    def FixWindowSize(self):
        self.setMinimumHeight((Config.mapSize+1) * Config.gridSize)
        self.setMinimumWidth(Config.mapSize * Config.gridSize)
        self.setMaximumHeight((Config.mapSize+1) * Config.gridSize)
        self.setMaximumWidth(Config.mapSize * Config.gridSize)

    def DisplayMainMenu(self):
        #self.mediaPlayer.stop()
        #self.mediaPlayer.setVideoOutput(None)
        #self.videoWidget.setGeometry(0, 0, 0, 0)
        #self.videoWidget.hide()
        #self.videoWidget = None
        self.Menu = None
        self.Menu = Meni(self, self.SinglePlayerMode, self.TwoPlayerMode, self.HsFunkc, self.MainMenuHostClick,self.MainMenuJoinClick, self.CloseWindow)

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
        self.DisplayMap() #u displayMap se kreira objekat self.updaterGameObjekataThread i zato DisplayMap mora ici prvi
        self.createThreadToUpdateGameObjects()
        self.startThreadForUpdatingGameObjects()
        self.scoreboard.ShowScore()
        self.CreatePlayers()
        Config.collectLilypadsToAdvanceLevel = 1

    def ClearZeusQueue(self):
        while not self.queue.empty():
            self.queue.get()

    def TwoPlayerMode(self, OverNetworkGame = False):
        self.ClearZeusQueue()
        self.Menu.HideMainMenu()
        if not OverNetworkGame: #kad je preko mreze onda updateovanje krece kad klijent bude spreman
            self.createThreadToUpdateGameObjects()
            self.startThreadForUpdatingGameObjects()
        self.DisplayMap(TwoPlayers=True)
        self.scoreboard.ShowScores()
        self.CreatePlayers(TwoPlayers=True)
        Config.collectLilypadsToAdvanceLevel = 1

    def MainMenuHostClick(self):
        self.HostServer(Config.serverAddress, Config.serverPort)

    def MainMenuJoinClick(self):
        #self.Menu.JoinWidgetHide()
        self.setFocus()

        #ovde sacuvamo ip adresu i port u fajl. da kad se sledeci put upali igra da odma ucita tu ipadresu i port
        try:
            with open(Config.lastIp_filename, "w") as f:
                f.write(str(self.Menu.ipAddr) + ":" + str(self.Menu.port))
        except:
            pass

        self.JoinServer(self.Menu.ipAddr, int(self.Menu.port))

    def CreatePlayers(self, TwoPlayers=False):
        self.player1 = Frog(Config.player1StartPosition[0], Config.player1StartPosition[1], self.GameOverCheck, self.updateP1Score, self.createGreenLives)
        self.player1RectId = self.player1.id
        if TwoPlayers:
            self.player2 = Frog(Config.player2StartPosition[0], Config.player2StartPosition[1], self.GameOverCheck, self.updateP2Score, self.createPinkLives, isPlayerTwo=True)
            self.player2RectId = self.player2.id

    def updateP1Score(self, newScore):
        self.scoreboard.updateP1Score(newScore)
        if self.isHost:
            self.host.SendToClient(Config.network_updateGameScoreAndLives + ":" + "P1S_" + str(newScore)) #P2L => Player 2 Lives

    def updateP2Score(self, newScore):
        self.scoreboard.updateP2Score(newScore)
        if self.isHost:
            self.host.SendToClient(Config.network_updateGameScoreAndLives + ":" + "P2S_" + str(newScore)) #P2L => Player 2 Lives

    def createPinkLives(self, lives):
        self.scoreboard.CreatePinkLives(lives)
        if self.isHost:
            self.host.SendToClient(Config.network_updateGameScoreAndLives + ":" + "P2L_" + str(lives)) #P2L => Player 2 Lives

    def createGreenLives(self, lives):
        self.scoreboard.CreateGreenLives(lives)
        if self.isHost:
            self.host.SendToClient(Config.network_updateGameScoreAndLives + ":" + "P1L_" + str(lives))#P1L => Player 2 Lives

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

    def GameOverCheck(self, isPlayerTwo):
        #fja koja se poziva kada igrac ima 0 zivota, prosledjuje se igracima kroz konstruktor
        self.GameOverBrojac += 1
        if self.player1 != None and self.player2 != None:
            if self.GameOverBrojac == 1:
                if isPlayerTwo:
                    self.highscore.checkIfHighScore(self.player2.playerName, self.player2.score)
                    self.player2.RemoveFromScreen()
                    self.player2 = None
                    Config.p2Lives = 0
                else:
                    self.highscore.checkIfHighScore(self.player1.playerName, self.player1.score)
                    self.player1.RemoveFromScreen()
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
        self.scoreboard.HideScores()
        self.Menu.kisa.hide()
        self.Menu.sneg.hide()

        self.InitFlagsAndVariables()

        # javimo klijentu da bi se vratio na meni
        if self.isHost:
            self.host.SendToClient("CONN_ERROR")

    def LevelPassed(self):
        #fja koja se poziva kad su svih 5 Lilypada popunjena, prosledjuje se u konstruktoru, prvo finalLejnu pa samim objektima
        self.Level += 1
        Lane.ResetLaneStartingIndex()
        self.GameOverBrojac = 0
        self.DeleteMap()
        if self.player1 != None and self.player2 != None:
            Config.p1Score = self.player1.score
            Config.p2Score = self.player2.score
            Config.p1Lives = self.player1.lives
            Config.p2Lives = self.player2.lives
            self.DisplayMap(TwoPlayers=True)
            self.CreatePlayers(TwoPlayers=True)
        elif self.player1 != None:
            Config.p1Score = self.player1.score
            Config.p1Lives = self.player1.lives
            self.DisplayMap()
            self.CreatePlayers()
        elif self.player2 != None:
            Config.p2Score = self.player2.score
            Config.p2Lives = self.player2.lives
            self.DisplayMap()
            self.CreatePlayers(TwoPlayers=True)
            self.player1.RemoveFromScreen()
            self.player1 = None
        #TODO: TREBA DODATI DA JAVI KLIJENTU DA SE UPDATEUJE LEVEL

        if self.isHost and self.player2 != None:
            self.SendClientToReplicateObjects()

    def DeleteMap(self, deleteP1=False, deleteP2=False):
        if deleteP1:
            try:
                self.player1.RemoveFromScreen()
                self.player1 = None
            except:
                print('P1 vec postavljen na None')

        if deleteP2:
            try:
                self.player2.RemoveFromScreen()
                self.player2 = None
            except:
                print('P2 vec postavljen na None')

        for lane in self.Map:
            for obs in lane.obstacles:
                obs.RemoveFromScreen()
            lane.obstacles.clear()
            lane.RemoveFromScreen()

        for layer, listOfRectanglesInLayer in Rectangle.allRectangles.items():
            for rect in listOfRectanglesInLayer:
                rect.RemoveFromScreen()
            listOfRectanglesInLayer.clear()

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
        if not self.isClient:
            if key == Qt.Key_Escape and self.gamePaused:
                self.ResumeGame()
            elif key == Qt.Key_Escape and not self.gamePaused:
                self.PauseGame()

        if self.isClient:   #ako sam klijent onda pored pomeranja zabe, hocu da posaljem INPUT serveru
            if key == Qt.Key_Right:
                self.client.SendToServer(Config.network_inputKlijentaPrefix + "DESNO")
            elif key == Qt.Key_Down:
                self.client.SendToServer(Config.network_inputKlijentaPrefix + "DOLE")
            elif key == Qt.Key_Up:
                self.client.SendToServer(Config.network_inputKlijentaPrefix + "GORE")
            elif key == Qt.Key_Left:
                self.client.SendToServer(Config.network_inputKlijentaPrefix + "LEVO")

        if key == Qt.Key_T:
            for go in GameObject.allGameObjects:
                print(str(go.id) +"__"+ str(go.loadedSprite))

        if self.gamePaused: #sve sto je ispod nece biti odradjeno kad je game pauziran
            return

        if self.player1 != None:
            self.player1.KeyPress(key)
        if self.player2 != None:
            self.player2.KeyPress(key)


    def CloseWindow(self):
        # OVDE TREBA DA SE POZOVE KOD KOJI CE DA ZAUSTAVI ZEVSA
        # (ako uopste postoji neko toliko jak da zaustavi zevsa)
        self.procUKomZiviZevs.terminate()

        try:
            self.updaterGameObjekataThread.updaterThreadWork = False  # self.updaterGameObjekataThread se kreira samo kad pocne IGRA. Ako budes na meniju i nista ne radis nece se kreirati
        except:
            pass
        self.key_notifier.die()

    def closeEvent(self, event):
        self.CloseWindow()

    def createThreadToUpdateGameObjects(self):
        self.updaterGameObjekataThread = GOUpdater()
        self.updaterGameObjekataThread.nekiObjekat.connect(self.updateAllGameObjects)

        #OVO (thread koji updateuje objekte) SE POKRECE KAD KLIJENT BUDE SPREMAN (nakon sto preuzme sve objekte i nacrta ih na ekranu), ili kad pocne neki od lokalnih game modova
        #self.updaterGameObjekataThread.start()

    def startThreadForUpdatingGameObjects(self):
        self.updaterGameObjekataThread.start()

    def stopThreadForUpdatingObjects(self):
        try: #na klijentu ovaj objekat za updateovanje ce biti null
            self.updaterGameObjekataThread.updaterThreadWork = False
        except:
            pass

    def updateAllGameObjects(self, dummy): #callback funkcija
        for gameObject in GameObject.allGameObjects:
            gameObject.update()

        # ako je instanca server i postoje gameobjekti onda da salje klijentu pozicije tih objekata
        if self.isHost and len(GameObject.allGameObjects) > 0:
            self.SendRectPositionUpdateToClient()

        if not self.queue.empty():
            self.updateWeather(self.queue.get())
        else:
            return


    def updateWeather(self, newWeather):
        if self.isHost:
            self.host.SendToClient(Config.network_updateWeatherInfo + ":" + newWeather)

        if newWeather == 'k':
            if self.previousWeather == 'k':
                self.ZaustaviKisu()
            elif self.previousWeather == 's':
                self.ZaustaviSneg()
            self.PokreniKisu()
        elif newWeather == 's':
            if self.previousWeather == 'k':
                self.ZaustaviKisu()
            elif self.previousWeather == 's':
                self.ZaustaviSneg()
            self.PokreniSneg()
        elif newWeather == 'n':
            if self.previousWeather == 'k':
                self.ZaustaviKisu()
            elif self.previousWeather == 's':
                self.ZaustaviSneg()

        self.previousWeather = newWeather

    def createLanes(self, niz, type):
        #funkcija koja generise lejnove u zavisnosti od prosledjenog niza i karaktera u njemu
        if type == 'Road':
            for letter in niz:
                if letter == 'e':
                    self.Map.append(Lane.GenerateEasyLane())
                elif letter == 'm':
                    self.Map.append(Lane.GenerateMediumLane())
                elif letter == 'h':
                    self.Map.append(Lane.GenerateHardLane())
        elif type == 'Water':
            for letter in niz:
                if letter == 'e':
                    self.Map.append(Lane.GenerateEasyWaterLane())
                elif letter == 'm':
                    self.Map.append(Lane.GenerateMediumWaterLane())
                elif letter == 'h':
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

    def SendClientToReplicateObjects(self):
        self.host.SendToClient(Config.network_kreirajSveObjekteNaKlijentu + ":" + self.CreateInitObjectsString())

    # ovo ce biti pozvano kad server primi poruku od klijenta
    def ReceiveFromClient(self, data):
        # print("Primio od klijenta: " + str(data))
        if data == Config.network_clientIsReady:  # kad primi ovo znaci da se klijent povezao
            self.TwoPlayerMode(OverNetworkGame=True)
            Config.collectLilypadsToAdvanceLevel = 3
            self.player2.keyBoardInputEnabled = False
            self.SendClientToReplicateObjects()                             #da ne generise updater svaki put kad se predje level, vec samo incijalno kad se uspostavi veza
        elif data == Config.network_potvrdaKlijentaDaJeNapravioSveObjekte and self.Level == 1:  # klijent je potvrdio da je napravio sve objekte i sad pokrecemo igru (pravimo i pokrecemo thread koji updateuje igru)
            self.createThreadToUpdateGameObjects()
            self.startThreadForUpdatingGameObjects()
        elif Config.network_inputKlijentaPrefix in data and self.player2 != None: #ovo da li je igrac razlicit od None je ustvari provera da li je ziv
            if Config.network_inputKlijentaPrefix + "DESNO" == data:
                self.player2.GoRight()
            elif Config.network_inputKlijentaPrefix + "DOLE" == data:
                self.player2.GoDown()
            elif Config.network_inputKlijentaPrefix + "GORE" == data:
                self.player2.GoUp()
            elif Config.network_inputKlijentaPrefix + "LEVO" == data:
                self.player2.GoLeft()
        elif "CONN_ERROR" == data:
            print("Klijent je otiso :(")
            self.ResetGameStateOnError()

    # ovo ce biti pozvano kad klijent primi poruku od servera
    def ReceiveFromServer(self, data):
        #print("Primio od servera: " + str(data))
        if data == Config.network_serverWelcomeMsg:  # znaci da smo se uspesno povezali sa serverom i inicijalizujemo gejm
            self.InitNetworkGame()
        elif Config.network_kreirajSveObjekteNaKlijentu in data:
            self.GenerateObjects(data.split(":")[1])
            self.client.SendToServer(Config.network_potvrdaKlijentaDaJeNapravioSveObjekte)
        elif Config.network_updateSveObjekteNaKlijentu in data:
            self.UpdateObjectsPosition(data.split(":")[1])
        elif Config.network_updateGameScoreAndLives in data:
            #ako ovde udje PAYLOAD moze da izgleda ovako:
            #P2L_3
            #P1S_2
            #P2S_4
            #P1L_1
            payload = data.split(":")[1]
            player, scoreOrLives = payload.split('_')
            #print(str(payload))
            if "P1" in player:
                if "S" in player:
                    self.updateP1Score(scoreOrLives)
                elif "L" in player:
                    self.createGreenLives(int(scoreOrLives))
            elif "P2" in player:
                if "S" in player:
                    self.updateP2Score(scoreOrLives)
                elif "L" in player:
                    self.createPinkLives(int(scoreOrLives))

        elif Config.network_updateWeatherInfo in data:
            self.updateWeather(data.split(":")[1])
        elif "CONN_ERROR" == data:
            self.ResetGameStateOnError()

    #ovo se poziva na klijentu.
    def InitNetworkGame(self):
        self.TwoPlayerMode(OverNetworkGame=True) #nije potrebno ovo True, al da se dzabe nebi pravio thread koji se ne koristi :D

        #sklanjamo sve objekte, jer ce nam server poslati sta je on generisao (velicine, pozicije, sprajtove)
        for go in GameObject.allGameObjects:
            go.RemoveFromScreen()
        GameObject.allGameObjects.clear()
        #klijent javi serveru da je spreman (spreman da primi podatke o svim objektima)
        self.client.SendToServer(Config.network_clientIsReady)

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
        self.GameOver()

    #poziva se samo na serveru
    def SendRectPositionUpdateToClient(self):
        self.host.SendToClient(Config.network_updateSveObjekteNaKlijentu + ":" + self.CreateUpdateObjectsString())

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

        # ovo je dodato ako neki od igraca umre da ga klijent skloni sa ekrana (sprite se stavi na prazan string)
        if self.player1 == None and self.player1RectId != -1:
            objektiUString.append(str(self.player1RectId) + "%" + str(0) + "%" + str(0) + "%DEAD")
            self.player1RectId = -1
        if self.player2 == None and self.player2RectId != -1:
            objektiUString.append(str(self.player2RectId) + "%" + str(0) + "%" + str(0) + "%DEAD")
            self.player2RectId = -1

        return "#".join(objektiUString)

    #ova funkcija se poziva na klijentu, da napravi objekte iste kao sto su na serveru. Pozove se samo na pocetku
    def GenerateObjects(self, data):
        for layer, listOfRects in Rectangle.allRectangles.items():
            for rect in listOfRects:
                rect.RemoveFromScreen()
            listOfRects.clear()


        objs = data.split("#")
        Rectangle.ResetId()
        for obj in objs:
            objData = obj.split("%")
            r = Rectangle(float(objData[2]), float(objData[3]), int(objData[4]), int(objData[5]), objData[1], layer=objData[0], forceId=int(objData[0]))
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
