from Rectangle import Rectangle
from Config import Config
from Obstacle import  Obstacle
from enum import Enum
import  random

class Lane(Rectangle):
    #n je broj kola u traci,spd->brzina,spc->razmak izmedju njih,ostalo sve isto i type je tip povrsine
    def __init__(self,numOfObs,speed,spacing,index,type):

        Config.yLane = (Config.mapSize - index - 1) * Config.gridSize
        Config.indexHelper = index
        #print(self.yLane)
        if numOfObs == 0:
            type = "safe"
            #print(type)
        #print(str(self.yLane))
        if(type=="voda"):
            self.sprite=Config.water
        elif(type=="safe"):
            self.sprite=Config.safeLane
        elif(type=="roadTop"):
            self.sprite=Config.trafficTop
        elif(type=="roadBottom"):
            self.sprite=Config.trafficBottom
        else:
            self.sprite=Config.traffic

        super().__init__(0, Config.yLane,Config.gridSize*Config.mapSize,  Config.gridSize,self.sprite)

        self.n=numOfObs
        self.spd=speed
        self.spc=spacing
        self.obstacles=[]
        self.offset = 220
        self.Show()

        for i in range(numOfObs):
            if index == 6:
                o = Obstacle(i * self.spc + self.offset, Config.yLane, 120, Config.gridSize, self.spd)
                o.Show()
                self.obstacles.append(o)
            elif index == 7:
                o = Obstacle(i * self.spc + self.offset, Config.yLane, 158, Config.gridSize, self.spd)
                o.Show()
                self.obstacles.append(o)
            elif index == 8:
                o = Obstacle(i * self.spc + self.offset, Config.yLane, 158, Config.gridSize, self.spd)
                o.Show()
                self.obstacles.append(o)
            elif index == 9:
                o = Obstacle(i * self.spc + self.offset, Config.yLane, 310, Config.gridSize, self.spd)
                o.Show()
                self.obstacles.append(o)
            else:
                o = Obstacle(i * self.spc + self.offset, Config.yLane, 100, Config.gridSize, self.spd)
                o.Show()
                self.obstacles.append(o)







