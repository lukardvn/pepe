from Config import Config


class GameObject:
    allGameObjects = []

    def __init__(self):
        self.allGameObjects.append(self)

    def update(self):
        pass