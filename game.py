import pygame

#bullet class
class boolet():
    def __init__(self, location, vector, sprite):
        self.location = location
        self.height = 10
        self.width = 10
        self.velocity = 10 * vector
        self.sprite = sprite        


def Game(_frameRate, _window, _plyr):

    boolets = []

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

        # converting player coordinates from tuple to list to access each element
        _plyr_coordinates_list = list(_plyr["coordinates"])

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
        _plyr_coordinates_list[0] += (keys[pygame.K_RIGHT] -
                                    keys[pygame.K_LEFT]) * _plyr["speed"]
        _plyr_coordinates_list[1] += (keys[pygame.K_DOWN] -
                                    keys[pygame.K_UP]) * _plyr["speed"]

        # player sprite property management
        _plyr["sprite"] = pygame.transform.scale(
            # sprite that is being scaled up
            _plyr["sprite"],
            # the scaled height and width of the sprite
            (_plyr["height"], _plyr["width"]))

        # Left and right facing player sprites
        rightPlayer = pygame.transform.scale(pygame.image.load('Images/playerCharacter.bmp'), (_plyr["height"], _plyr["width"]))
        leftPlayer = pygame.transform.scale(pygame.transform.flip(rightPlayer, True, False), (_plyr["height"], _plyr["width"]))

        # flip player when it changes direction
        if (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) < 0:
            _plyr["sprite"] = leftPlayer
        elif (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) > 0: 
            _plyr["sprite"] = rightPlayer

        rightBoolet = pygame.transform.scale(pygame.image.load('Images/bullet.bmp'), (10, 10))
        leftBoolet =  pygame.transform.scale(pygame.transform.flip(rightBoolet, True, False), (10, 10))
        # shoot bullet when space pressed
        if keys[pygame.K_SPACE]:
            print("pew pew")
            if _plyr["sprite"] == leftPlayer:
                vector = -1
                sprite = leftBoolet
            else:
                vector = 1
                sprite = rightBoolet
            boolets.append(boolet(_plyr_coordinates_list, vector, sprite))

        windowX_restriction = _window["size"][0]  # restrict to width of window
        # restrict to height of window
        windowY_restriction = _window["size"][1]

        # restrict player's x and y coordinates to edge of window
        # restricting to left side
        if _plyr_coordinates_list[0] < 0:             
            _plyr_coordinates_list[0] = 0
        # restricting to right side; 
        # added player width so player does not clip through the edge of screen
        elif _plyr_coordinates_list[0] + _plyr["width"] > windowX_restriction:
            _plyr_coordinates_list[0] = windowX_restriction - _plyr["width"]
        # restricting to top edge
        if _plyr_coordinates_list[1] < 0:             
            _plyr_coordinates_list[1] = 0
        # restricting to bottom edge
        # added player height so player does not clip through the edge of screen
        elif _plyr_coordinates_list[1] + _plyr["height"] > windowY_restriction:    
            _plyr_coordinates_list[1] = windowY_restriction - _plyr["height"]

        
        _plyr["coordinates"] = (_plyr_coordinates_list[0], _plyr_coordinates_list[1]) 

        # window fill before drawing player
        # so player is above window layer
        windowDisplay.blit(_window["gameBG"], (0, 0))
        windowDisplay.blit(_plyr["sprite"], (_plyr["coordinates"]))

        for bullet in boolets:
            bullet.location[0] += bullet.velocity
            windowDisplay.blit(bullet.sprite, bullet.location)
    
        pygame.display.update()

    return
