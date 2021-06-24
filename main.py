import pygame
from pygame.locals import *

pygame.init()  # initialise python


size = [700, 700]
background = (50, 50, 50)

screen = pygame.display.set_mode(size)

plyrCoordinates = [200, 200]
image_height, image_width = 50, 50
movementIncrement = 2

while True:
    for event in pygame.event.get():
        # initialising screen
        pygame.display.set_caption("(insert game title here)")
        screen.fill(background)

        # quitting the screen
        if event.type == pygame.QUIT:
            exit()

        # loading player character
        plyr = pygame.image.load("Images/playerCharacter.bmp")
        plyr = pygame.transform.scale(plyr, (image_height, image_width))
        screen.blit(source=plyr, dest=plyrCoordinates)
        rect = plyr.get_rect()  # forms a rect around image for collision detection

        # moving player character
        # returns array of booleans, showing which keys are pressed
        while event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                plyrCoordinates[0] -= movementIncrement
            elif event.key == pygame.K_RIGHT:
                plyrCoordinates[0] += movementIncrement
            elif event.key == pygame.K_UP:
                plyrCoordinates[1] -= movementIncrement
            elif event.key == pygame.K_DOWN:
                plyrCoordinates[1] += movementIncrement
            break

        pygame.display.update()
