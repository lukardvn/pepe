from Config import Config
from Rectangle import Rectangle

class Lilypad(Rectangle):
    def __init__(self, x,  y, lvlPassed):
        super().__init__(x, y, 50, 50, 'lilypadV2.png', Config.layerLilypad)
        self.Show()
        self.lastPlayerOnLilypad = None
        self.levelPassed = lvlPassed
        self.brojac = 0

    def usedByPlayer(self, player, isTwoPlayer):
        self.lastPlayerOnLilypad = player

        if self.lastPlayerOnLilypad == None and self.loadedSprite != 'lilypadV2.png':
            self.ChangeSprite('lilypadV2.png')
        elif self.lastPlayerOnLilypad.isPlayerTwo:
            self.ChangeSprite('lilypadV2_player2.png')
            player.ReturnToStart()
            player.UpdateScore()
        else:
            self.ChangeSprite('lilypadV2_player1.png')
            player.ReturnToStart()
            player.UpdateScore()


        for lilypad in Rectangle.allRectangles[Config.layerLilypad]:
            if lilypad.lastPlayerOnLilypad != None:
                self.brojac += 1

        if self.brojac == Config.collectLilypadsToAdvanceLevel:
            self.levelPassed()
            self.brojac = 0
        #else:
        #    if self.brojac == 3:
        #        self.levelPassed()
        #        self.brojac = 0

if __name__ == '__main__':
    pass