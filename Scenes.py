import pygame

def Menu(_frameRate, _window, buttonDict):

    _windowScreen = _window.screen

    while True:
        # framerate
        clock = pygame.time.Clock()
        clock.tick(_frameRate)

        # background
        _windowScreen.blit(_window.bg, (0, 0))

        # events (key presses, mouse presses)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return None  # exits loop

            # created a loop so any number of buttons
            # can be added without altering this file
            for buttonName in buttonDict:
                button = buttonDict[buttonName]
                # checks if mouse clicks buttons
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # condition for mouse click on buttons
                    if button.IsButtonClick() == True:
                        # exits loop and returns the name of the button
                        return button.myText.originalText

        # calls main() in all buttons of buttonDict
        for buttonName in buttonDict:
            button = buttonDict[buttonName]
            button.main()
            # rendering text so it is on the uppermost layer
            _windowScreen.blit(button.myText.renderedText, button.textRect)

        pygame.display.update()


def Game(_frameRate, _window, _plyr):

    mouseVisibility = False
    limit_external_input = True 

    gameState = True
    while gameState:

        # framerate
        clock = pygame.time.Clock()
        clock.tick(_frameRate)

        # non-visble mouse during in game
        pygame.mouse.set_visible(mouseVisibility)
        # limits all user input to pygame environment
        pygame.event.set_grab(limit_external_input)

        for event in pygame.event.get():

            # quitting the screen
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

        # getting state of all keys
        keys = pygame.key.get_pressed()
        # keys[pygame.(any key)] is always either 0 (if not being pressed) or 1 (if being pressed); boolean value
        # therefore, keys[pygame.K_RIGHT] = 0, keys[pygame.K_LEFT] = 1 --> player x-coordinate = (0 - 1) * speed --> goes left
        # same for player y-coordinate (down is positive and up is negative, in pygame)
<<<<<<< Updated upstream
        _plyr.coordinates[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * _plyr.speed
        _plyr.coordinates[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * _plyr.speed
=======
        if keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] > 0 or keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] < 0:
            _plyrCoordinatesList[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * _plyr.speed
        elif keys[pygame.K_DOWN] - keys[pygame.K_UP] > 0 or keys[pygame.K_DOWN] - keys[pygame.K_UP] < 0:
            _plyrCoordinatesList[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * _plyr.speed
>>>>>>> Stashed changes

        # flipping from left to right facing player surfaces
        if (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) > 0:
            _plyr.surface = _plyr.surface_original
        elif (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) < 0:
            _plyr.surface = _plyr.surface_flipped

        # restrict player's x and y coordinates to edge of window
        if _plyr.coordinates[0] < 0:
            _plyr.coordinates[0] = 0
        elif _plyr.coordinates[0] + _plyr.size[0] > _window.width:
            _plyr.coordinates[0] = _window.width - _plyr.size[0]
        if _plyr.coordinates[1] < 0:
            _plyr.coordinates[1] = 0
        elif _plyr.coordinates[1] + _plyr.size[1] > _window.height:
            _plyr.coordinates[1] = _window.height - _plyr.size[1]

        # drawing surfaces onto screen
        _window.screen.blit(_window.bg, (0, 0))        
        _window.screen.blit(_plyr.surface, (_plyr.coordinates))

        # updating screen
        pygame.display.update()


    return



    
