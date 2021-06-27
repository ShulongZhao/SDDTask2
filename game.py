from types import TracebackType
import pygame
from pygame.locals import *


def Game(_frameRate, _clock, _window, _windowBG, _plyr):

    gameState = True
    while gameState:

        # framerate
        _clock.tick(_frameRate)

        # window fill before drawing player
        # so player is above window layer
        _window.fill(_windowBG)

        # quitting the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # exits loop 
                gameState = False

        # getting state of all keys
        keys = pygame.key.get_pressed()
        # keys[pygame.(any key)] is always either 0 (if not being pressed) or 1 (if being pressed); boolean value
        # therefore, keys[pygame.K_RIGHT] = 0, keys[pygame.K_LEFT] = 1 --> player x-coordinate = (0 - 1) * speed --> goes left
        # same for player y-coordinate (down is positive and up is negative, in pygame)
        _plyr["coordinates"][0] += (keys[pygame.K_RIGHT] -
                                    keys[pygame.K_LEFT]) * _plyr["speed"]
        _plyr["coordinates"][1] += (keys[pygame.K_DOWN] -
                                    keys[pygame.K_UP]) * _plyr["speed"]

        

        # player sprite property management
        _plyr["sprite"] = pygame.transform.scale(
            # sprite that is being scaled up
            _plyr["sprite"],
            # the scaled height and width of the sprite
            (_plyr["height"], _plyr["width"]))

        # draws player onto screen
        _window.blit(_plyr["sprite"], (_plyr["coordinates"]))

        pygame.display.update()


    return
