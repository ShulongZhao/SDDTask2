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

        
        GUISpriteGroup.draw(window.screen)

        pygame.display.update()


def Game(window, plyr, enemy):

    charList = [plyr, enemy]

    mouseVisibility = False
    limit_external_input = True 

    characterSpriteGroup = pygame.sprite.Group()
    characterSpriteGroup.add(plyr, enemy)

    gameState = True
    while gameState:

        print(plyr.speed)

        # calling character objects
        plyr
        enemy

        # framerate
        clock = pygame.time.Clock()
        clock.tick(window.frameRate)

        # non-visble mouse during in game
        pygame.mouse.set_visible(mouseVisibility)
        # limits all user input to pygame environment
        pygame.event.set_grab(limit_external_input)

        # getting state of all keys
        keys = pygame.key.get_pressed()
        # keys[pygame.(any key)] is always either 0 (if not being pressed) or 1 (if being pressed); boolean value
        deltaVert = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        deltaHoriz = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]

        # flipping horizontal faces
        if deltaHoriz > 0:
            plyr.velocity[0] = abs(plyr.speed[0])
            plyr.flipSprite = False
        elif deltaHoriz < 0:
            plyr.velocity[0] = -abs(plyr.speed[0])
            plyr.flipSprite = True
        elif deltaHoriz == 0:
            plyr.velocity[0] = 0
        # player going vertical direction
        if deltaVert > 0:
            plyr.velocity[1] = abs(plyr.speed[1])
        elif deltaVert < 0:
            plyr.velocity[1] = -(abs(plyr.speed[1]))
        elif deltaVert == 0:
            plyr.velocity[1] = 0

        # making horiz and vert positive so velocity determines direction,
        # (velocity is used elsewhere in program)
        # making sure player only either goes vertically or horizontally, not both
        if deltaHoriz:
            plyr.rect.x += plyr.velocity[0]
        elif deltaVert:
            plyr.rect.y += plyr.velocity[1]

        # restrict player's x and y coordinates to edge of window
        if plyr.rect.x < 0:
            plyr.rect.x = 0
        elif plyr.rect.x + plyr.rect.width > window.width:
            plyr.rect.x = window.width - plyr.rect.width
        if plyr.rect.y < 0:
            plyr.rect.y = 0
        elif plyr.rect.y + plyr.rect.height > window.height:
            plyr.rect.y = window.height - plyr.rect.height


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
                    plyrBullet = Bullet(plyr.bulletImage, size=[10, 10], velocity=[10, 0], startingPos=(plyr.rect.centerx, plyr.rect.bottom))
                    plyrBullet.InitVelocity(plyr.velocity, plyr.flipSprite)
                    plyr.bullets.append(plyrBullet)
                    # activate the animation for shooting
                    plyr.animsDirList[2].isActive = True


        for char in charList:
            for charDir in char.animsDirList:
                # sort the list into alphabetical order
                charDir.animFramesList.sort()

                try:
                    # if animation is active
                    if (charDir.isActive == True) and charDir != "Images/playersprites/idle":

                        char.image = pygame.image.load(charDir.animFramesList[charDir.plyrAnimIdx]).convert_alpha()
                        char.rect = char.image.get_rect(x=char.rect.x, y=char.rect.y)
                        char.rect.size = (int(char.rect.width * char.scaleFactor), int(char.rect.height * char.scaleFactor))

                        char.image = pygame.transform.flip(
                            pygame.transform.scale(char.image, char.rect.size), char.flipSprite, False).convert_alpha()

                    else:
                        char.image = pygame.image.load(char.animsDirList[0].animFramesList[charDir.plyrAnimIdx]).convert_alpha()
                        char.rect = char.image.get_rect(x=char.rect.x, y=char.rect.y)
                        char.rect.size = (int(char.rect.width * char.scaleFactor), int(char.rect.height * char.scaleFactor))

                        char.image = pygame.transform.flip(
                            pygame.transform.scale(char.image, char.rect.size), char.flipSprite, False).convert_alpha()

                    charDir.plyrAnimIdx += 1
                except IndexError:
                    # loop back to 0 index after all animations have been looped
                    charDir.plyrAnimIdx = 0

                if charDir.maxCycles == -1:
                    charDir.maxCycles == -2
                    break

                if charDir.currentCycles == charDir.maxCycles:
                    charDir.isActive = False

                charDir.currentCycles += 1

        # updating all visible plyr bullets on screen
        for bullet in plyr.bullets:
            # deleting plyr bullets that travel off screen
            if bullet.rect.x < 0 or bullet.rect.x > window.width or bullet.rect.y < 0 or bullet.rect.y > window.height:
                plyr.bullets.remove(bullet)
            
            # updating bullet rect
            bullet.rect.x += bullet.velocity[0]
            bullet.rect.y += bullet.velocity[1]

            characterSpriteGroup.add(bullet)


        # enemy movement
        enemy.rect.x += enemy.velocity[0]

        if enemy.rect.x < 0 or enemy.rect.x + enemy.rect.width > window.width or enemy.rect.y < 0 or enemy.rect.y + enemy.rect.height > window.height:
            enemy.velocity[0] = -enemy.velocity[0]
                

        # drawing surfaces onto screen
        window.screen.blit(window.bg, (0, 0))

        characterSpriteGroup.update()
        characterSpriteGroup.draw(window.screen)

        

        # updating screen
        pygame.display.update()


    return
     




    
