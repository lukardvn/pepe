from Config import Config
from Rectangle import Rectangle

class Lilypad(Rectangle):
    def __init__(self, x,  y):
        super().__init__(x, y, 50, 50, 'lilypadV2.png', Config.layerLilypad)
        self.Show()
        self.lastPlayerOnLilypad = None

    def usedByPlayer(self, player):
        self.lastPlayerOnLilypad = player
        if self.lastPlayerOnLilypad == None and self.loadedSprite != 'lilypadV2.png':
            self.ChangeSprite('lilypadV2.png')
        elif self.lastPlayerOnLilypad.isPlayerTwo:
            self.ChangeSprite('lilypadV2_player2.png')
            player.ReturnToStart()
        else:
            self.ChangeSprite('lilypadV2_player1.png')
            player.ReturnToStart()