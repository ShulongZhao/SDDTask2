import pygame
from Animations import animations

class Character (pygame.sprite.Sprite):
    def __init__(self, _image, size, speed, attackFileLocation):
        pygame.sprite.Sprite.__init__(self)
        # self.sprites = [pygame.image.load(sprite) for sprite in spriteList]
        self.imageLeft = pygame.transform.flip(pygame.transform.scale(pygame.image.load(_image), size), True, False)
        self.imageRight = pygame.transform.scale(pygame.image.load(_image), size)
        self.image = self.imageRight


        self.rect = self.image.get_rect()
        self.rect.size = size

        self.speed = speed

        self.attackFileLocation = pygame.image.load(attackFileLocation)
    
        

