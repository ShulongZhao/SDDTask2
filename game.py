import pygame
from pygame.locals import *
#import time

size = [700, 700]
background = (50, 50, 50)

pygame.init()
screen = pygame.display.set_mode(size)

plyrCoordinates = [size[0]/2, size[1]/2]
plyrheight, plyrwidth = 100, 100
speed = 5

pygame.display.set_caption("(insert game title here)")

gameState = True
while gameState:
    # quitting the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameState = False

    # moving player character
    keys = pygame.key.get_pressed()
    plyrCoordinates[0] += (keys[pygame.K_RIGHT] -
                           keys[pygame.K_LEFT]) * speed
    plyrCoordinates[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * speed

    screen.fill(background)

    # loading player character
    plyr = pygame.image.load("Images/playerCharacter.bmp")
    plyr = pygame.transform.scale(plyr, (plyrheight, plyrwidth))
    # draws player onto screen
    screen.blit(plyr, (plyrCoordinates))

    pygame.display.update()


pygame.quit()
exit()
