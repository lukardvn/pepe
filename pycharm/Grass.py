from Rectangle import Rectangle
from Config import Config

class Grass(Rectangle):
    def __init__(self, x, y, widthPX, heightPX):
        super().__init__(x,y, widthPX, heightPX, '')
        self.Show()