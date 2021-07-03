import pygame

class Player:
    def __init__(self, coordinates, size, speed, fileLocation):
        self.coordinates = coordinates
        self.size = size
        self.speed = speed
        self.fileLocation = fileLocation
        self.surface_original = pygame.transform.scale(pygame.image.load(fileLocation), (size[0], size[1]))
        self.surface_flipped = pygame.transform.flip(pygame.transform.scale(pygame.image.load(fileLocation), (size[0], size[1])), True, False)
        self.surface = self.surface_original
