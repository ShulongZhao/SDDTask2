import pygame

def Menu(_frameRate, _window, buttonDict):

    _windowDisplay = _window["display"]

    while True:
        # framerate
        clock = pygame.time.Clock()
        clock.tick(_frameRate)

        # background
        _windowDisplay.blit(_window["menuBG"], (0, 0))

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
            _windowDisplay.blit(button.myText.renderedText, button.textRect)

        pygame.display.update()


def Game(_frameRate, _window, _plyr):

    # local variable intialisation for easier readability
    mouseVisibility = False
    limit_external_input = True
    
    _windowDisplay = _window["display"]
    _window_w = _window["size"][0]
    _window_h = _window["size"][1]

    _plyrCoordinates_X = _plyr.coordinates[0]
    _plyrCoordinates_Y = _plyr.coordinates[1]
    _plyrSize_w = _plyr.size[0]
    _plyrSize_h = _plyr.size[1]

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
        _plyr.coordinates[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * _plyr.speed
        _plyr.coordinates[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * _plyr.speed

        # flipping from left to right facing player surfaces
        if (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) > 0:
            _plyr.surface = _plyr.surface_original
        elif (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) < 0:
            _plyr.surface = _plyr.surface_flipped

        # restrict player's x and y coordinates to edge of window
        if _plyrCoordinates_X < 0:
            _plyrCoordinates_X = 0
        elif _plyrCoordinates_X + _plyrSize_w > _window_w:
            _plyrCoordinates_X = _window_w - _plyrSize_w
        if _plyrCoordinates_Y < 0:
            _plyrCoordinates_Y = 0
        elif _plyrCoordinates_Y + _plyrSize_h > _window_h:
            _plyrCoordinates_Y = _window_h - _plyrSize_h

        # drawing surfaces onto screen
        _windowDisplay.blit(_window["gameBG"], (0, 0))        
        _windowDisplay.blit(_plyr.surface, (_plyr.coordinates))

        # updating screen
        pygame.display.update()


    return



    
