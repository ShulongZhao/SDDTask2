import pygame
from pygame.locals import *

size = [700, 700]
background = (50, 50, 50)

plyrCoordinates = [size[0]/2, size[1]/2]
plyrheight, plyrwidth = 100, 100
speed = 5

pygame.init()
pygame.display.set_caption("(insert game title here)")
screen = pygame.display.set_mode(size)


def game():
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
