from Config import Config
from Rectangle import Rectangle

class Lilypad(Rectangle):
    def __init__(self, x,  y, funkcijaZaLilypad):
        super().__init__(x, y, 50, 50, 'lilypadV2.png', Config.layerLilypad)
        self.Show()
        self.lastPlayerOnLilypad = None
        self.funkcijaZaLilypad = funkcijaZaLilypad
        self.brojac = 0

    def usedByPlayer(self, player,isTwoPlayer):
        self.lastPlayerOnLilypad = player
        if self.lastPlayerOnLilypad == None and self.loadedSprite != 'lilypadV2.png':
            self.ChangeSprite('lilypadV2.png')
        elif self.lastPlayerOnLilypad.isPlayerTwo:
            self.ChangeSprite('lilypadV2_player2.png')
            player.ReturnToStart()
        else:
            self.ChangeSprite('lilypadV2_player1.png')
            player.ReturnToStart()

        for rect in Rectangle.allRectangles[Config.layerLilypad]:
            if rect.lastPlayerOnLilypad != None:
                self.brojac += 1

        #print(Config.twoPl,isTwoPlayer)
        if isTwoPlayer:
            if self.brojac == 3:
                self.funkcijaZaLilypad()
                self.brojac = 0
        else:
            if self.brojac == 5:
                self.funkcijaZaLilypad()
                self.brojac = 0