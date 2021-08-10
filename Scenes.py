import pygame
import random
import shutil
import os
from re import search


from Animations import Animation
from Sprites import Human
from Sprites import Bullet

def Menu(window, buttonDict):
    pygame.display.quit()
    
    window.screen = pygame.display.set_mode((window.size), pygame.FULLSCREEN)
    pygame.display.set_caption(window.title)
    window.bg = pygame.image.load(window.bgFileLocation)

    GUISpriteGroup = pygame.sprite.Group()

    menuState = "True"
    while menuState == "True":
        # framerate
        clock = pygame.time.Clock()
        clock.tick(window.frameRate)
        mouse = pygame.mouse.get_pos()

        # background
        window.screen.blit(window.bg, (0, 0))

        # for each reference to the button in the button dictionary...
        for buttonRef in buttonDict:
            button = buttonDict[buttonRef]
            button.main()
            GUISpriteGroup.add(button)
         
        # events (key presses, mouse presses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuState = ""  # exits loop            

            # loops through all buttons within the scene
            for buttonRef in buttonDict:
                button = buttonDict[buttonRef]
                # checks if mouse clicks buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # condition for mouse click on buttons
                    if button.IsLayerClicked() == True:
                        # exits loop and returns the name of the button
                        GUISpriteGroup.empty()
                        menuState = button.myText.originalText
        
        GUISpriteGroup.draw(window.screen)
        pygame.display.update()
        
    return menuState


