from Rectangle import Rectangle
from Config import Config


class Obstacle(Rectangle):
    speed = 0

    def __init__(self, x, y, w, h, s):
        self.sprite = ''
        if Config.yLane > 450:
            self.sprite = 'car_1_right.png'
            if s < 0:
                self.sprite = "car_1_left.png"
        elif Config.yLane <= 450:
            if Config.indexHelper == 6:
                #Config.obstacleHelper1 = 77
                if s > 0:
                    self.sprite = 'log_small_right.png'
                else:
                    self.sprite = 'log_small_left.png'
            elif Config.indexHelper == 7:
                #Config.obstacleHelper2 = 78
                if s > 0:
                    self.sprite = 'log_medium_right.png'
                else:
                    self.sprite = 'log_medium_left.png'
            elif Config.indexHelper == 8:
                #Config.obstacleHelper3 = 79
                if s > 0:
                    self.sprite = 'log_medium_right.png'
                else:
                    self.sprite = 'log_medium_left.png'
            elif Config.indexHelper == 9:
                if s > 0:
                    self.sprite = 'log_large_right.png'
                else:
                    self.sprite = 'log_large_left.png'
        self.speed = s
        self.buffer = 70
        super().__init__(x, y, w, h, self.sprite, layer=Config.layerPrepreke)

    def update(self):
        x,y = self.GetPosition()

        self.SetPosition(x + self.speed, self.y)
        if self.speed > 0 and self.x > Config.gridSize * Config.mapSize:
            self.SetPosition(-self.w - self.buffer, y)
        elif self.speed < 0 and self.x + self.w < 0:
            self.SetPosition(Config.gridSize * Config.mapSize + self.buffer, y)