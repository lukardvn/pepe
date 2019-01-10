import time
import random
import multiprocessing as mp
from multiprocessing import Queue

class Zeus:

    def __init__(self, kju, secondsSunnyMin, secondsSunnyMax, secondsRainMin, secondsRainMax):
        self.minSunny = secondsSunnyMin
        self.maxSunny = secondsSunnyMax
        self.minRain = secondsRainMin
        self.maxRain = secondsRainMax
        self.kju = kju
        self.vreme = "s"    #kakvo je trenutno vreme; n=>NISTA (nema ni snega ni kise), s=>sneg, k=>kisa


    def MakeItRain(self):
        while True:
            self.ChangeWheather()
            if self.vreme == "n":
                time.sleep(random.random() * self.maxSunny + self.minSunny)
            elif self.vreme == 's' or self.vreme == 'k':
                time.sleep(random.random() * self.maxRain + self.minRain)

    def ChangeWheather(self):
        self.vreme = random.choice(['s', 'n', 'k', 'n', 'n', 'n']) #da budu vece sanse da je suncano nego kisa/sneg
        self.kju.put(self.vreme)


def _zevseOvoRadi(kju):
    zevs = Zeus(kju, 3, 7, 1, 3)
    zevs.MakeItRain()

def PokreniZevsa(kju):
    proc = mp.Process(target=_zevseOvoRadi, args=(kju,))
    proc.start()
    return proc

def Main():
    q = Queue()
    PokreniZevsa(q)

    while True:
        print(q.get())


if __name__ == "__main__":
    Main()