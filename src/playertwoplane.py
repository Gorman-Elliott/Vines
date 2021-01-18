# 5/1/2020
# Elliott Gorman
# ITSW 1359
# VINES - PLAYER TWO PLANE CLASS

from plane import Plane
import pygame

class playerTwoPlane(Plane):

    def __init__(self, vines_game):
        super().__init__(vines_game)

        self.animation = [pygame.image.load('Sprites/playerTwo_1.png'), pygame.image.load('Sprites/playerTwo_2.png')]

    def drawHealth(self):
        self.screen.blit(self.healthBar[self.health], (self.settings.screen_width - 210, self.settings.screen_height - 50)) #45 is the size of the images + 5 padding
