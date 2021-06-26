import pygame
from pygame.locals import *

size = [700, 700]
background = (50, 50, 50)

plyrCoordinates = [size[0]/2, size[1]/2]
plyrheight, plyrwidth = 20, 20
speed = 7.5

pygame.init()
pygame.display.set_caption("(insert game title here)")
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()


def Game(is_game_running):  # parsed from menu.Menu(), to run the game
    while is_game_running == True:
        # framerate
        clock.tick(50)

        # quitting the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False

        # moving player character
        keys = pygame.key.get_pressed()
        plyrCoordinates[0] += (keys[pygame.K_RIGHT] -
                               keys[pygame.K_LEFT]) * speed
        plyrCoordinates[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * speed

        # screen fill before drawing player
        # so player is above screen layer
        screen.fill(background)

        # loading player character
        plyr = pygame.image.load("Images/playerCharacter.bmp")
        plyr = pygame.transform.scale(plyr, (plyrheight, plyrwidth))
        # draws player onto screen
        screen.blit(plyr, (plyrCoordinates))

        pygame.display.update()

    return
