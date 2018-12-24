from Rectangle import Rectangle
from PyQt5.QtCore import Qt

from Config import Config

class Frog(Rectangle):
    # height = 50
    # width = 50
    height = Config.gridSize
    width = Config.gridSize

    def __init__(self,x,y, isPlayerTwo = False):
        self.sprite = 'frog_sprite_50.png'
        if isPlayerTwo:
            self.sprite = 'frog_sprite_player2_50.png'

        super().__init__(x * Config.gridSize,y * Config.gridSize,self.height,self.width, self.sprite)
        self.isPlayerTwo = isPlayerTwo

    def Move(self, x,y):
        currentPosition = super().GetPosition()
        newXcoord = currentPosition[0] + Config.gridSize * x
        newYcoord = currentPosition[1] + Config.gridSize * y
        super().SetPosition(newXcoord, newYcoord)

    def GoLeft(self):
        self.Move(-1,0)
    def GoRight(self):
        self.Move(1,0)
    def GoUp(self):
        self.Move(0,-1)
    def GoDown(self):
        self.Move(0,1)

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