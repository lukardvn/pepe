from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from Rectangle import Rectangle
from Config import Config


class Obstacle(Rectangle):
    speed = 0

    def __init__(self, x, y, w, h, s):
        super().__init__(x, y, w, h)
        self.sprite = 'car_obstacle.png'
        self.speed = s

    def update(self):
        self.x = self.x + self.speed

        if self.speed > 0 and self.x > Config.gridSize:
            #x = -self.w - Config.gridSize
            self.x, self.y = self.SetPosition(-self.w - Config.gridSize, self.y)
        elif self.speed < 0 and self.x + self.w < Config.gridSize:
            #x = self.w + Config.gridSize
            self.x, self.y = self.SetPosition(self.w + Config.gridSize, self.y)