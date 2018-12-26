from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from Config import Config

class Rectangle:
    def __init__(self, x, y, w, h, sprite):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.loadedSprite = sprite
        self.pixmap = QPixmap(Config.spriteLocation + sprite)
        self.label = QLabel(Config.mainWindow)

    def __init_ui__(self):
        pass

    def GetSides(self):
        left = self.x
        right = self.x + self.w
        top = self.y
        bottom = self.y + self.h

        return (top, right, bottom, left)

    def Show(self):
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(self.x, self.y, self.h, self.w)

    def Collision(self, other):
        top, right, bottom, left = self.GetSides()
        otop, oright, obottom, oleft = other.GetSides()

        return not (
            left >= oright or
            right <= oleft or
            top >= obottom or
            bottom <= otop
        )

    def ChangeSprite(self, spriteName):
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