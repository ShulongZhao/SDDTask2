from types import TracebackType
import pygame
from pygame.locals import *


def Game(_frameRate, _window, _windowBG, _plyr):

    mouseVisibility = False
    limit_external_input = True

    gameState = True
    while gameState:

        # framerate
        clock = pygame.time.Clock()
        clock.tick(_frameRate)

        # non-visble mouse during in game
        pygame.mouse.set_visible(mouseVisibility)
        #limits all user input to pygame environment
        pygame.event.set_grab(limit_external_input)

        # window fill before drawing player
        # so player is above window layer
        _window.fill(_windowBG)

        # quitting the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # exits loop
                gameState = False
            
            # if player hits escape, mouse is unhidden;
            # if player hits mouse down when mouse is unhidden,
            # mouse is hidden again
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # mouse visibility is true
                    mouseVisibility = True
                    limit_external_input = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (mouseVisibility == True) and (limit_external_input == False):
                    mouseVisibility = False
                    limit_external_input = True

        # getting state of all  keys
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
