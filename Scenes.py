import pygame

from Sprites import Bullet


def Menu(window, buttonDict):

    GUISpriteGroup = pygame.sprite.Group()

    while True:
        # framerate
        clock = pygame.time.Clock()
        clock.tick(window.frameRate)

        # background
        window.screen.blit(window.bg, (0, 0))

        # calls main() in all buttons of buttonDict
        for buttonRef in buttonDict:
            button = buttonDict[buttonRef]
            button.main()
            GUISpriteGroup.add(button)
         
        # events (key presses, mouse presses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # exits loop

            # loops through all buttons within the scene
            for buttonRef in buttonDict:
                button = buttonDict[buttonRef]
                # checks if mouse clicks buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # condition for mouse click on buttons
                    if button.IsLayerClicked() == True:
                        # exits loop and returns the name of the button
                        return button.myText.originalText

        
        GUISpriteGroup.draw(window.screen)

        pygame.display.update()


def Game(window, charList):
    
    # calling character objects
    plyr = charList[0]
    enemy = charList[1]

    mouseVisibility = True

    starting = False
    dogfight = False

    characterSpriteGroup = pygame.sprite.Group()
    characterSpriteGroup.add(character for character in charList)
    

    gameState = True
    while gameState:

        # framerate
        clock = pygame.time.Clock()
        clock.tick(window.frameRate)
        curTime = pygame.time.get_ticks()

        # mouse visibility during the game
        pygame.mouse.set_visible(mouseVisibility)

        # getting state of all keys
        keys = pygame.key.get_pressed()
        # keys[pygame.(any key)] is always either 0 (if not being pressed) or 1 (if being pressed); boolean value
        deltaVert = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        deltaHoriz = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]

        # dogfight begins if B pressed, only for development reasons will be removed in final game.
        if keys[pygame.K_b]:
            starting = True
            dogfight = True

        if enemy.rect.y < window.height/2 and starting:
            enemy.rect.y += enemy.velocity[1]
        if enemy.rect.x + enemy.rect.width < (window.width - 15) and starting:
            enemy.rect.x += enemy.velocity[1]
        if enemy.rect.x + enemy.rect.width > (window.width - 16) and enemy.rect.y > (window.height/2-1) and starting:
            starting = False
            
        # flipping player sprite based on direction 
        if enemy.health > 0:
            if deltaHoriz > 0:
                plyr.velocity[0] = abs(plyr.speed[0])
                plyr.diagonalSpeed[0] = abs(plyr.diagonalSpeed[0])
                plyr.flipSprite = False
            elif deltaHoriz < 0:
                plyr.velocity[0] = -abs(plyr.speed[0])
                plyr.diagonalSpeed[0] = -abs(plyr.diagonalSpeed[0])
                plyr.flipSprite = True
            elif deltaHoriz == 0:
                plyr.velocity[0] = 0

        # moving player vertically 
        if deltaVert > 0:
            plyr.velocity[1] = abs(plyr.speed[1])
            plyr.diagonalSpeed[1] = abs(plyr.diagonalSpeed[1])
        elif deltaVert < 0:
            plyr.velocity[1] = -(abs(plyr.speed[1]))
            plyr.diagonalSpeed[1] = -abs(plyr.diagonalSpeed[1])
        elif deltaVert == 0:
            plyr.velocity[1] = 0

        if deltaHoriz != 0 and deltaVert != 0:
            plyr.velocity = plyr.diagonalSpeed

        plyr.rect.x += plyr.velocity[0]
        plyr.rect.y += plyr.velocity[1]

        # restrict player's x and y coordinates to edge of window
        if plyr.rect.x < 0:
            plyr.rect.x = 0
        elif plyr.rect.x + plyr.rect.width > window.width:
            plyr.rect.x = window.width - plyr.rect.width
        if dogfight == False:
            if plyr.rect.y < enemy.rect.height + enemy.rect.y:
                plyr.rect.y = enemy.rect.height + enemy.rect.y
        elif plyr.rect.y < 0:
            plyr.rect.y = 0
        elif plyr.rect.y + plyr.rect.height > window.height:
            plyr.rect.y = window.height - plyr.rect.height

        plyrColEnemy = plyr.rect.colliderect(enemy.rect)
        if plyrColEnemy:
            InitAnim(plyr, plyr.animsDirList[1])
            InitAnim(enemy, enemy.animsDirList[1])


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
                if event.key == pygame.K_SPACE and curTime - plyr.bullet.timeSinceLastCall >= plyr.bullet.cooldown:
                    plyr.bullet = Bullet(plyr.bulletImage, [10, 10], [10, 0], (plyr.rect.centerx, plyr.rect.bottom), 400)
                    plyr.bullet.InitVelocity(plyr.velocity, plyr.flipSprite)
                    plyr.bullets.append(plyr.bullet)

                    plyr.bullet.timeSinceLastCall = curTime

                    # initalises the animation
                    InitAnim(plyr, plyr.animsDirList[2])

        def InitAnim(char, anim):
            char.anim = anim
            # reset the cycles of the animation whenever it is called
            char.anim.currentCycles = 0
            char.anim.idx = 0

            
        for char in charList:
            # if the current time minus the time since the last animation was played is greater than the cooldown...
            # for animation frame time control
            if(curTime - char.anim.timeSinceLastCall >= char.anim.cooldown):
                try:
                    # deactivate animation if the maximum number of cycles has been reached
                    while char.anim.currentCycles != char.anim.maxCycles:
                        # update player rect
                        char.image = pygame.image.load(char.anim.framesList[char.anim.idx])
                        char.rect = char.image.get_rect(x=char.rect.x, y=char.rect.y)
                        char.rect.size = (int(char.rect.width * char.scaleFactor), int(char.rect.height * char.scaleFactor))
                        # broadcast updated player info to the sprite's image component
                        char.image = pygame.transform.flip(
                            pygame.transform.scale(
                                    char.image,
                                char.rect.size), 
                            char.flipSprite, False).convert_alpha()

                        char.anim.idx += 1
                        char.anim.currentCycles += 1
                        char.anim.timeSinceLastCall = curTime
                        break
                    else:
                        char.anim = char.animsDirList[0]
                        char.anim.idx = 0
                except IndexError:
                    char.anim.idx = 0
            

        # updating all visible plyr bullets on screen
        for bullet in plyr.bullets:
            # deleting plyr bullets that travel off screen
            if bullet.rect.x < 0 or bullet.rect.x > window.width or bullet.rect.y < 0 or bullet.rect.y > window.height:
                plyr.bullets.remove(bullet)
            
            # updating bullet rect
            bullet.rect.x += bullet.velocity[0]
            bullet.rect.y += bullet.velocity[1]


            characterSpriteGroup.add(bullet)

            # if enemy gets hit
            bulletColEnemy = bullet.rect.colliderect(enemy.rect)
            if bulletColEnemy:
                plyr.bullets.remove(bullet)
                characterSpriteGroup.remove(bullet)
                InitAnim(enemy, enemy.animsDirList[1])
                enemy.health += -1
                print(enemy.health)

        # enemy movement
        if dogfight == False:
            enemy.rect.x += enemy.velocity[0]

        if enemy.rect.x < 0 or enemy.rect.x + enemy.rect.width > window.width:
            enemy.velocity[0] = -enemy.velocity[0]
        if enemy.rect.y < 0 or enemy.rect.y + enemy.rect.height > window.height:
            enemy.velocity[1] = -enemy.velocity[1]

        # drawing surfaces onto screen
        window.screen.blit(window.bg, (0, 0))

        characterSpriteGroup.update()
        characterSpriteGroup.draw(window.screen)

        if enemy.health == 0:
            InitAnim(enemy, enemy.animsDirList[2])
            for bullet in plyr.bullets:
                bullet.velocity[0] = 0
            plyr.speed = [0, 0]
            plyr.diagonalSpeed = [0, 0]
            enemy.rect.y -= 10
        

        # updating screen
        pygame.display.update()


    return
