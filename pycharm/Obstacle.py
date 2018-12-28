from Rectangle import Rectangle
from Config import Config
import random


class Obstacle(Rectangle):
    speed = 0

    def __init__(self, x, y, s, isLogLane=False, sprite=None, width=None):
        self.sprite = ''
        layer = Config.layerDefault

        if isLogLane:
            layer = Config.layerDrva

        if sprite != None and width != None:
            self.sprite = sprite
            w = width
        else:
            if not isLogLane:
                self.sprite, w = Obstacle.getRandomCar(s)
            else:
                self.sprite, w = Obstacle.getRandomLog(s)

        self.speed = s
        self.buffer = 70
        h = 50
        super().__init__(x, y, w, h, self.sprite, layer=Config.layerPrepreke)
        super().AddToLayer(layer)

    def update(self):
        x,y = self.GetPosition()

        self.SetPosition(x + self.speed, self.y)
        if self.speed > 0 and self.x > Config.gridSize * Config.mapSize:
            self.SetPosition(-self.w - self.buffer, y)
        elif self.speed < 0 and self.x + self.w < 0:
            self.SetPosition(Config.gridSize * Config.mapSize + self.buffer, y)

    @staticmethod
    def getRandomSprite(availableSprites, speed):
        direction = "_right"

        if speed < 0:
            direction = "_left"

        key = random.choice(list(availableSprites.keys()))

        return (key + direction + ".png", availableSprites[key])

    @staticmethod
    def getRandomCar(speed):
        return Obstacle.getRandomSprite(Config.availableCars, speed)

    @staticmethod
    def getRandomTruck(speed):
        return Obstacle.getRandomSprite(Config.availableTrucks, speed)

    @staticmethod
    def getRandomLog(speed):
        return Obstacle.getRandomSprite(Config.availableLogs, speed)

    @staticmethod
    def getSmallLog(x,y, speed):
        sprite = "log_small_left.png"
        if speed > 0:
            sprite = "log_small_right.png"

        return Obstacle(x,y,speed, sprite=sprite,width=120)

    @staticmethod
    def getMediumLog(x, y, speed):
        sprite = "log_medium_left.png"
        if speed > 0:
            sprite = "log_medium_right.png"

        return Obstacle(x, y, speed, sprite=sprite, width=158)

    @staticmethod
    def getLargeLog(x, y, speed):
        sprite = "log_large_left.png"
        if speed > 0:
            sprite = "log_large_right.png"

        return Obstacle(x, y, speed, sprite=sprite, width=310)

