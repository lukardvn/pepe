from Rectangle import Rectangle
from Config import Config
import random


class Obstacle(Rectangle):
    speed = 0

    def __init__(self, x, y, s, isLogLane=False, sprite=None, width=None, toFollow=None, laneSpacing=0):
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
                self.buffer = 150
            else:
                self.sprite, w = Obstacle.getRandomLog(s)
                self.buffer = 330

        self.laneSpacing = laneSpacing #spejsing u lejnu u kom se ovaj objekat nalazi
        self.following = toFollow #objekat iza kog se krece trenutni objekat

        self.speed = s
        h = 50
        super().__init__(x, y, w, h, self.sprite, layer=Config.layerPrepreke)
        super().AddToLayer(layer)

    def setLaneSpacing(self, spacing):
        self.laneSpacing = spacing

    def setObjectToFollow(self, obstacle):
        if self != obstacle:
            self.following = obstacle

    def update(self):
        self.MoveObstacle()

        if self.speed > 0:
            self.CheckIfBehindRightEdge()
        else:
            self.CheckIfBehindLeftEdge()

    def MoveObstacle(self):
        if self.speed != 0:
            self.SetPosition(self.x + self.speed, self.y)  # prvo pomerimo objekat pa onda proverimo da li je izasao iz ekrana

    def CheckIfBehindRightEdge(self):
        if self.x > Config.gridSize * Config.mapSize + self.buffer: #ako se obstacle krece u desno
            if self.following != None:  #ovde ce uci kada u lejnu ima vise od 2 obstacle-a
                positionXBehindIdol = self.following.x - self.laneSpacing - self.w #izracuna se nova kordinata X (iza objekta koji se prati). Treba da bude van ekrana (sa leve strane)

                if positionXBehindIdol > -self.w: #provera da li je ta kordinata unutar vidljivog dela ekrana, ako jeste onda se postavi da bude van ekrana
                    positionXBehindIdol = -1 * (self.w + 15)

                self.SetPosition(positionXBehindIdol, self.y)
            else:
                #znaci da u laneu ima samo jedan obstacle
                self.SetPosition(-self.w, self.y)

    def CheckIfBehindLeftEdge(self):
        if self.x + self.w + self.buffer < 0:
            if self.following != None: #ovde ce uci kada u lejnu ima vise od 2 obstacle-a
                positionXBehindIdol = self.following.x + self.following.w + self.laneSpacing #izracuna se nova kordinata X (iza objekta koji se prati). Treba da bude van ekrana (sa desne strane)

                if positionXBehindIdol < Config.mapSize * Config.gridSize: #ako je nova kordinata na vidljivo delu (nije dovoljno velika) onda se postavi da bude van ekrana
                    positionXBehindIdol = Config.mapSize * Config.gridSize + 15

                self.SetPosition(positionXBehindIdol, self.y)
            else:
                # znaci da u laneu ima samo jedan obstacle
                self.SetPosition(Config.gridSize * Config.mapSize, self.y)

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

if __name__ == '__main__':
    pass