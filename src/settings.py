# 5/1/2020
# Elliott Gorman
# ITSW 1359
# VINES - SETTINGS CLASS

import pygame

class Settings():

    def __init__(self):
        self.screen_width = 700
        self.screen_height = 900

        #background image
        self.bg_image = pygame.image.load("Sprites/background.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
        self.bg_rect = [0, 0]

        #Create second identical background for scrolling effect
        self.bg_imageTwo = self.bg_image
        self.bg_rectTwo = [0, -self.bg_image.get_height()]

        #playerSpeed
        self.playerSpeed = 4.0

        #bulletSpeed
        self.bulletSpeed = 15

        #enemy speed settings
        #index 0 is basic enemy, index 1 is higher level, so on
        self.enemySpeeds = [3, 5, 7, 9]
