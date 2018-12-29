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
        layer = Config.layerDefault

        #print(self.yLane)
        if numOfObs == 0:
            type = "safe"
            #print(type)
        #print(str(self.yLane))
        if(type=="voda"):
            self.sprite=Config.water
            layer = Config.layerWaterLane
        elif(type=="safe"):
            self.sprite=Config.safeLane
        elif(type=="roadTop"):
            self.sprite=Config.trafficTop
        elif(type=="roadBottom"):
            self.sprite=Config.trafficBottom
        else:
            self.sprite=Config.traffic



        super().__init__(0, Config.yLane,Config.gridSize*Config.mapSize,  Config.gridSize,self.sprite, layer=layer)

        self.n=numOfObs
        self.spd=speed
        self.spc=spacing
        self.obstacles=[]
        self.offset = 220
        self.Show()
        self.presaoGranicu = False

        #ispravljeno da se stabla ne preklapaju, radi tako sto proverava da li se preklapa sa nekim drugim stablom
        #i ako se preklapa prepravlja se x koordinata (linija 56), randint se koristi da se onda izmedu stabla
        #jos doda razmak, od 70 do 90 da zaba ne moze preci sa stabla na stablo, to mozda i ne treba pa se moze smanjiti
        #Ako je prepravljena x koordinata veca od ivice prozora, znaci pocinje van ekrana, jednostavno
        #je visak, i nju onda ne prikazujemo, nema mesta gde da se ubaci, zbog toga postoji if u liniji 67.
        #to se desi npr kad se generisu 3 stabla i sva tri su w=310.

        for i in range(numOfObs):
            if type == "voda":
                self.offset = 150
                self.presaoGranicu = False
                o = Obstacle(i * self.spc + self.offset, Config.yLane, self.spd, isLogLane=True)
                #print('generisani', o.x, o.w, o.x + o.w)
                for obs in self.obstacles:
                    if obs.x + obs.w >= o.x:
                        #print('kolizija sa', obs.x, obs.w, obs.x + obs.w)
                        o.x += obs.x + obs.w - o.x + random.randint(70, 90)
                        if o.x > Config.gridSize * Config.mapSize:
                            #print('preko granice')
                            self.presaoGranicu = True
                        else:
                            self.presaoGranicu = False

                        #print('ispravljeni', o.x, o.w, o.x + o.w)
                if self.presaoGranicu == False:
                    o.Show()
                    self.obstacles.append(o)
            else:
                o = Obstacle(i * self.spc + self.offset, Config.yLane, self.spd)
                o.Show()
                self.obstacles.append(o)







