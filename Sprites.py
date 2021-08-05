import pygame
import math

class Character (pygame.sprite.Sprite):
    def __init__(self, scaleFactor, startingPos, speed, animsDirList, bulletImage, health):
        # initialising sprite logic
        pygame.sprite.Sprite.__init__(self)

        self.animsDirList = animsDirList
        self.anim = self.animsDirList[0]

        self.scaleFactor = scaleFactor
        
        self.image = pygame.image.load(self.anim.framesList[0]).convert_alpha()
        # establishing a rect object on the player, and setting its coordinates
        self.rect = self.image.get_rect(x=startingPos[0], y=startingPos[1])
        self.scaleFactor = scaleFactor        

        # speed is an unchanged magnitude 
        self.speed = speed
        # whereas velocity changes based on direction
        self.velocity = list((speed[0], speed[1]))
        # diagonal vector is the average of the horizontal and vertical speeds 
        diagonalVector = (self.speed[0] + self.speed[1])/2
        # diagonal speed is the speeds at which the player has to travel horizontally and vertically
        # to travel at exactly diagonal vector's magnitude
        self.diagonalSpeed = [math.sqrt((diagonalVector**2)/2), math.sqrt((diagonalVector**2)/2)]
        self.diagonalVelocity = list((self.diagonalSpeed[0], self.diagonalSpeed[1]))

        self.bulletImage = bulletImage
        self.bullet = Bullet(self.bulletImage, [0, 0], [10, 0], (self.rect.centerx, self.rect.bottom), 0)
        self.bullets = []

        self.flipSprite = False

        self.health = health
        self.MAX_HEALTH = health

    def drawHealth(self):
        r = min(255, 255 - (255 * ((self.health - (self.MAX_HEALTH - self.health)) / self.MAX_HEALTH)))
        g = min(255, 255 * (self.health / (self.MAX_HEALTH / 2)))
        color = (r, g, 0)
        width = int(self.rect.width * self.health / self.MAX_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 7)
        if self.health < self.MAX_HEALTH:
            pygame.draw.rect(self.image, color, self.health_bar)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, size, velocity, startingPos, cooldown):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.imagesList = []

        self.rect = self.image.get_rect()
        self.rect.x = startingPos[0]
        self.rect.y = startingPos[1]
        self.size = size

        self.velocity = velocity

        self.timeSinceLastCall = 0
        self.cooldown = cooldown

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
