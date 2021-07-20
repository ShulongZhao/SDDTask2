import pygame

class Character (pygame.sprite.Sprite):
    def __init__(self, scaleFactor, startingPos, velocity, animsDirList, bulletImage):
        # initialising sprite logic
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((0, 0)).convert_alpha()
        # establishing a rect object on the player, and setting its coordinates
        self.rect = self.image.get_rect(center=startingPos)
        self.scaleFactor = scaleFactor

        self.velocity = velocity

        self.animsDirList = animsDirList

        self.bulletImage = bulletImage
        self.bullets = []

        self.flipSprite = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, size, velocity, startingPos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.rect = self.image.get_rect()
        self.rect.x = startingPos[0]
        self.rect.y = startingPos[1]
        self.size = size
        self.velocity = velocity
        self.i = 0

    def InitVelocity(self, plyrVelocity, flipSprite):
        # only sets the velocity initialisation once
        while self.i < 1:
            # j iterates as 0 and 1, and therefore manipulates each index of 
            # velocities of player and bullet at the same time
            for j in range(len(plyrVelocity) - 1):
                # if when the player shoots, the player is facing left
                if flipSprite:
                    self.velocity[j] = -(abs(plyrVelocity[j]) + self.velocity[j])
                # ...or facing right
                elif flipSprite == False:
                    self.velocity[j] = abs(plyrVelocity[j]) + self.velocity[j]
            self.i += 1
