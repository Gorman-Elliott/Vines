# 5/1/2020
# Elliott Gorman
# ITSW 1359
# VINES - HEADS UP DISPLAY CLASS
# This class also contains methods for manipulating the start screen

import pygame.font
from gamestats import gameStats

class Hud():

    def __init__(self, vines_game):
        #init retro font
        pygame.font.init()
        self.font = pygame.font.Font("Resources/PressStart2P-Regular.ttf", 20)
        self.settings = vines_game.settings
        self.screen = vines_game.screen
        self.gameStats = vines_game.gameStats

        #scores and players
        self.currentScore = 0
        self.playerTwoScore = 0
        self.highScore = self.gameStats.highScore
        self.currentPlayers = self.gameStats.currentPlayers
        self.playerOne = vines_game.playerOne
        self.playerTwo = vines_game.playerTwo

        #strings
        self.pressSpace = "PRESS SPACE TO START"
        self.playerOneText = "PLAYER ONE"
        self.playerTwoText=  "PLAYER TWO"
        self.highscoreText = "HI-SCORE"
        self.pressEnter = "PRESS ENTER"
        self.numPlayersText = "{} PLAYER".format(self.currentPlayers)

        #set color to white
        self.hudColor = (255, 255, 255)

        #init start info - "Press Space" to start game
        self.startInfo = self.font.render(self.pressSpace, False, self.hudColor)
        self.startInfo_x, self.startInfo_y = self.font.size(self.pressSpace)

        #init and render static texts: "PLAYERSCORE" - player one, "HIGHSCORE"
        self.playerOneTextRender = self.font.render(self.playerOneText, False, self.hudColor)
        self.highscoreTextRender = self.font.render(self.highscoreText, False, self.hudColor)
        self.highscoreTextRender_x, self.highscoreTextRender_y = self.font.size(self.highscoreText)

        #init and render static texts for "PLAYER TWO" score
        self.playerTwoTextRender = self.font.render(self.playerTwoText, False, self.hudColor)
        self.playerTwoTextRender_x, self.playerTwoTextRender_y = self.font.size(self.playerTwoText)

        #Initalize "PRESS ENTER for player two"
        self.pressEnterTextRender = self.font.render(self.pressEnter, False, self.hudColor)
        self.pressEnterTextRender_x, self.pressEnterTextRender_y = self.font.size(self.pressEnter)

        #init render for current number of players selected
        self.currentPlayers = self.font.render(self.numPlayersText, False, self.hudColor)
        self.currentPlayers_x, self.currentPlayers_y = self.font.size(self.numPlayersText)

        #init hud
        self.updateHud()


    #required for displaying how the hud is updating
    def updateHud(self):
        #info for current score for PLAYER ONE
        playerOne_score_str = "{:,}".format(self.currentScore)
        playerOne_score_str.ljust(7)
        self.playerOneScoreRender = self.font.render(playerOne_score_str, False, self.hudColor)

        #info for current score for PLAYER TWO if player two is playing
        if (self.gameStats.secondPlayerIsActive):
            self.playerTwo_score_str = "{:,}".format(self.playerTwoScore)
            self.playerTwo_score_str.rjust(7)
            self.playerTwoScoreRender = self.font.render(self.playerTwo_score_str, False, self.hudColor)
            #adjust location based on size so that as text grows it stays on screen

        self.highScore = self.gameStats.highScore #grab and update highScore from gameStats
        hiScore_str = "{:,}".format(self.highScore)
        self.hiScore = self.font.render(hiScore_str, False, self.hudColor)

        #update center position of highscore as score grows
        highScore_x_currentSize, highScore_y_currentSize = self.font.size(str(self.gameStats.highScore))
        self.highScore_x = (self.settings.screen_width - highScore_x_currentSize) / 2

        #update player text if secondPlayerIsActive swaps
        # this requires updating numPlayers text and re-rendering it
        # only run this code if game is not active
        if (not self.gameStats.gameActive):
            if (self.gameStats.secondPlayerIsActive == True):
                self.numPlayersText = "{} PLAYER".format(self.gameStats.currentPlayers + 1)
                self.currentPlayers = self.font.render(self.numPlayersText, False, self.hudColor)
            else:
                self.numPlayersText = "{} PLAYER".format(self.gameStats.currentPlayers)
                self.currentPlayers = self.font.render(self.numPlayersText, False, self.hudColor)

    def displayHud(self):
        #display current playthroughs player one score at top left of screen
        self.screen.blit(self.playerOneScoreRender, (35, 35))

        #display current playthroughs player two score at the top right of the screen
        # only if player two is playing and the game is running
        if (self.gameStats.secondPlayerIsActive and self.gameStats.gameActive):
            self.screen.blit(self.playerTwoTextRender, (self.settings.screen_width - self.playerTwoTextRender_x - 10, 5))
            self.screen.blit(self.playerTwoScoreRender, (self.settings.screen_width - 35 - self.font.size(self.playerTwo_score_str)[0], 35))
            print(self.playerTwo_score_str)

        #display current play throughs high score
        self.screen.blit(self.hiScore, (self.highScore_x, 35))

        #draw hud texts
        self.screen.blit(self.playerOneTextRender, (10, 5))
        self.screen.blit(self.highscoreTextRender, ((self.settings.screen_width - self.highscoreTextRender_x) / 2, 5))

        #draw num players only if game is not active
        if (not self.gameStats.gameActive):
            self.screen.blit(self.currentPlayers, ((self.settings.screen_width - self.currentPlayers_x) / 2, self.settings.screen_height - ((self.settings.screen_height - self.currentPlayers_y) / 4)))


    #this function displays the "Press Space" text at the start of game
    #separated due to its nature of only being shown when game is not active
    def drawTempHud(self):
        #blit "Press Space To Start"
        self.screen.blit(self.startInfo, ((self.settings.screen_width - self.startInfo_x) / 2, self.settings.screen_height - ((self.settings.screen_height - self.startInfo_y) / 3)))

        if (not self.gameStats.secondPlayerIsActive):
            #blit "Press Enter" -- for two player play -- only drawn when second player is not active
            self.screen.blit(self.pressEnterTextRender, (self.settings.screen_width - self.pressEnterTextRender_x - 10, 5))
        else:
            self.screen.blit(self.playerTwoTextRender, (self.settings.screen_width - self.playerTwoTextRender_x - 10, 5))

    def updateLevel(self):
        self.currentLevel = self.gameStats.currentLevel

    #This function is a helper function that when the user selects 2 player,
    # the ships are spaced apart and don't appear on top of eachother
    def repositionShips(self):
            if (self.gameStats.secondPlayerIsActive == True):
                self.playerOne.rect.x = self.playerOne.rect.x - 100
                self.playerTwo.rect.x = self.playerTwo.rect.x + 100
            else:
                self.playerOne.rect.x = self.playerOne.rect.x + 100
                self.playerTwo.rect.x = self.playerTwo.rect.x - 100
