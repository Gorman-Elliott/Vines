# 5/1/2020
# Elliott Gorman
# ITSW 1359
# VINES - SOUND CONTROLLER CLASS

import pygame
from gamestats import gameStats

class gameSounds():

    def __init__(self):

        #load start music
        self.startMusic = pygame.mixer.music.load("Sounds/DutyCycle.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

        self.music = ("Sounds/DutyCycle.mp3", "Sounds/BipolarBear.mp3")

        #load initial sounds into game and set volume
        self.playerGunSound = pygame.mixer.Sound(file = "Sounds/playerShotSoundEffect.ogg")
        self.playerGunSound.set_volume(0.02)

        self.musicPlayer()

    def playSound(self, sound):
        sound.play()

    def stopSound(self, sound):
        sound.stop()

    def musicPlayer(self):
        pygame.mixer.music.queue(self.music[0])
        pygame.mixer.music.queue(self.music[1])
