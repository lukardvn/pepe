class Config:
    gridSize = 50   #velicina (u pikselima) 'mreze' po kojoj se krecu igraci
    mapSize = 15    #velicina mape => 'mreza' 15x15 (750px X 750px)
    FPS = 30
                            #X, Y
    player1StartPosition = (10,14)
    player2StartPosition = (3,14)

    newLaneYIndex = 0 #globalni brojac gde treba da se nalazi novi lane u gridu

    mainWindow = None  # ovo se postavlja iz MAIN.py

    #sprajtovi
    spriteLocation = "sprites/"
    laneSpriteSafety="grass.png"
    laneSpriteWater = "water.png"
    laneSpriteTraffic = "road.png"
    laneSpriteTrafficTop = "roadTop.png"
    laneSpriteTrafficBottom = "roadBottom.png"

    #collision lejeri (grupisanje rectangli)
    layerDefault = 'default'
    layerZabe = 'zabe'
    layerPrepreke = 'obstacles'
    layerKola = 'kola'
    layerDrva = 'drva'
    layerWaterLane = 'waterLane'

    laneTypeWater = 'voda'
    laneTypeTraffic = 'kola'
    laneTypeTrafficTop = 'kolaGornjaTraka'
    laneTypeTrafficBottom = 'kolaDonjaTraka'
    laneTypeSafety = 'safety'

    laneTypeToLaneSprite = {
        laneTypeWater: laneSpriteWater,
        laneTypeTraffic: laneSpriteTraffic,
        laneTypeTrafficTop: laneSpriteTrafficTop,
        laneTypeTrafficBottom: laneSpriteTrafficBottom,
        laneTypeSafety: laneSpriteSafety
    }

    #sprajtovi grupisani po tipu lejna gde ce se pojaviti
    #kljuc je naziv sprajta, vrednost je sirina sprajta u pikselima
    availableCars = {
        "car_1": 100,
        "car_2": 100,
        "car_3": 100,
        "truck_1": 200,
        "truck_2": 135
    }

    availableTrucks = {
        "truck_1": 200,
        "truck_2": 135
    }

    availableLogs = {
        "log_small": 120,
        "log_medium": 158,
        "log_large": 310
    }
