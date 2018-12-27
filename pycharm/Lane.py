from Rectangle import Rectangle
from Config import Config
from Obstacle import  Obstacle
from enum import Enum
import  random

class Lane(Rectangle):
    #n je broj kola u traci,spd->brzina,spc->razmak izmedju njih,ostalo sve isto i type je tip povrsine
    def __init__(self,numOfObs,speed,spacing,index,type):

        self.yLane =  (Config.mapSize - index - 1) * Config.gridSize

        print(str(self.yLane))
        if(type=="voda"):
            self.sprite=Config.water
        elif(type=="safe"):
            self.sprite=Config.safeLane
        else:
            self.sprite=Config.traffic

        super().__init__(0, self.yLane, Config.gridSize * Config.mapSize, Config.gridSize, self.sprite)

        self.n=numOfObs
        self.spd=speed
        self.spc=spacing
        self.obstacles=[]
        self.offset = 100
        if(numOfObs>0):
            for i in range(numOfObs):
                o = Obstacle(i*self.offset+self.spc,self.yLane,50,Config.gridSize,self.spd)
                o.Show()
                self.obstacles.append(o)
        else:
            #










