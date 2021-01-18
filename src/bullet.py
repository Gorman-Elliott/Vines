# 5/1/2020
# Elliott Gorman
# ITSW 1359
# VINES - PLAYER BULLETS CLASS

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, vines_game):

        super().__init__()
        self.screen = vines_game.screen
        self.settings = vines_game.settings

        #init bullet image and rect
        self.image = pygame.image.load('Sprites/bullets.png')
        self.rect = self.image.get_rect()

        #movement properties
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        self.y -= (1*self.settings.bulletSpeed)
        self.rect.y = self.y

    def draw(self):
        self.screen.blit(self.image, self.rect)

class playerBullet(Bullet):
    def __init__(self, vines_game, player):
        super().__init__(vines_game)

        #redefine location properties
        self.rect.midbottom = player.rect.midtop    #spawn bullet at location of player plane
        self.y = float(self.rect.y)                 #movement properties

class EnemyBullet(Bullet):
    def __init__(self, vines_game, enemy):
        super().__init__(vines_game)

        #redefine default bullet options for enemy bullet
        self.image = pygame.image.load("Sprites/enemyBullet.png")
        self.rect = self.image.get_rect()

        #grab information about players location
        # testing for playerOne first
        self.playerOne = vines_game.playerOne

        #update bullet speed for enemies
        self.bulletSpeed = 12

        #spawn bullet at enemy that is firing bullet
        #get enemy's location info
        self.rect.midbottom = enemy.rect.midbottom
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.enemy_y = enemy.rect.y
        self.enemy_x = enemy.rect.x

    #override update to follow player
    def update(self):
        #y difference between player and bullet
        self.y_difference = (self.playerOne.rect.y - self.enemy_y)
        self.x_difference = (self.playerOne.rect.x - self.enemy_x)
        self.x_steps = abs(self.x_difference / self.y_difference)

        self.y += (1*self.bulletSpeed)
        if (self.x_difference > 0):
            self.x += (self.x_steps*self.settings.bulletSpeed)
        elif (self.x_difference < 0):
            self.x -= (self.x_steps*self.settings.bulletSpeed)

        self.rect.y = self.y
        self.rect.x = self.x
