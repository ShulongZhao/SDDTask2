import pygame
from pygame.locals import *


def Game(_framerate, _windowSize, _windowBackground, _plyr, is_game_running):
    # ability to customise game window; different to menu window
    window = pygame.display.set_mode(_windowSize)
    clock = pygame.time.Clock()
    while is_game_running == True:
        # framerate
        clock.tick(_framerate)

        # quitting the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False

        # moving player character
        keys = pygame.key.get_pressed()

        # keys[pygame.(any key)] is always either 0 (if not being pressed) or 1 (if being pressed); boolean value
        # i.e. keys[pygame.K_RIGHT] = 0, keys[pygame.K_LEFT] = 1 --> player x-coordinate = (0 - 1) * speed --> goes left
        # same for player y-coordinate (down is positive and up is negative, in pygame)
        _plyr["coordinates"][0] += (keys[pygame.K_RIGHT] -
                                    keys[pygame.K_LEFT]) * _plyr["speed"]
        _plyr["coordinates"][1] += (keys[pygame.K_DOWN] -
                                    keys[pygame.K_UP]) * _plyr["speed"]

        # window fill before drawing player
        # so player is above window layer
        window.fill(_windowBackground)

        # player sprite property management
        _plyr["sprite"] = pygame.transform.scale(
            # sprite that is being scaled up
            _plyr["sprite"],
            # the scaled height and width of the sprite
            (_plyr["height"], _plyr["width"]))

        # draws player onto screen
        window.blit(_plyr["sprite"], (_plyr["coordinates"]))

        pygame.display.update()

    return
