# 5/1/2020
# Elliott Gorman
# ITSW 1359
# VINES - gameStats CLASS

class gameStats():

    def __init__(self):

        #set scoring information
        self.highScore = 0

        #set current gamestate information
        self.gameActive = False
        self.currentLevel = 1

        #second player active state
        self.secondPlayerIsActive = False

        #currentPlayers - 1 being default
        self.currentPlayers = 1
