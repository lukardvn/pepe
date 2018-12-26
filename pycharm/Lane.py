from Rectangle import Rectangle
from Config import Config
from enum import Enum
import  random

class Lane(Rectangle):
    #n je broj kola u traci,spd->brzina,spc->razmak izmedju njih,ostalo sve isto i type je tip povrsine
    def __init__(self,n,spd,spc,x,y,w,h,sprite,type):

        super().__init__(0,y*Config.gridSize,w,Config.gridSize,sprite)
        if(type=="voda"):
            self.sprite=Config.water
        elif(type=="safe"):
            self.sprite=Config.safeLane
        else:
            self.sprite=Config.traffic

        self.n=n
        self.spd=spd
        self.spc=spc
        self.obstacles=[]
        #offset odstojanje izmedju lejnova
        #offset = random()
        offset = 100;
        for i in range(n):
            self.obstacles.append(Obstacle(offset+spc*i+1,y*Config.gridSize,w*Config.gridSize,Config.gridSize,spd,sprite))







