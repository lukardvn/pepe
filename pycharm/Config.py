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
        "car_4": 107,
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

    #tupla => broj prepreka, brzina, spejsing, tipLejna
    lanesEasyConfig = [
        (1, 5.6, 180, laneTypeTraffic),
        (8, 3.9, 210, laneTypeTraffic),
        (3, 4.5, 240, laneTypeTraffic),
        (12, 3.2, 170, laneTypeTraffic),
    ]

    #tupla => broj prepreka, brzina, spejsing, tipLejna
    lanesMediumConfig = [
        (3, 6, 200, laneTypeTraffic),
        (8, 4.7, 240, laneTypeTraffic),
        (6, 8, 280, laneTypeTraffic),
        (15, 5.2, 200, laneTypeTraffic),
        (20, 6.25, 220, laneTypeTraffic),
        (10, 9, 450, laneTypeTraffic),
        (6, 6.3, 240, laneTypeTraffic)
    ]

    #tupla => broj prepreka, brzina, spejsing, tipLejna
    lanesHardConfig = [
        (5, 8, 175, laneTypeTraffic),
        (1, 15, 175, laneTypeTraffic),
        (7, 9, 240, laneTypeTraffic),
        (13, 6, 185, laneTypeTraffic),
        (4, 11, 270, laneTypeTraffic),
        (3, 7.33, 110, laneTypeTraffic),
        (2, 13.2, 95, laneTypeTraffic)
    ]

    # tupla => broj prepreka, brzina, spejsing, tipLejna
    lanesEasyWaterConfig = [
        (4, 3.2, 150, laneTypeWater),
        (3, 4.7, 220, laneTypeWater),
        (2, 4, 250, laneTypeWater)
    ]

    # tupla => broj prepreka, brzina, spejsing, tipLejna
    lanesMediumWaterConfig = [
        (6, 5.3, 260, laneTypeWater),
        (4, 6.3, 280, laneTypeWater),
        (3, 7, 230, laneTypeWater)
    ]

    # tupla => broj prepreka, brzina, spejsing, tipLejna
    lanesHardWaterConfig = [
        (3, 7.32, 315, laneTypeWater),
        (4, 8.23, 320, laneTypeWater),
        (5, 9.15, 260, laneTypeWater)
    ]
