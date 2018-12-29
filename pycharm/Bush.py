from Rectangle import Rectangle
from Config import Config

class Bush(Rectangle):
    def __init__(self, x, y, widthPX, heightPX):
        super().__init__(x,y, widthPX, heightPX, 'bush.png', Config.layerZabe)
        self.Show()