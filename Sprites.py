import pygame

class Character (pygame.sprite.Sprite):
    def __init__(self, scaleFactor, velocity, animsDirList, bulletImage, flipSprite=False):
        # initialising sprite logic
        pygame.sprite.Sprite.__init__(self)

<<<<<<< Updated upstream
        self.image = pygame.Surface(size)
=======
        self.image = pygame.Surface((0, 0)).convert_alpha()
>>>>>>> Stashed changes
        self.rect = self.image.get_rect()
        self.scaleFactor = scaleFactor

        self.velocity = velocity

        self.animsDirList = animsDirList

        self.bulletImage = bulletImage

        self.flipSprite = flipSprite


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, size, velocity, startingPos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.rect = self.image.get_rect()
        self.rect.x = startingPos[0]
        self.rect.y = startingPos[1]
        self.size = size
        self.velocity = velocity
