import pygame

from Sprites import Bullet

def Menu(_window, buttonDict):

    GUISpriteGroup = pygame.sprite.Group()

    while True:
        # framerate
        clock = pygame.time.Clock()
        clock.tick(_window.frameRate)

        # background
        _window.screen.blit(_window.bg, (0, 0))

        # calls main() in all buttons of buttonDict
        for buttonName in buttonDict:
            button = buttonDict[buttonName]
            button.main()
            GUISpriteGroup.add(button)
         
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
                    if button.IsLayerClicked() == True:
                        # exits loop and returns the name of the button
                        return button.myText.originalText

        
        GUISpriteGroup.draw(_window.screen)
        #_window.screen.blit(button.myText.renderedText, button.rect)

        pygame.display.update()


def Game(_window, _plyr):

    bullets = []

    mouseVisibility = True

    characterSpriteGroup = pygame.sprite.Group()
    characterSpriteGroup.add(_plyr)
    
    gameState = True
    while gameState:

        # framerate
        clock = pygame.time.Clock()
        clock.tick(_window.frameRate)

        # mouse visibility during the game
        pygame.mouse.set_visible(mouseVisibility)

        for event in pygame.event.get():

            # quitting the screen
            if event.type == pygame.QUIT:
                # exits loop
                gameState = False   

            # if player hits escape, mouse is unhidden;
            # if player hits mouse down, mouse is hidden,
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mouseVisibility = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseVisibility = False
        
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
                    
                    # initalises the animation
                    InitAnim(_plyr.animsDirList[2])

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
            _plyr.rect.x += deltHorizMovement * _plyr.velocity
        elif deltaVertMovement:
            _plyr.rect.y += deltaVertMovement * _plyr.velocity

        # flipping from left to right facing player surfaces
        if deltHorizMovement > 0:
            _plyr.flipSprite = False
        elif deltHorizMovement < 0:
            _plyr.flipSprite = True

        # restrict player's x and y coordinates to edge of window
        if _plyr.rect.x < 0:
            _plyr.rect.x = 0
        elif _plyr.rect.x + _plyr.rect.width > _window.width:
            _plyr.rect.x = _window.width - _plyr.rect.width
        if _plyr.rect.y < 0:
            _plyr.rect.y = 0
        elif _plyr.rect.y + _plyr.rect.height > _window.height:
            _plyr.rect.y = _window.height - _plyr.rect.height
              

        def InitAnim(anim):
            _plyr.anim = anim
            # reset the cycles of the animation whenever it is called
            _plyr.anim.currentCycles = 0
 
        curTime = pygame.time.get_ticks()
        # if the current time minus the time since the last animation was played is greater than the cooldown...
        # for animation frame time control
        if(curTime - _plyr.anim.timeSinceLastCall >= _plyr.anim.cooldown):
            try:
                # deactivate animation if the maximum number of cycles has been reached
                while _plyr.anim.currentCycles != _plyr.anim.maxCycles:
                    # update player rect
                    _plyr.image = pygame.image.load(_plyr.anim.framesList[_plyr.anim.idx])
                    _plyr.rect = _plyr.image.get_rect(x=_plyr.rect.x, y=_plyr.rect.y)
                    _plyr.rect.size = (int(_plyr.rect.width * _plyr.scaleFactor), int(_plyr.rect.height * _plyr.scaleFactor))
                    # broadcast updated player info to the sprite's image component
                    _plyr.image = pygame.transform.flip(
                        pygame.transform.scale(
                                _plyr.image,
                            _plyr.rect.size), 
                        _plyr.flipSprite, False).convert_alpha()

                    _plyr.anim.idx += 1
                    _plyr.anim.currentCycles += 1
                    _plyr.anim.timeSinceLastCall = curTime
                    break
                else:
                    _plyr.anim = _plyr.animsDirList[0]
            except IndexError:
                _plyr.anim.idx = 0

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
