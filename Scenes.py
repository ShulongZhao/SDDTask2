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

        if enemy.rect.y < window.height/2 - enemy.rect.y/2 and starting:
            enemy.rect.y += enemy.velocity[1]
        if enemy.rect.x + enemy.rect.width < (window.width - 15) and starting:
            enemy.rect.x += enemy.velocity[1]
        if enemy.rect.x + enemy.rect.width > (window.width - 16) and enemy.rect.y > (window.height/2- enemy.rect.y/2 -1) and starting:
            enemy.flipSprite = True
            starting = False
            
        # assigning the direction to the player's velocity
        # deltaHoriz and deltaVert are either 1, 0, -1, which assigns direction correctly        
        plyr.velocity[0] = deltaHoriz * plyr.speed[0]
        plyr.velocity[1] = deltaVert * plyr.speed[1]
        # diagonal velocity is to keep the player from travelling quicker 
        # than the normal horizontal and vertical speeds (pythagoras' theorem)
        # --> see player class for more on diagonal velocity
        plyr.diagonalVelocity[0] = deltaHoriz * plyr.diagonalSpeed[0] 
        plyr.diagonalVelocity[1] = deltaVert * plyr.diagonalSpeed[1]
        # if player is going left, flip sprite
        plyr.flipSprite = keys[pygame.K_LEFT]

        # if the player is going diagonally, assign the diagonal speed
        if deltaHoriz != 0 and deltaVert != 0:
            plyr.velocity = plyr.diagonalVelocity
        
        # add the velocity to the player's position 
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
        if plyr.rect.y + plyr.rect.height > window.height - 2 * plyr.rect.height and plyr.health > 0:
            plyr.rect.y = window.height - 3 * plyr.rect.height

        plyrColEnemy = plyr.rect.colliderect(enemy.rect)
        if plyrColEnemy and plyr.health > 0:
            InitAnim(plyr, plyr.animsDirList[1])
            InitAnim(enemy, enemy.animsDirList[1])
            plyr.health += -1
            enemy.health += -1


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
                    plyr.bullet = Bullet(plyr.bulletImage, [20, 10], [10, 0], (plyr.rect.centerx, plyr.rect.bottom), 400)
                    plyr.bullet.InitVelocity(plyr.velocity, plyr.flipSprite)
                    plyr.bullets.append(plyr.bullet)

                    plyr.bullet.timeSinceLastCall = curTime

                    # initalises the animation
                    InitAnim(plyr, plyr.animsDirList[2])

        if dogfight == True and curTime - enemy.bullet.timeSinceLastCall >= enemy.bullet.cooldown:
            enemy.bullet = Bullet(enemy.bulletImage, [20, 10], [10, 0], (enemy.rect.centerx, enemy.rect.bottom), 400)
            enemy.bullet.InitVelocity(enemy.velocity, enemy.flipSprite)
            enemy.bullets.append(enemy.bullet)

            enemy.bullet.timeSinceLastCall = curTime
            InitAnim(plyr, plyr.animsDirList[2])
        
        for bullet in enemy.bullets:
            # deleting enemy bullets that travel off screen
            if bullet.rect.x < 0 or bullet.rect.x > window.width or bullet.rect.y < 0 or bullet.rect.y > window.height:
                enemy.bullets.remove(bullet)
            
            # updating bullet rect
            bullet.rect.x += bullet.velocity[0]
            bullet.rect.y += bullet.velocity[1]
            
            characterSpriteGroup.add(bullet)

            bulletColPlyr = bullet.rect.colliderect(plyr.rect)
            if bulletColPlyr:
                enemy.bullets.remove(bullet)
                characterSpriteGroup.remove(bullet)
                InitAnim(plyr, plyr.animsDirList[1])
                plyr.health += -1
                print(plyr.health)

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
            InitAnim(enemy, enemy.animsDirList[3])
            for bullet in plyr.bullets:
                bullet.velocity[0] = 0
            plyr.speed = [0, 0]
            plyr.diagonalSpeed = [0, 0]
            enemy.rect.y -= 10

        if plyr.health == 0:
            InitAnim(plyr, plyr.animsDirList[3])
            for bullet in plyr.bullets:
                bullet.velocity[0] = 0
            plyr.speed = [0, 0]
            plyr.diagonalSpeed = [0, 0]
            plyr.rect.y += 10

        enemy.drawHealth()

        # updating screen
        pygame.display.update()


    return
