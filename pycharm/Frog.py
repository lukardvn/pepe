from Rectangle import Rectangle
from PyQt5.QtCore import Qt

from Config import Config

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

    def __init__(self,x,y, isPlayerTwo = False):
        self.sprite = self.spriteUpP1
        if isPlayerTwo:
            self.sprite = self.spriteUpP2

        super().__init__(x * Config.gridSize,y * Config.gridSize,self.height,self.width, self.sprite)
        self.isPlayerTwo = isPlayerTwo

    def Move(self, x,y):
        currentPosition = super().GetPosition()
        newXcoord = currentPosition[0] + Config.gridSize * x
        newYcoord = currentPosition[1] + Config.gridSize * y
        super().SetPosition(newXcoord, newYcoord)

    def GoLeft(self):
        x, y = self.GetPosition()
        if x == 0 :
            return

        self.Move(-1,0)
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteLeftP2)
        else:
            self.ChangeSprite(self.spriteLeftP1)

    def GoRight(self):
        x, y = self.GetPosition()
        if x == Config.gridSize * (Config.mapSize -1 ) :
            return

        self.Move(1,0)
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteRightP2)
        else:
            self.ChangeSprite(self.spriteRightP1)
    def GoUp(self):
        x, y = self.GetPosition()
        if y == 0 :
            return
        self.Move(0,-1)
        self.GetPosition()
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteUpP2)
        else:
            self.ChangeSprite(self.spriteUpP1)
    def GoDown(self):
        x, y = self.GetPosition()
        if y == Config.gridSize * (Config.mapSize -1 ) :
            return
        self.Move(0,1)
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteDownP2)
        else:
            self.ChangeSprite(self.spriteDownP1)

    def KeyPress(self, key):
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