def Game(window, charList):
    pygame.display.quit()
    window.screen = pygame.display.set_mode((window.size), pygame.FULLSCREEN)
    pygame.display.set_caption(window.title)
    window.bg = pygame.image.load(window.bgFileLocation)

    # instantiating all instances of the characters within the game
    for character in charList:
        character
    
    # assigning characters
    plyr = charList[0]
    enemy = charList[1]

    # converting it into an immutable and back to a list so program passes by value 
    humans = list(charList)
    humans.remove(plyr)
    humans.remove(enemy)

    # temp variable
    _humans = list(humans)

    no_of_instances = 0
    i = 0
    for _human in _humans:
           
        # counts how many times each human character appears 
        for dirs in os.listdir("Images/people/"):
            if search(_human.name, "Images/people/" + dirs):
                no_of_instances += 1

        # if the number of characters are over what is specified
        # then remove any number of copies
        if no_of_instances > _human.max_no_of_instances:
            for _ in range(no_of_instances - _human.max_no_of_instances):
                shutil.rmtree(f"Images/people/{_human.name} - copy ({no_of_instances - _human.max_no_of_instances - 1})")
                no_of_instances -= 1

        # if the number of characters are under what is specified
        # add more copies of the folders
        elif no_of_instances < _human.max_no_of_instances:
            while i < _human.max_no_of_instances - no_of_instances:
                src = _human.anim.dir
                dest = _human.anim.dir + f" - copy ({i})"                
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                
                try:
                    shutil.copytree(src, dest)
                    i += 1
                except FileExistsError:
                    i += 1
                    dest = _human.anim.dir + f" - copy ({i})"

        # reset counters for next human character iteration
        i = 0
        no_of_instances = 0
 

    # generate humans off the copies that were generated above
    for directory in os.listdir("Images/people/"):
        randomNum = random.randint(1, 3) * 1000
        try:
            humanAnimCopy = [Animation("Images/people/" + directory, 100, -1)]
            humanCopy = Human(directory, 1/8, [3, 0], humanAnimCopy, window=window, health=1, walkTime=1000 + randomNum, waitTime=3000 + randomNum)
            humans.append(humanCopy)
        except NotADirectoryError:
            # some files are not folders, therefore exception
            pass
    

    # adding all the proper human characters to the characters list
    # which is added next to the character sprite group
    for _human in _humans:
        charList.remove(_human)
    for human in humans:
        charList.append(human)


    for i in range(len(humans)):
        equalSegments = window.width / len(humans)
        humans[i].rect.x = i * equalSegments


    mouseVisibility = False
    limit_external_input = True

    starting = False
    dogfight = False

    characterSpriteGroup = pygame.sprite.Group()
    characterSpriteGroup.add(character for character in charList)

    gameState = True
    while gameState:

        # framerate
        clock = pygame.time.Clock()
        clock.tick(window.frameRate)
        # gets the time since start of Python in milliseconds
        curTime = pygame.time.get_ticks()

        # mouse visibility during the game
        pygame.mouse.set_visible(mouseVisibility)
        # limits all user input to pygame environment
        pygame.event.set_grab(limit_external_input)

        # getting state of all keys
        keys = pygame.key.get_pressed()
        # keys[pygame.(any key)] is always either 0 (if not being pressed) or 1 (if being pressed); boolean value
        deltaVert = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        deltaHoriz = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]

        # dogfight begins if B pressed, only for development reasons will be removed in final game.
        if keys[pygame.K_b]:
            starting = True

        if enemy.rect.y < window.height/2 - enemy.rect.y/2 and starting:
            enemy.rect.y += 8
        if enemy.rect.x + enemy.rect.width < (window.width - 15) and starting:
            enemy.rect.x += 8
        if enemy.rect.x + enemy.rect.width > (window.width - 16) and enemy.rect.y > (window.height/2- enemy.rect.y/2 -1) and starting:
            enemy.flipSprite = True
            dogfight = True
            starting = False
            print("arrived")
            
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
        if dogfight == False and starting == False:
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

            # if player hits escape, mouse is unhidden and player can move their input outside of the window;
            # if player hits mouse down, mouse is hidden and external input is once again hidden,
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mouseVisibility = True
                    limit_external_input = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (mouseVisibility == True) and (limit_external_input == False):
                    mouseVisibility = False
                    limit_external_input = True
        
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
            InitAnim(enemy, enemy.animsDirList[2])

            enemy.bullet.timeSinceLastCall = curTime

            InitAnim(plyr, plyr.animsDirList[2])

        if enemy.rect.x < 0 or enemy.rect.x + enemy.rect.width > window.width:
            enemy.velocity[0] = -enemy.velocity[0]
        if enemy.rect.y < 0 or enemy.rect.y + enemy.rect.height > window.height:
            enemy.velocity[1] = -enemy.velocity[1]

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



        # human walking animation logic
        for human in humans:
            # boundary restrictions
            # if humans hit left border...
            if human.rect.x - 10 < 0:
                human.velocity[0] = abs(human.speed[0])
                human.flipSprite = False
            # if humans hit right border
            elif (human.rect.x + human.rect.width + 10) > window.width:
                human.velocity[0] = -human.speed[0]
                human.flipSprite = True
            
            # cooldown for stopping and starting humans
            while ((pygame.time.get_ticks() - human.timeSinceLastCall) <= human.walkTime):
                human.anim.cooldown = human.anim.tempCooldown
                if human.flipSprite:
                    human.velocity = [-human.speed[0], 0]
                else:
                    human.velocity = [abs(human.speed[0]), 0]
                break
            else:
                if ((pygame.time.get_ticks() - human.timeSinceLastCall) >= (human.waitTime)):
                    human.timeSinceLastCall = pygame.time.get_ticks()
                
                human.velocity[0] = 0



        # for every character present in the game
        for char in charList:
        
            # adding humans velocities, after manipulation above
            if char in humans:
                char.rect.x += char.velocity[0]

            # animation logic:

            # if the current time minus the time since the last animation was played is greater than the cooldown...
            # for animation frame time control
            if (curTime - char.anim.timeSinceLastCall >= char.anim.cooldown):
                try:
                    # deactivate animation if the maximum number of cycles has been reached
                    while char.anim.currentCycles != char.anim.maxCycles:

                        # update player rect
                        char.image = pygame.image.load(char.anim.framesList[char.anim.idx])
                        char.rect = char.image.get_rect(x=char.rect.x, y=char.rect.y)
                        char.rect.size = (int(char.rect.width * char.scaleFactor), int(char.rect.height * char.scaleFactor))

                        if char in humans:
                            if char.velocity[0] == 0:
                                # setting the time for each frame to the time taken for humans to exit zero velocity,
                                # essentially freezing the frame for the humans animation when they're still
                                char.anim.cooldown = char.waitTime
                            elif char.velocity[0] < 0:
                                char.flipSprite = True
                            elif char.velocity[0] > 0:
                                char.flipSprite = False 
                        
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
        if dogfight == False and starting == False:
            enemy.rect.x += enemy.velocity[0]

            if curTime - enemy.bullet.timeSinceLastCall >= enemy.bullet.cooldown:
                enemy.bullet = Bullet(enemy.bulletImage, [20, 10], [10, 0], (enemy.rect.centerx, enemy.rect.bottom), 400)
                enemy.bullet.InitVelocity(enemy.velocity, enemy.flipSprite)
                enemy.bullets.append(enemy.bullet)
                InitAnim(enemy, enemy.animsDirList[2])

                enemy.bullet.timeSinceLastCall = curTime

                InitAnim(plyr, plyr.animsDirList[2])

        
        # drawing surfaces onto screen
        window.screen.blit(window.bg, (0, 0))


        if enemy.health == 0:
            InitAnim(enemy, enemy.animsDirList[2])

            for p_bullet in plyr.bullets:
                p_bullet.velocity[0] = 0
                characterSpriteGroup.remove(p_bullet)

            for e_bullet in enemy.bullets:
                characterSpriteGroup.remove(e_bullet)
                
            plyr.speed = [0, 0]
            plyr.diagonalSpeed = [0, 0]
            enemy.rect.y -= 10

        if plyr.health == 0:
            InitAnim(plyr, plyr.animsDirList[3])

            for p_bullet in plyr.bullets:
                bullet.velocity[0] = 0
                characterSpriteGroup.remove(p_bullet)
            
            for e_bullet in enemy.bullets:
                characterSpriteGroup.remove(e_bullet)
            plyr.speed = [0, 0]
            plyr.diagonalSpeed = [0, 0]
            plyr.rect.y += 10     


        characterSpriteGroup.update()
        characterSpriteGroup.draw(window.screen)


        enemy.DrawHealth()

        # updating screen
        pygame.display.update()


    return
