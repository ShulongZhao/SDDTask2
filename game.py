import pygame
from pygame.locals import *
import time

pygame.init()

size = [700, 700]
background = (50, 50, 50)

screen = pygame.display.set_mode(size)

plyrCoordinates = [200, 200]
image_height, image_width = 50, 50

speedMultiplier = 2

gameState = True
while gameState:
    for event in pygame.event.get():
        # initialising screen
        pygame.display.set_caption("(insert game title here)")
        screen.fill(background)

        # quitting the screen
        if event.type == pygame.QUIT:
            gameState = False

        # loading player character
        plyr = pygame.image.load("Images/playerCharacter.bmp")
        plyr = pygame.transform.scale(plyr, (image_height, image_width))
        # redraws ball image onto screen
        screen.blit(source=plyr, dest=plyrCoordinates)
        # forms a rect around image for collision detection
        rect = plyr.get_rect()

        # moving player character
        keys = pygame.key.get_pressed()

        plyrCoordinates[0] += (keys[pygame.K_RIGHT] -
                               keys[pygame.K_LEFT]) * speedMultiplier
        plyrCoordinates[1] += (keys[pygame.K_DOWN] -
                               keys[pygame.K_UP]) * speedMultiplier

        pygame.display.update()


pygame.quit()
exit()
