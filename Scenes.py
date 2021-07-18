import pygame
from Sprites import Bullet

def Menu(_window, buttonDict):

    _windowScreen = _window.screen

    while True:
        # framerate
        clock = pygame.time.Clock()
        clock.tick(_window.frameRate)

        # background
        _windowScreen.blit(_window.bg, (0, 0))

        # events (key presses, mouse presses)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return None  # exits loop

            # loops through all buttons within the scene
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


def Game(_window, _plyr):

    bullets = []

    mouseVisibility = False
    limit_external_input = True 

    characterSpriteGroup = pygame.sprite.Group()
    characterSpriteGroup.add(_plyr)

    # added local variables because rect's own coordinates reset after every iteration
    # therefore function updates local variables and passes them to player rect coordinates
    plyr_X = 0
    plyr_Y = 0

    gameState = True
    while gameState:

        # framerate
        clock = pygame.time.Clock()
        clock.tick(_window.frameRate)

        # non-visble mouse during in game
        pygame.mouse.set_visible(mouseVisibility)
        # limits all user input to pygame environment
        pygame.event.set_grab(limit_external_input)

        for event in pygame.event.get():

            # quitting the screen
            if event.type == pygame.QUIT:
                gameState = False   # exits loop

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
        
            # shoot bullet when space pressed
            # (created 2 keydown event checks to split both functionalities apart)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playerBullet = Bullet(_plyr.bulletImage, [10, 10], 10, startingPos=(_plyr.rect.centerx, _plyr.rect.bottom))
                    if _plyr.flipSprite == False:
                        playerBullet.velocity = abs(playerBullet.velocity)
                    elif _plyr.flipSprite == True:
                        playerBullet.velocity = -(playerBullet.velocity)
                    bullets.append(playerBullet)
                    _plyr.animsDirList[2].isActive = True

        # getting state of all keys
        keys = pygame.key.get_pressed()
        # keys[pygame.(any key)] is always either 0 (if not being pressed) or 1 (if being pressed); boolean value
        # therefore, keys[pygame.K_RIGHT] = 0, keys[pygame.K_LEFT] = 1 --> player x-coordinate = (0 - 1) * velocity --> goes left
        # same for player y-coordinate (down is positive and up is negative, in pygame)
        deltaVertMovement = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        deltHorizMovement = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        
        # restricting diagonal movement by only either allowing 
        # horizontal or vertical movement at a time
        if deltHorizMovement:
            plyr_X += deltHorizMovement * _plyr.velocity
        elif deltaVertMovement:
            plyr_Y += deltaVertMovement * _plyr.velocity

        # flipping from left to right facing player surfaces
        if deltHorizMovement > 0:
            _plyr.flipSprite = False
        elif deltHorizMovement < 0:
            _plyr.flipSprite = True

    
        # restrict player's x and y coordinates to edge of window
        if plyr_X < 0:
            plyr_X = 0
        elif plyr_X + _plyr.rect.width > _window.width:
            plyr_X = _window.width - _plyr.rect.width
        if plyr_Y < 0:
            plyr_Y = 0
        elif plyr_Y + _plyr.rect.height > _window.height:
            plyr_Y = _window.height - _plyr.height


        for _plyrDir in _plyr.animsDirList:
            # sort the list into alphabetical order
            _plyrDir.animFramesList.sort()


            try:
                # if animation is active
                if (_plyrDir.isActive == True) and _plyrDir != "Images/playersprites/idle":

                    plyrImage = pygame.image.load(
                        _plyrDir.animFramesList[_plyrDir.plyrAnimIdx]).convert_alpha()
                    _plyr.rect = plyrImage.get_rect(x=plyr_X, y=plyr_Y)
                    _plyr.rect.size = (int(_plyr.rect.width * _plyr.scaleFactor), int(_plyr.rect.height * _plyr.scaleFactor))

                    _plyr.image = pygame.transform.flip(
<<<<<<< Updated upstream
                        pygame.transform.scale(
                                pygame.image.load(_plyrDir.animFramesList[_plyrDir.plyrAnimIdx]), 
                            _plyr.size),
                        _plyr.flipSprite, False
                    )
=======
                        pygame.transform.scale(plyrImage, _plyr.rect.size), _plyr.flipSprite, False).convert_alpha()

>>>>>>> Stashed changes
                else:
                    plyrImage = pygame.image.load(
                        _plyr.animsDirList[0].animFramesList[_plyrDir.plyrAnimIdx]).convert_alpha()
                    _plyr.rect = plyrImage.get_rect(x=plyr_X, y=plyr_Y)
                    _plyr.rect.size = (int(_plyr.rect.width * _plyr.scaleFactor), int(_plyr.rect.height * _plyr.scaleFactor))


                    _plyr.image = pygame.transform.flip(
<<<<<<< Updated upstream
                        pygame.transform.scale(
                                pygame.image.load(_plyr.animsDirList[0].animFramesList[_plyrDir.plyrAnimIdx]), 
                            _plyr.size),
                        _plyr.flipSprite, False
                    )
=======
                        pygame.transform.scale(plyrImage, _plyr.rect.size), _plyr.flipSprite, False).convert_alpha()

>>>>>>> Stashed changes
                _plyrDir.plyrAnimIdx += 1
            except IndexError:
                # loop back to 0 index after all animations have been looped
                _plyrDir.plyrAnimIdx = 0

            if _plyrDir.maxCycles == -1:
                _plyrDir.maxCycles == -2
                break

            if _plyrDir.currentCycles == _plyrDir.maxCycles:
                _plyrDir.isActive = False

            _plyrDir.currentCycles += 1

        # updating all visible bullets on screen
        for bullet in bullets:
            # deleting bullets that travel off screen
            if bullet.rect.x > _window.width or bullet.rect.y > _window.height:
                bullets.remove(bullet)
            # updating bullet coordinates
            bullet.rect.x += bullet.velocity

            characterSpriteGroup.add(bullet)

        # drawing surfaces onto screen
        _window.screen.blit(_window.bg, (0, 0))

        characterSpriteGroup.update()
        characterSpriteGroup.draw(_window.screen)


        # updating screen
        pygame.display.update()


    return
     




    
