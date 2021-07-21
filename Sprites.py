import pygame

class Character (pygame.sprite.Sprite):
    def __init__(self, scaleFactor, velocity, animsDirList, bulletImage):
        # initialising sprite logic
        pygame.sprite.Sprite.__init__(self)

        self.animsDirList = animsDirList
        self.anim = self.animsDirList[0]

        self.scaleFactor = scaleFactor
        
        # setting the image to the first idle image
        self.image = pygame.image.load(self.anim.framesList[0]).convert_alpha()
        self.rect = self.image.get_rect()

        self.velocity = velocity

        


        self.bulletImage = bulletImage

        self.flipSprite = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, size, velocity, startingPos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.imagesList = []
        self.rect = self.image.get_rect()
        self.rect.x = startingPos[0]
        self.rect.y = startingPos[1]
        self.size = size
        self.velocity = velocity
