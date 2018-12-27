from Rectangle import Rectangle
from Config import Config


class Obstacle(Rectangle):
    speed = 0

    def __init__(self, x, y, w, h, s):
        self.sprite = 'safeLane.png'
        self.speed = s
        self.buffer = 40
        super().__init__(x, y, w, h, self.sprite, layer=Config.layerPrepreke)

    def update(self):
        x,y = self.GetPosition()

        self.SetPosition(x + self.speed, self.y)
        if self.speed > 0 and self.x > Config.gridSize * Config.mapSize:
            self.SetPosition(-self.w - self.buffer, y)
        elif self.speed < 0 and self.x + self.w < 0:
            self.SetPosition(Config.gridSize * Config.mapSize + self.buffer, y)