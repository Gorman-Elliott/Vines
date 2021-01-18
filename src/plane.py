# 5/1/2020
# Elliott Gorman
# ITSW 1359
# VINES - PLANE CLASS

import pygame
import math
from settings import Settings
from pygame.sprite import Sprite

class Plane(Sprite):

    def __init__(self, vines_game):
        super().__init__()

        #grab and create necessary objects
        self.screen = vines_game.screen
        self.screen_rect = vines_game.screen.get_rect()
        self.settings = Settings()

        #set plane health
        self.health = 5
        self.healthBar = [pygame.image.load('Sprites/Health_Sprites/Health_Sprites_0.png'),
                          pygame.image.load('Sprites/Health_Sprites/Health_Sprites_1.png'),
                          pygame.image.load('Sprites/Health_Sprites/Health_Sprites_2.png'),
                          pygame.image.load('Sprites/Health_Sprites/Health_Sprites_3.png'),
                          pygame.image.load('Sprites/Health_Sprites/Health_Sprites_4.png'),
                          pygame.image.load('Sprites/Health_Sprites/Health_Sprites_5.png')]

        #animation information about plane - This is the default animation
        self.animationSpot = 0
        self.animation = [pygame.image.load('Sprites/AirShip_testOne.png'), pygame.image.load('Sprites/AirShip_testTwo.png')]

        #get rect of base image
        self.image = self.animation[0]
        self.rect = self.image.get_rect()

        #Start plane at bottom middle of screen_rect
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y = self.rect.y - 100

        #movement properties
        #init to none
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    #blit for drawing plane
    def draw(self, frame):
        #Draw ship at current location: self.rect.midbottom
        self.screen.blit(frame, self.rect)

    def drawHealth(self):
        self.screen.blit(self.healthBar[self.health], (10, self.settings.screen_height - 50)) #45 is the size of the images + 5 padding

    def move(self, playerSpeed):
        #find movement direction
        if (self.movingLeft == True and math.ceil(self.rect.x) > 0):
            self.x -= (1.0*playerSpeed)
        if (self.movingRight == True and math.floor(self.rect.x) < self.settings.screen_width - self.image.get_width()):
            self.x += (1.0*playerSpeed)
        if (self.movingUp == True and math.floor(self.rect.y) > 0):
            self.y -= (1.0*playerSpeed)
        if (self.movingDown == True and math.ceil(self.rect.y) < self.settings.screen_height - self.image.get_height() - 55): # -55 adds padding for bottom hud
            self.y += (1.0*playerSpeed)

        self.rect.x = self.x
        self.rect.y = self.y
