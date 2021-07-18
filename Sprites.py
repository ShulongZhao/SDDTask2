import pygame

class Character (pygame.sprite.Sprite):
    def __init__(self, size, velocity, animsDirList, bulletImage, flipSprite=False):
        # initialising sprite logic
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (1280 / 2, 720 / 2)
        self.size = size
        self.velocity = velocity

        self.animsDirList = animsDirList
        self.bulletImage = bulletImage

        self.flipSprite = flipSprite


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, size, velocity, startingPos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image), size).convert()
        self.rect = self.image.get_rect()
        self.rect.x = startingPos[0]
        self.rect.y = startingPos[1]
        self.size = size
        self.velocity = velocity
