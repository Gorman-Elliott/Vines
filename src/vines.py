# 5/1/2020
# Elliott Gorman
# ITSW 1359
# VINES

import pygame
import time
from playeroneplane import playerOnePlane
from playertwoplane import playerTwoPlane
from settings import Settings
from stack import Stack
from bullet import playerBullet
from bullet import EnemyBullet
from enemy import Enemy
from enemy import ShootingEnemy
from enemy import SpawnSequence
from gamestats import gameStats
from sounds import gameSounds
from hud import Hud

#throttle function
def throttle(s):
    def decorater(f):
        t = None
        def wrapped(*args, **kwargs):
            nonlocal t
            t_ = time.time()
            if t is None or t_ - t >= s:
                result = f(*args, **kwargs)
                t = time.time()
                return result
        return wrapped
    return decorater

class Vines():

    def __init__(self):
        # Init objects and constants
        pygame.init()
        pygame.display.set_caption("VINES")
        self.settings = Settings()
        self.gameStats = gameStats()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.playerOne = playerOnePlane(self)
        self.playerOneBullets = pygame.sprite.Group()
        self.playerTwo = playerTwoPlane(self)
        self.playerTwoBullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()
        self.playerOneShootingStack = Stack()
        self.playerTwoShootingStack = Stack()
        self.gameSounds = gameSounds()
        self.hud = Hud(self)

        # Create clock for framerate and get time info
        self.clock = pygame.time.Clock()

        # controller for enemy spawn sequence
        #  as enemies spawn, update their starting positions from List
        #  containing spawn sequence of enemies
        self.spawnSequence = SpawnSequence(self)
        self.currentSpotInSequence = 0

        # create event for enemy creation
        self.ENEMY_SPAWN_EVENT = 24
        pygame.time.set_timer(self.ENEMY_SPAWN_EVENT, 1000)

        # create event for enemy shooting
        self.ENEMY_SHOOTING_TIMER = 25
        pygame.time.set_timer(self.ENEMY_SHOOTING_TIMER, 2500)

        #event for player animation
        self.PLAYER_ANIMATION_TIMER = 26
        pygame.time.set_timer(self.PLAYER_ANIMATION_TIMER, 26)



    def run_game(self):
        while True:
            #set game to target 60 frames per second
            self.clock.tick_busy_loop(100)

            #check events
            self._checkEvents()

            #draw background - must happen before drawing anything else
            self._scrollBackground()

            if (self.gameStats.gameActive):
                #Fire bullets
                # This code is only called if the correspongind key to the stack is being held down
                if (self.playerOneShootingStack.peek()):
                    #start gun sound playback
                    self.gameSounds.playSound(self.gameSounds.playerGunSound)
                    self._firePlayerOneBullet(self.playerOne, self.playerOneBullets)
                if (self.playerTwoShootingStack.peek()):
                    #start gun sound playback
                    self.gameSounds.playSound(self.gameSounds.playerGunSound)
                    self._firePlayerTwoBullet(self.playerTwo, self.playerTwoBullets)

                #update player one based on user input
                self.playerOne.move(self.settings.playerSpeed)
                #update bullets for player 1 and player 2 if active
                self._updateBullets(self.playerOneBullets)
                if (self.gameStats.secondPlayerIsActive):
                    self._updateBullets(self.playerTwoBullets)
                    self.playerTwo.move(self.settings.playerSpeed)

                self._updateEnemies()      #update enemies
                self._updateEnemyBullets() #update enemy bullets

                #check to see if any players collided with any enemies
                # Also check to see if the bullets hit the player
                self._checkPlaneCollisions(self.playerOne, self.enemies)
                self._checkPlaneCollisions(self.playerOne, self.enemyBullets)
                if (self.gameStats.secondPlayerIsActive):
                    self._checkPlaneCollisions(self.playerTwo, self.enemies)
                    self._checkPlaneCollisions(self.playerTwo, self.enemyBullets)

            #draw all updates
            self._updateScreen()

    def _scrollBackground(self):
        #move top image first, then bottom image
        # to avoid tearing
        self.settings.bg_rectTwo[1] += 1
        self.settings.bg_rect[1] += 1
        self.screen.blit(self.settings.bg_image, self.settings.bg_rect)
        self.screen.blit(self.settings.bg_image, self.settings.bg_rectTwo)

        #check to see if we need to flip background
        if (self.settings.bg_rect[1] > self.settings.screen_height):
            self.settings.bg_rect[1] = -self.settings.screen_height
        if (self.settings.bg_rectTwo[1] > self.settings.screen_height):
            self.settings.bg_rectTwo[1] = -self.settings.screen_height

    def _checkPlayerBulletCollisions(self, groupOne, groupTwo):
        collisions = pygame.sprite.groupcollide(groupOne, groupTwo, False, True)

        for collision in collisions:
            #get type of enemy
            if (type(collision) is Enemy):
                collision.health -= 1
            if (type(collision) is ShootingEnemy):
                collision.health -= 1
            if (collision.health == 0):
                self.enemies.remove(collision)

                #if enemy is killed, add score
                if (self.playerOneBullets is groupTwo):
                    if (type(collision) is Enemy):
                        self.hud.currentScore += 50
                    elif (type(collision) is ShootingEnemy):
                        self.hud.currentScore += 100
                elif(self.playerTwoBullets is groupTwo):
                    if (type(collision) is Enemy):
                        self.hud.playerTwoScore += 50
                    elif (type(collision) is ShootingEnemy):
                        self.hud.playerTwoScore += 100

            #check if score is higher than highscore, if so, update hi-score
            if (self.hud.currentScore > self.gameStats.highScore):
                self.gameStats.highScore = self.hud.currentScore
            elif (self.hud.playerTwoScore > self.gameStats.highScore):
                self.gameStats.highScore = self.hud.playerTwoScore

    def _checkPlaneCollisions(self, player, group):
        collision = pygame.sprite.spritecollideany(player, group)

        #remove health from plane that was hit
        if isinstance(collision, Enemy):
            self.enemies.remove(collision)
            player.health -= 1
        elif isinstance(collision, EnemyBullet):
            self.enemyBullets.remove(collision)
            player.health -= 1

        #check to see if player health is less than 0
        if (player.health <= 0):
            self._resetScreen()

    def _resetScreen(self):
        self.enemies.empty()
        self.enemyBullets.empty()
        self.playerOneBullets.empty()

        #delete player and create a new object with the same name
        del self.playerOne
        self.playerOne = playerOnePlane(self)

        #Update player two status if in play
        if (self.gameStats.secondPlayerIsActive):
            self.playerTwoBullets.empty()
            del self.playerTwo
            self.playerTwo = playerTwoPlane(self)

        self.gameStats.gameActive = False

    def _checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            #KEYDOWN EVENTS
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_d):
                    self.playerOne.movingRight = True
                if (event.key == pygame.K_a):
                    self.playerOne.movingLeft = True
                if (event.key == pygame.K_w):
                    self.playerOne.movingUp = True
                if (event.key == pygame.K_s):
                    self.playerOne.movingDown = True
                if (event.key == pygame.K_SPACE):
                    self.playerOneShootingStack.push(True)
                    #if game is not active, and player presses space, start game
                    if (not self.gameStats.gameActive):
                        self.gameStats.gameActive = True

                #check player two events only if game is inactive
                if (not self.gameStats.gameActive):
                    if (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                        self.gameStats.secondPlayerIsActive = not self.gameStats.secondPlayerIsActive
                        self.hud.repositionShips()


                #event keys for player two
                if (self.gameStats.secondPlayerIsActive):
                    if (event.key == pygame.K_RIGHT):
                        self.playerTwo.movingRight = True
                    if (event.key == pygame.K_LEFT):
                        self.playerTwo.movingLeft = True
                    if (event.key == pygame.K_UP):
                        self.playerTwo.movingUp = True
                    if (event.key == pygame.K_DOWN):
                        self.playerTwo.movingDown = True
                    if (event.key == pygame.K_KP_ENTER):
                        self.playerTwoShootingStack.push(True)

            #KEYUP EVENTS
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_d):
                    self.playerOne.movingRight = False
                if (event.key == pygame.K_a):
                    self.playerOne.movingLeft = False
                if (event.key == pygame.K_w):
                    self.playerOne.movingUp = False
                if (event.key == pygame.K_s):
                    self.playerOne.movingDown = False
                if (event.key == pygame.K_SPACE):
                    self.playerOneShootingStack.pop()
                    #also stop playerGunSound if player is not pressing space
                    self.gameSounds.stopSound(self.gameSounds.playerGunSound)

                #check player two keyup events if active
                if (self.gameStats.secondPlayerIsActive):
                    if (event.key == pygame.K_LEFT):
                        self.playerTwo.movingLeft = False
                    if (event.key == pygame.K_RIGHT):
                        self.playerTwo.movingRight = False
                    if (event.key == pygame.K_UP):
                        self.playerTwo.movingUp = False
                    if (event.key == pygame.K_DOWN):
                        self.playerTwo.movingDown = False
                    if (event.key == pygame.K_KP_ENTER):
                        self.playerTwoShootingStack.pop()
                        #also stop playerGunSound if player is not pressing space
                        self.gameSounds.stopSound(self.gameSounds.playerGunSound)

            #DEV MADE EVENTS
            elif event.type == self.ENEMY_SPAWN_EVENT:
                self._createEnemy()
            elif event.type == self.PLAYER_ANIMATION_TIMER:
                if (self.playerOne.animationSpot == len(self.playerOne.animation) - 1):
                    self.playerOne.animationSpot = 0
                    self.playerTwo.animationSpot = 0
                else:
                    self.playerOne.animationSpot += 1
                    self.playerTwo.animationSpot += 1
            elif event.type == self.ENEMY_SHOOTING_TIMER:
                for enemy in self.enemies.copy():
                    if isinstance(enemy, ShootingEnemy):
                        enemy.shoot()

    def _updateScreen(self):
        #draw bullets first so as to not have them appear "above"
        # other sprites
        for bullet in self.playerOneBullets.sprites():
            bullet.draw()
        for bullet in self.playerTwoBullets.sprites():
            bullet.draw()

        #draw playerOne plane
        self.playerOne.draw(self.playerOne.animation[self.playerOne.animationSpot])

        #draw player two plane if active
        if (self.gameStats.secondPlayerIsActive):
            self.playerTwo.draw(self.playerTwo.animation[self.playerTwo.animationSpot])

        #redraw planes health after checking collisions
        self.playerOne.drawHealth()
        if (self.gameStats.secondPlayerIsActive):
            self.playerTwo.drawHealth()

        #if game is not active, show logo and info on how to start
        if (not self.gameStats.gameActive):
            self._showLogo()
            self.hud.drawTempHud()

        #draw the hud on top of everything
        self.hud.updateHud()
        self.hud.displayHud()

        #Make most recently drawn screen visible
        pygame.display.flip()

    #0.0875 is half of the audio file length for gun fire
    @throttle(0.0875)
    def _firePlayerOneBullet(self, player, playerBulletGroup):
        #Fires bullets only if space is being held down
        new_bullet = playerBullet(self, player) #pass self for screen and settings, player to know which players bullet
        playerBulletGroup.add(new_bullet)

    @throttle(0.0875)
    def _firePlayerTwoBullet(self, player, playerBulletGroup):
        #Fires bullets only if space is being held down
        new_bullet = playerBullet(self, player) #pass self for screen and settings, player to know which players bullet
        playerBulletGroup.add(new_bullet)

    def _updateBullets(self, playerBulletGroup):
        playerBulletGroup.update()

        for bullet in playerBulletGroup.copy():
            if bullet.rect.bottom <= 0:
                playerBulletGroup.remove(bullet)

        self._checkPlayerBulletCollisions(self.enemies, playerBulletGroup)


    def _updateEnemies(self):
        self.enemies.update()

        #remove enemies that are out of bounds
        for enemy in self.enemies.copy():
            if (enemy.rect.bottom > self.settings.screen_height or enemy.rect.bottom < 0):
                self.enemies.remove(enemy)

        #draw enemies
        for enemies in self.enemies.sprites():
            enemies.draw()


    def _updateEnemyBullets(self):
        self.enemyBullets.update()

        #remove bullets from group if there are off screen
        for bullet in self.enemyBullets.copy():
            if (bullet.rect.bottom > self.settings.screen_height):
                self.enemyBullets.remove(bullet)

        #draw enemy bullets
        for bullets in self.enemyBullets.sprites():
            bullets.draw()

    def _createEnemy(self):
        #Temp code to repeat spawn set
        if (self.currentSpotInSequence == len(self.spawnSequence.levelOne)):
            self.currentSpotInSequence = 0

        #get number of enemies in current iteration of spawn set
        currentSequence = self.spawnSequence.levelOne[self.currentSpotInSequence]

        #if the first thing in the list is a number, then that spot in the sequence is only
        # spawning one enemy, therefore, do not loop. otherwise, there is more than one enemy
        # to spawn, so loop
        if isinstance(currentSequence[0], int):
            #get information on type of enemy and spawn location
            enemyType, enemy_x = currentSequence
            enemy = self.spawnSequence.spawnEnemyOfType(enemyType)
            enemy.rect.x = enemy_x

            #if spawnsequence declares enemy to be of type shooting, then create EnemyBullet object
            if isinstance(enemy, ShootingEnemy):
                enemy_bullet = EnemyBullet(self, enemy)
                self.enemyBullets.add(enemy_bullet)

            self.enemies.add(enemy)
            self.currentSpotInSequence += 1
        else:
            for i in range(len(currentSequence)):
                #get information on type of enemy and spawn location
                enemyType, enemy_x = currentSequence[i]
                enemy = self.spawnSequence.spawnEnemyOfType(enemyType)
                enemy.rect.x = enemy_x

                #if spawnsequence declares enemy to be of type shooting, then create EnemyBullet object
                if isinstance(enemy, ShootingEnemy):
                    enemy_bullet = EnemyBullet(self, enemy)
                    self.enemyBullets.add(enemy_bullet)

                self.enemies.add(enemy)
            self.currentSpotInSequence += 1

    def _showLogo(self):
        if (not self.gameStats.gameActive):
            logo = pygame.image.load("Sprites/logo.png")
            logo_rect = logo.get_rect()
            screenCenter = self.screen.get_rect().center
            logo_rect.center = screenCenter
            self.screen.blit(logo, logo_rect)


if __name__ == "__main__":
    vines = Vines()
    vines.run_game()
