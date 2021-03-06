from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from Config import Config
from GameObject import GameObject

class Rectangle(GameObject):
    id = 1
    allRectangles = {}

    def __init__(self, x, y, w, h, sprite, layer=Config.layerDefault, forceId=-1):
        super().__init__()
        if forceId == -1: #ovo se koristi samo na klijentu kad se kreiraju objekti
            self.id = Rectangle.id #svaka rektangla dobija unikatan ID, ovo se jedino koristi za mulitplayer. Da mogu objekti da se sinhronizuju izmedju klijenta i servera
            Rectangle.id += 1
        else:
            self.id = forceId
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.layer = layer
        self.loadedSprite = sprite
        self.pixmap = QPixmap(Config.spriteLocation + sprite)
        self.label = QLabel(Config.mainWindow)
        self.isVisible = False

        self.AddToLayer(layer)

    def __init_ui__(self):
        pass

    def AddToLayer(self, layerName):
        if not self in self.allRectangles.items():
            if layerName in self.allRectangles.keys():
                self.allRectangles[layerName].append(self)
            else:
                self.allRectangles[layerName] = [self]

    def GetSides(self):
        left = self.x
        right = self.x + self.w
        top = self.y
        bottom = self.y + self.h

        return (top, right, bottom, left)

    def Show(self):
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(self.x, self.y, self.w, self.h)
        self.label.show()
        self.isVisible = True

    def Collision(self, other):
        top, right, bottom, left = self.GetSides()
        otop, oright, obottom, oleft = other.GetSides()

        return not (
            left >= oright or
            right <= oleft or
            top >= obottom or
            bottom <= otop
        )

    def CollisionLayerSpecific(self, checkForLayer, returnObject=False):
        if checkForLayer in self.allRectangles.keys():
            for obj in self.allRectangles[checkForLayer]:
                if self.Collision(obj):
                    if returnObject:
                        return obj
                    else:
                        return True
        if returnObject:
            return None
        else:
            return False

    def IsEmpty(self,x,y):
        x = self.x + Config.gridSize * x
        y = self.y + Config.gridSize * y
        left = x
        right = x + self.w
        top = y
        bottom = y + self.h

        for other in self.allRectangles[self.layer]:
            otop, oright, obottom, oleft = other.GetSides()
            if not (
                left >= oright or
                right <= oleft or
                top >= obottom or
                bottom <= otop
            ):
                return False
        return True

    def ChangeSprite(self, spriteName):
        #ovo se koristi da skloni zabu na klijentu. JAKO JE PRLJAVO RESENJE. BICE POSTAVLJENO IZ FUNKCIJE UpdateObjectsPosition u Main.py
        if spriteName == "DEAD":
            self.RemoveFromScreen()

        if spriteName != self.loadedSprite:
            self.loadedSprite = spriteName
            self.pixmap = QPixmap(Config.spriteLocation + spriteName)
            self.label.setPixmap(self.pixmap)

    def Distance(self, other):
        x2,y2 = other.GetPosition()
        return pow(pow(x2 - self.x,2) + pow(y2 - self.y, 2), 0.5)

    def SetPosition(self, x, y):
        self.x = x
        self.y = y
        self.label.setGeometry(self.x, self.y, self.w, self.h)

    def GetPosition(self):
        return (self.x, self.y)

    def SetSize(self, w, h):
        if w < 0:
            return
        if h < 0:
            return

        self.w = w
        self.h = h
        self.label.setGeometry(self.x, self.y, self.w, self.h)

    @staticmethod
    def ResetId():
        Rectangle.id = 1

    def GetSize(self):
        return (self.w, self.h)
        
    def RemoveFromScreen(self):
        self.label.setGeometry(0, 0, 0, 0)
        self.label.hide()
        self.SetSize(0, 0)
        self.label.setParent(None)

if __name__ == '__main__':
    pass
