from Rectangle import Rectangle

class Lane(Rectangle):
    obstacles =[]
    def __init__(self,n,spd,spc,x,y,w,h,sprite,isSafeLane=False):
        if(isSafeLane==False):
            self.sprite = 'beton.png'

        super().__init__(x,y,w,h,sprite)
        self.n=n
        self.spd=spd
        self.spc=spc
        self.isSafeLane=isSafeLane
        obstacle = Obstacle()
        obstacles.append(obstacle)




