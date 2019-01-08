from Rectangle import Rectangle
from PyQt5.QtCore import Qt, pyqtSignal, QThread

from Config import Config
import time
import random

class Frog(Rectangle):
    # height = 50
    # width = 50
    height = Config.gridSize
    width = Config.gridSize

    spriteUpP1 = 'frog_sprite_50.png'
    spriteLeftP1 = 'frog_sprite_l_50.png'
    spriteRightP1 = 'frog_sprite_r_50.png'
    spriteDownP1 = 'frog_sprite_d_50.png'

    spriteUpP2 = 'frog_sprite_player2_50.png'
    spriteLeftP2 = 'frog_sprite_player2l_50.png'
    spriteRightP2 = 'frog_sprite_player2r_50.png'
    spriteDownP2 = 'frog_sprite_player2d_50.png'

    def __init__(self, x, y, funkcijaZaGejmover, funkcijaZaScoreboard, funkcijaZaZivote, isPlayerTwo = False):
        self.startX = x
        self.startY = y
        self.logSpeed = 0

        self.playerName = Config.p1Name
        self.sprite = self.spriteUpP1
        self.keyBoardInputEnabled = True #koristi se za mulitplejer (tad se postavi na False), da ne moze drugi igrac da se kontrolise kad je multiplayer mod
        
        self.lives = Config.p1Lives
        self.score = Config.p1Score

        if isPlayerTwo:
            self.playerName = Config.p2Name
            self.sprite = self.spriteUpP2
            self.lives = Config.p2Lives
            self.score = Config.p2Score

        super().__init__(x * Config.gridSize,y * Config.gridSize,self.height,self.width, self.sprite, layer=Config.layerZabe)
        self.isPlayerTwo = isPlayerTwo
        #print(self.isPlayerTwo)
        #print(isPlayerTwo)
        self.GameOver = funkcijaZaGejmover
        self.funkcijaZaScoreboard = funkcijaZaScoreboard
        self.funkcijaZaZivote = funkcijaZaZivote
        self.Show()

        self.funkcijaZaScoreboard(self.score)
        self.funkcijaZaZivote(self.lives)

    def update(self):
        if self.IsInWaterLane():
            if self.IsOnLog():
                # kad je zaba na drvetu i dodje do ivice ekrana, da zaba klizi po drvetu (ne menja svoju poziciju)
                if (self.x > Config.gridSize * Config.mapSize - self.w and self.logSpeed > 0) or (self.x < 1 and self.logSpeed < 0):
                    return

                self.SetPosition(self.x + self.logSpeed, self.y)
            else:
                self.Die()
        else:
            if self.CollidedWithObstacle():
                self.Die()

        lokvanj = self.CollidedWithLilypad()
        if lokvanj != None:
            lokvanj.usedByPlayer(self,Config.twoPl)

    def CollidedWithLilypad(self):
        return self.CollisionLayerSpecific(Config.layerLilypad, returnObject=True)

    def CollidedWithObstacle(self):
        return self.CollisionLayerSpecific(Config.layerPrepreke)

    def IsOnLog(self):
        objCollidedWith = self.CollisionLayerSpecific(Config.layerDrva, returnObject=True)
        if objCollidedWith != None:
            self.logSpeed = objCollidedWith.speed
            return True
        return False

    def IsInWaterLane(self):
        return self.CollisionLayerSpecific(Config.layerWaterLane)

    def Die(self):
        self.lives -= 1
        self.funkcijaZaZivote(self.lives)

        if self.lives == 0:
            self.ReturnToStart()
            self.GameOver(self.isPlayerTwo)

        if self.lives > 0:
            self.ReturnToStart()

    def UpdateScore(self):
        self.score += 1
        self.funkcijaZaScoreboard(self.score)

    def ReturnToStart(self):
        self.SetPosition(self.startX * Config.gridSize, self.startY * Config.gridSize)
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteUpP2)
        else:
            self.ChangeSprite(self.spriteUpP1)

    def Move(self, x,y):
        currentPosition = super().GetPosition()
        newXcoord = currentPosition[0] + Config.gridSize * x
        newYcoord = currentPosition[1] + Config.gridSize * y
        #print(newXcoord,newYcoord)
        self.deus(newXcoord,newYcoord)
        super().SetPosition(newXcoord, newYcoord)

    def deus(self,xCord,yCord):
        if xCord == 0 and yCord ==350:
            if random.randint(1,5) == 3:
                if self.lives < 6:
                    if self.isPlayerTwo:
                        Config.p2Lives = self.lives + 1
                        self.lives = Config.p2Lives
                        self.funkcijaZaZivote(self.lives)
                        #print(self.lives)
                        #print(Config.p2Lives)
                    else:
                        Config.p1Lives = self.lives + 1
                        self.lives = Config.p1Lives
                        self.funkcijaZaZivote(self.lives)
                        #print(self.lives)
                        #print(Config.p1Lives)
                else:
                    print("")

    def GoLeft(self):
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteLeftP2)
        else:
            self.ChangeSprite(self.spriteLeftP1)

        if self.x == 0 :
            return

        if not self.IsEmpty(-1, 0):
            return

        self.Move(-1,0)

    def GoRight(self):
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteRightP2)
        else:
            self.ChangeSprite(self.spriteRightP1)

        if self.x == Config.gridSize * (Config.mapSize - 1):
            return

        if not self.IsEmpty(1,0):
            return

        self.Move(1,0)

    def GoUp(self):
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteUpP2)
        else:
            self.ChangeSprite(self.spriteUpP1)

        if self.y == 0:
            return

        self.CorrectXPositionToGrid()

        if not self.IsEmpty(0,-1):
            return

        self.Move(0,-1)

    def GoDown(self):
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteDownP2)
        else:
            self.ChangeSprite(self.spriteDownP1)

        self.CorrectXPositionToGrid()

        if self.y == Config.gridSize * (Config.mapSize - 1):
            return

        if not self.IsEmpty(0,1):
            return

        self.Move(0,1)

    def CorrectXPositionToGrid(self):
        if self.x % Config.gridSize >= 25:
            newX = self.x + (Config.gridSize - (self.x % Config.gridSize))
            self.SetPosition(newX, self.y)
        else:
            newX = self.x - (self.x % Config.gridSize)
            self.SetPosition(newX, self.y)

    def KeyPress(self, key):
        if self.keyBoardInputEnabled:   #bice false kad se igra multiplajer (za igraca 2 jer se on kontrolise preko mreze)
            if self.isPlayerTwo:
                if key == Qt.Key_D:
                    self.GoRight()
                elif key == Qt.Key_S:
                    self.GoDown()
                elif key == Qt.Key_W:
                    self.GoUp()
                elif key == Qt.Key_A:
                    self.GoLeft()
            else:
                if key == Qt.Key_Right:
                    self.GoRight()
                elif key == Qt.Key_Down:
                    self.GoDown()
                elif key == Qt.Key_Up:
                    self.GoUp()
                elif key == Qt.Key_Left:
                    self.GoLeft()

if __name__ == '__main__':
    pass
