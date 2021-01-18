# 5/1/2020rec
# Elliott Gorman
# ITSW 1359
# VINES - BASIC ENEMY CLASS

import pygame
import random
from bullet import EnemyBullet
from pygame.sprite import Sprite

class Enemy(Sprite):

    def __init__(self, vines_game, type = 0):

        super().__init__()
        self.screen = vines_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = vines_game.settings
        self.image = pygame.image.load('Sprites/basicEnemy_small.png')
        self.rect = self.image.get_rect()
        self.y = self.rect.y

        #enemyType is 0 by defualt, which is a basic enemey
        # higher level enemies will have different types
        self.enemyType = type
        self.health = self.enemyType + 1

        #Counter for how far to move down screen until moving back up
        self.y_max = 500
        self.y_min = -50      #set to -50 so when the planes go off screen they disappear. This is to give challenge to earning score
        self.flipDir = False

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if (self.y <= self.y_max and not self.flipDir):
            self.y += (1*self.settings.enemySpeeds[self.enemyType])
            if (self.y >= self.y_max):
                self.flipDir = not self.flipDir
                #flip image before moving upwards
                pygame.transform.rotate(self.image, 180)
        if (self.y >= self.y_min and self.flipDir):
            self.y -= (1*self.settings.enemySpeeds[self.enemyType])
            if (self.y <= self.y_min):
                self.flipDir = not self.flipDir

        self.rect.y = self.y

    #returns a random integer between the width of the screen - image width
    # I have not used this function in release.
    def randomX(self):
        location = random.randrange(20, self.settings.screen_width - self.image.get_width())
        return location

class ShootingEnemy(Enemy):
    def __init__(self, vines_game):
        super().__init__(vines_game, type = 1)

        #copy over vines_game object reference to use for shoot()
        self.vines_game = vines_game

        #override health
        self.health = 2

    def shoot(self):
        enemy_bullet = EnemyBullet(self.vines_game, self)
        self.vines_game.enemyBullets.add(enemy_bullet)



#This is a class to contain information about
# spawn sequences for the various levels
class SpawnSequence():

    def __init__(self, vines_game):
        #get screen information
        self.vines_game = vines_game
        self.screen = self.vines_game.screen
        self.screen_rect = self.screen.get_rect()

        #get ship widths
        basicShip = pygame.image.load('Sprites/basicEnemy_small.png')
        self.basicShipWidth = basicShip.get_width()

        #Calculate even placement using basicShipWidth
        self.location = self.screen.get_width() - self.basicShipWidth
        #Spawn locations
        self.middle = (self.location) / 2
        self.thirdLeft = (self.location) / 3
        self.thirdRight = (self.location) - ((self.location) / 3)
        self.fourthLeft = (self.location) / 4
        self.fourthRight = (self.location) - ((self.location) / 4)
        self.fifthLeft = (self.location) / 5
        self.fifthRight = (self.location) - ((self.location) / 5)
        self.sixthLeft = (self.location) / 6
        self.sixthRight = (self.location) - ((self.location) / 6)
        self.seventhLeft = (self.location) / 7
        self.seventhRight = (self.location) - ((self.location) / 7)
        self.eigthLeft = (self.location) / 8
        self.eigthRight = (self.location) - ((self.location) / 8)
        self.ninthLeft = (self.location) / 9
        self.ninthRight = (self.location) - ((self.location) / 9)
        self.tenthLeft = (self.location) / 10
        self.tenthRight = (self.location) - ((self.location) / 10)

        #Level One spawn sequence
        # 0 means can not shoot
        # 1 means can shoot
        self.levelOne = [
                         [0, self.middle],
                         [0, self.thirdLeft],
                         [0, self.fifthRight],
                         [[0, self.sixthRight], [1, self.sixthLeft]],
                         [[1, self.fifthLeft], [1, self.fifthRight]]
                        ]



    #This function is called by _createEnemy in Vines to instantiate the enemies
    def spawnEnemyOfType(self, type):
        if (type == 0):
            return Enemy(self.vines_game)
        elif(type == 1):
            return ShootingEnemy(self.vines_game)
