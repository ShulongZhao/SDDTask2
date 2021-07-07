import pygame
from Animations import animations

class Player:
    def __init__(self, coordinates, size, speed, bulletImageFileLocation, _animDirectoryList):
        self.coordinates = coordinates
        self.size = size
        self.speed = speed
        self.surface = None
        self.bulletImage = pygame.image.load(bulletImageFileLocation)
        self.animations = animations(_animDirectoryList)

class Enemy:
    def __init__(self, coordinates, size, speed, bombImageFileLocation, _animDirectoryList):
        self.coordinates = coordinates
        self.size = size
        self.speed = speed
        self.surface = None
        self.bombImage = pygame.image.load(bombImageFileLocation)
        self.animations = animations(_animDirectoryList)