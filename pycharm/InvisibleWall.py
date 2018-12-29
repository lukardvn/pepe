from Rectangle import Rectangle
from Config import Config

class InvisibleWall(Rectangle):
    def __init__(self, x, y, widthPX, heightPX):
        super().__init__(x,y, widthPX, heightPX, '', Config.layerZabe)
        self.Show()