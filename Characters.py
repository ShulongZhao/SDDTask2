import pygame
from Animations import animations

class Player:
    def __init__(self, coordinates, size, speed, _animDirectoryList):
        self.coordinates = coordinates
        self.size = size
        self.speed = speed
        self.surface = None
        self.animations = animations(_animDirectoryList)
