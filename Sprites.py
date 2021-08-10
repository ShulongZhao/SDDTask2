import pygame
import math
import random

class Character (pygame.sprite.Sprite):
    def __init__(self, scaleFactor, startingPos, speed, animsDirList, health, bulletImage, window):
        # initialising sprite logic
        pygame.sprite.Sprite.__init__(self)

        self.animsDirList = animsDirList
        self.anim = self.animsDirList[0]

        self.scaleFactor = scaleFactor * window.height / 720
        
        self.image = pygame.image.load(self.anim.framesList[0]).convert_alpha()
        # establishing a rect object on the player, and setting its coordinates
        self.rect = self.image.get_rect(x=startingPos[0] * window.height / 720, y=startingPos[1] * window.height / 720)

        # speed is an unchanged magnitude 
        self.speed = [speed[0] * window.height / 720, speed[1] * window.height / 720]
        # whereas velocity changes based on direction
        self.velocity = list((speed[0], speed[1]))
        # diagonal vector is the average of the horizontal and vertical speeds 
        diagonalVector = (self.speed[0] + self.speed[1])/2
        # diagonal speed is the speeds at which the player has to travel horizontally and vertically
        # to travel at exactly diagonal vector's magnitude
        self.diagonalSpeed = [math.sqrt((diagonalVector**2)/2), math.sqrt((diagonalVector**2)/2)]
        self.diagonalVelocity = list((self.diagonalSpeed[0], self.diagonalSpeed[1]))

        self.bulletImage = bulletImage
        self.bullet = Bullet(self.bulletImage, [0, 0], [10, 0], (self.rect.centerx, self.rect.bottom), 0, window)
        self.bullets = []

        self.flipSprite = False

        self.health = health
        self.max_health = health
      

# inherits attributes and methods from Character class 
# but also introduces new attributes specific to humans
class Human (Character):
    def __init__(self, name, scaleFactor, speed, animsDirList, window, health, walkTime=2000, waitTime=3000, bulletImage=None, max_no_of_instances=1):

        self.scaleFactor = scaleFactor
        self.speed = speed
        self.animsDirList = animsDirList
        self.health = health
        self.bulletImage = bulletImage
        
        self.name = name
        # conditions for specific humans movement
        self.is_moving = True
        # walk time is how long human walks for
        self.walkTime = walkTime
        self.waitTime = waitTime
        self.timeSinceLastCall = 0
        self.max_no_of_instances = max_no_of_instances
        
        # allowing this as a seperate function allows calling from anywhere else as well
        self.Main(window)


    def Main(self, window):
        startingPos = [random.randint(0, window.width), 585 * window.height/720]

        Character.__init__(self, self.scaleFactor, startingPos, self.speed, self.animsDirList, self.health, self.bulletImage, window)
        self.rect.size = (int(self.rect.width * self.scaleFactor), int(self.rect.height * self.scaleFactor))

        if random.randint(1, 2) == 1:
            self.flipSprite = True


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, size, velocity, startingPos, cooldown, window):
        pygame.sprite.Sprite.__init__(self)

        # catch exception due to None type error from passing None at initialisation
        try:
            self.image = pygame.transform.scale(pygame.image.load(image), size)
            self.rect = self.image.get_rect()
            self.rect.x = startingPos[0]
            self.rect.y = startingPos[1]
            self.size = size
        except: 
            pass

        self.imagesList = []

        self.velocity = [velocity[0] * window.height / 720, velocity[1] * window.height / 720]

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
