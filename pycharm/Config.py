class Config:
    mainWindow = None #ovo se postavlja iz MAIN.py
    gridSize = 50   #velicina (u pikselima) 'mreze' po kojoj se krecu igraci
    mapSize = 15    #velicina mape => 'mreza' 15x15 (750px X 750px)
    spriteLocation = "sprites/"
    safeLane="grass.png"
    water = "water.png"
    traffic = "road.png"
    trafficTop = "roadTop.png"
    trafficBottom = "roadBottom.png"
    yLane = 0
    indexHelper = 0
    obstacleHelper1 = 0
    obstacleHelper2 = 0
    obstacleHelper3 = 0
    obstacleHelper = 0
    FPS = 30

    layerZabe = 'zabe'
    layerPrepreke = 'obstacles'
    layerKola = 'kola'
    layerDrva = 'drva'

    availableCars = {
        "car_1": 100,
        "car_2": 100,
        "car_3": 100
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

                            #X, Y
    player1StartPosition = (10,14)
    player2StartPosition = (3,14)
