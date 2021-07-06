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
