from Rectangle import Rectangle
from Config import Config
from Obstacle import  Obstacle
import random
from Lilypad import Lilypad
from Bush import Bush
from LilyDeus import LilyDeus
from Grass import Grass

class Lane(Rectangle):
    def __init__(self, numOfObs, speed, spacing, typeOfLane):
        self.laneType = typeOfLane
        self.numberOfObstacles = numOfObs
        self.speed = speed
        self.spacing = spacing
        self.obstacles = []

        self.offset = random.randint(int(65 * (abs(speed) * 0.3)), int(305  * (abs(speed) * 0.1)))
        if self.offset < 55:
            self.offset = 55

        self.sprite = Config.laneTypeToLaneSprite[self.laneType]

        layer = Config.layerDefault
        if self.laneType == Config.laneTypeWater:
            layer = Config.layerWaterLane

        laneYCoord = (Config.mapSize - Config.newLaneYIndex - 1) * Config.gridSize
        Config.newLaneYIndex += 1

        super().__init__(0, laneYCoord, Config.gridSize*Config.mapSize,  Config.gridSize, self.sprite, layer=layer)

        self.Show()
        if self.numberOfObstacles > 0:
            self.InitObstacles()

    def ChangeSpeed(self, speed):
        if self.speed > 0:
            for obj in self.obstacles:
                obj.speed += speed
        else:
            for obj in self.obstacles:
                obj.speed -= speed


    def InitObstacles(self):
        self.GenerateObstacles()
        self.SetFollowers()

    def GenerateObstacles(self):
        startingX = self.offset

        for i in range(self.numberOfObstacles):
            if self.laneType == Config.laneTypeWater:
                newObstacle = Obstacle(startingX, self.y, self.speed, isLogLane=True)
            else:
                newObstacle = Obstacle(startingX, self.y, self.speed)


            #u ovom bloku racuna X sledeceg obstaclea i po potrebi korektuje X trenutnog obstaclea :D
            if self.speed < 0:
                startingX = startingX + self.spacing + newObstacle.w
            else:
                startingX = startingX - self.spacing - newObstacle.w
                # mora da se uzme u obzir i sirina novog obstacle-a jer je X koridinata sa leve strane objekta (a objekat treba da se pojavi sa leve strane ekrana)
                newObstacle.SetPosition(startingX, self.y)


            # ovo je da bi offset ostao izmedju prvog i poslednjeg auta u lejnu kada se prvi auto ponovo pojavi
            if i == 0:
                newObstacle.setLaneSpacing(self.spacing + self.offset)
            else:
                newObstacle.setLaneSpacing(self.spacing)

            self.obstacles.append(newObstacle)

    def SetFollowers(self):
        #kad ima jedan obstacle, nece sam sebe pratiti zbog uslova u funkciji setObjectToFollow
        for i in range(len(self.obstacles) - 1):
            self.obstacles[i + 1].setObjectToFollow(self.obstacles[i])
            self.obstacles[i + 1].Show()

        self.obstacles[0].setObjectToFollow(self.obstacles[-1])
        self.obstacles[0].Show()

    @staticmethod
    def GenerateLane(availableConfigs, overrideLaneType=None):
        selectedConfig = random.randint(0, len(availableConfigs) - 1)
        config = availableConfigs[selectedConfig]

        direction = pow(-1,random.randint(0, 9))

        if overrideLaneType != None:
            return Lane(config[0], config[1] * direction, config[2], overrideLaneType)
        else:
            return Lane(config[0],config[1] * direction, config[2],config[3])

    @staticmethod
    def GenerateSafetyLane():
        return Lane(0,0,0,Config.laneTypeSafety)

    @staticmethod
    def GenerateSafetyLaneWithDeus(deusPattern=Config.safetyLaneDeusPattern):
        l = Lane(0, 0, 0, Config.laneTypeSafety)
        counter = 0
        for char in deusPattern:
            if char == "0":
                Grass(counter * Config.gridSize, l.y, 50, 50)
            elif char == "1":
                LilyDeus(counter * Config.gridSize, l.y, 50, 50)
            counter += 1

        if counter < Config.mapSize - 1:
            print("Sablon za lejn nije dobar")

        return l

    @staticmethod
    def GenerateEasyLane(overrideLaneType=None):
        return Lane.GenerateLane(Config.lanesEasyConfig, overrideLaneType=overrideLaneType)

    @staticmethod
    def GenerateMediumLane(overrideLaneType=None):
        return Lane.GenerateLane(Config.lanesMediumConfig, overrideLaneType=overrideLaneType)

    @staticmethod
    def GenerateHardLane(overrideLaneType=None):
        return Lane.GenerateLane(Config.lanesHardConfig, overrideLaneType=overrideLaneType)

    @staticmethod
    def GenerateEasyWaterLane(overrideLaneType=None):
        return Lane.GenerateLane(Config.lanesEasyWaterConfig, overrideLaneType=overrideLaneType)

    @staticmethod
    def GenerateMediumWaterLane(overrideLaneType=None):
        return Lane.GenerateLane(Config.lanesMediumWaterConfig, overrideLaneType=overrideLaneType)

    @staticmethod
    def GenerateHardWaterLane(overrideLaneType=None):
        return Lane.GenerateLane(Config.lanesHardWaterConfig, overrideLaneType=overrideLaneType)

    @staticmethod
    def GenerateFinalLane(funkcijaZaLilypad, lilyPadPattern = Config.lilypadPatternBO5Standard, randomPatternBO5=False):
        l = Lane(0,0,0, Config.laneTypeFinal) #ovo se poziva samo da bi se inkrementirao indeks za lejn i dobila Y pozicija
        counter = 0

        if randomPatternBO5:
            lilyPadPattern = random.choice([Config.lilypadPatternBO5Standard, Config.lilypadPatternBO5V2, Config.lilypadPatternBO5V3])

        for char in lilyPadPattern:
            if char == "0":
                Bush(counter * Config.gridSize, l.y, 50, 50)
            elif char == "1":
                Lilypad(counter * Config.gridSize, l.y, funkcijaZaLilypad)
            counter += 1

        if counter < Config.mapSize - 1:
            print("Sablon za final lejn nije dobar")

        return l

if __name__ == '__main__':
    pass