import pygame


def Game(_frameRate, _window, _plyr):

    mouseVisibility = False
    limit_external_input = True

    
    windowDisplay = _window["display"]

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
        windowDisplay.blit(_window["gameBG"], (0, 0))

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



        windowX_restriction = _window["size"][0]  # restrict to width of window
        # restrict to height of window
        windowY_restriction = _window["size"][1]

        # restrict player's x and y coordinates to edge of window
        # restricting to left side
        if _plyr["coordinates"][0] < 0:             
            _plyr["coordinates"][0] = 0

        # restricting to right side; 
        # added player width so player does not clip through the edge of screen
        elif _plyr["coordinates"][0] + _plyr["width"] > windowX_restriction:
            _plyr["coordinates"][0] = windowX_restriction - _plyr["width"]

        # restricting to top edge
        if _plyr["coordinates"][1] < 0:             
            _plyr["coordinates"][1] = 0
        
        # restricting to bottom edge
        # added player height so player does not clip through the edge of screen
        elif _plyr["coordinates"][1] + _plyr["height"] > windowY_restriction:    
            _plyr["coordinates"][1] = windowY_restriction - _plyr["height"]


        # draws player onto screen
        print(_plyr["coordinates"])
        windowDisplay.blit(_plyr["sprite"], (_plyr["coordinates"]))

        pygame.display.update()

    return
