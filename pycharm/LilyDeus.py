from Rectangle import Rectangle
from Config import Config
import random

class LilyDeus(Rectangle):
    def __init__(self, x, y, widthPX, heightPX):
        super().__init__(x, y, widthPX, heightPX, 'lilypad.png', Config.layerDefault)
        self.Show()