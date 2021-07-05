import pygame

class Bullet:
    def __init__(self, coordinates, size, velocity, fileLocation):
        # converting from tuple to list for access into each element
        self.coordinates = list(coordinates)

        self.size = size
        self.height = self.size[0]
        self.width = self.size[1]

        self.velocity = velocity

        self.surface_original = pygame.transform.scale(pygame.image.load(fileLocation), self.size)
        self.surface_flipped = pygame.transform.flip(pygame.transform.scale(pygame.image.load(fileLocation), self.size), False, True)
        self.surface = self.surface_original        

