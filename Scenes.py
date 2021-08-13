import pygame
import random
import shutil
import os
from re import search
import math

from Animations import Animation
from Sprites import Human
from Sprites import Bullet
import GUI

try:
    pygame.mixer.init()
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1)
except NotImplementedError:
    pass


# Tutorial Scene
def Tutorial(window, charList, layersDict):

    plyr = charList[0]
    enemy = charList[1]

    characterSpriteGroup = pygame.sprite.Group()
    characterSpriteGroup.add(plyr)

    GUISpriteGroup = pygame.sprite.Group()

    has_moved = False
    has_shot = False

    mouseVisibility = False

    pauseMenuBgColour = (200, 200, 200)

    while True:

        clock = pygame.time.Clock()
        clock.tick(window.frameRate)

        # mouse visibility during the game
        pygame.mouse.set_visible(mouseVisibility)

        curTime = pygame.time.get_ticks()

        # getting state of all keys
        keys = pygame.key.get_pressed()

        # keys[pygame.(any key)] is always either 0 (if not being pressed) or 1 (if being pressed); boolean value
        plyr_deltaVert = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        plyr_deltaHoriz = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]


        for event in pygame.event.get():
            # quitting the screen
            if event.type == pygame.QUIT:
                # exits loop
                return "Quit"

            # if player hits escape, mouse is unhidden and player can move their input outside of the window;
            # if player hits mouse down, mouse is hidden and external input is once again hidden,
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mouseVisibility = True

                # shoot bullet when space pressed
                if (
                    event.key == pygame.K_SPACE
                    and (curTime - plyr.bullet.timeSinceLastCall >= plyr.bullet.cooldown)
                    and has_moved
                ):
                    if has_shot is False:
                        has_shot = True
                    plyr.bullet = Bullet(plyr.bulletImage, [30, 15], [15, 0], (plyr.rect.centerx, plyr.rect.bottom), 200, window)
                    plyr.bullet.InitVelocity(plyr.velocity, plyr.flipSprite)
                    plyr.bullets.append(plyr.bullet)

                    plyr.bullet.timeSinceLastCall = curTime

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouseVisibility == True:
                    mouseVisibility = False

                # Settings

                if layersDict["pauseLogo"].IsLayerClicked() == True and layersDict["pauseLogo"].is_active:
                    # pause surface
                    window.layers.append(pygame.Surface((250, 325)))
                    # get the most recently added layer and fill it
                    window.layers[-1].fill((pauseMenuBgColour))
                    mouseVisibility = True
                    layersDict["pauseText"].is_active = True
                    layersDict["homeLogo"].is_active = True
                    layersDict["resumeLogo"].is_active = True
                    layersDict["quitLogo"].is_active = True
                    # pause the game

                # returns back to homepage
                elif layersDict["homeLogo"].IsLayerClicked() == True and layersDict["homeLogo"].is_active:
                    return "Home"

                # quits the game
                elif layersDict["quitLogo"].IsLayerClicked() == True and layersDict["quitLogo"].is_active:
                    return "Quit"

                # resumes the game
                elif layersDict["resumeLogo"].IsLayerClicked() == True and layersDict["resumeLogo"].is_active:
                    window.layers.pop(len(window.layers) - 1)
                    mouseVisibility = False
                    layersDict["pauseText"].is_active = False
                    layersDict["homeLogo"].is_active = False
                    layersDict["resumeLogo"].is_active = False
                    layersDict["quitLogo"].is_active = False

                    layersDict["aimText"].is_active = True
                    layersDict["movementText"].is_active = True
                    layersDict["shootText"].is_active = True
                    layersDict["skipLogo"].is_active = True

                
                elif layersDict["skipLogo"].IsLayerClicked() == True and layersDict["skipLogo"].is_active:
                    return "Skip"


        # Movement

        # assigning the direction to the player's velocity
        # plyr_deltaHoriz and plyr_deltaVert are either 1, 0, -1, which assigns direction correctly
        plyr.velocity[0] = plyr_deltaHoriz * plyr.speed[0]
        plyr.velocity[1] = plyr_deltaVert * plyr.speed[1]
        # diagonal velocity is to keep the player from travelling quicker
        # than the normal horizontal and vertical speeds (pythagoras' theorem)
        # --> see Character class for more on diagonal velocity
        plyr.diagonalVelocity[0] = plyr_deltaHoriz * plyr.diagonalSpeed[0]
        plyr.diagonalVelocity[1] = plyr_deltaVert * plyr.diagonalSpeed[1]

        # if the player is going diagonally, assign the diagonal speed
        if 0 not in (plyr_deltaHoriz, plyr_deltaVert):
            plyr.velocity = plyr.diagonalVelocity

        # Restrictions

        if plyr.rect.x < 0:
            plyr.rect.x = 0
        elif plyr.rect.x + plyr.rect.width > window.width:
            plyr.rect.x = window.width - plyr.rect.width

        # upper boundaries are enemy location
        if plyr.rect.y < enemy.rect.height + enemy.rect.y + 10:
            plyr.rect.y = enemy.rect.height + enemy.rect.y + 10
        # if the player is not dead, then the lower boundary is the human location
        if (
            plyr.health > 0
            and (plyr.rect.y + plyr.rect.height > 500 * (window.height / 720))
        ):
            plyr.rect.y = 500 * (window.height / 720) - plyr.rect.height
        # else if the player has died, then they fall through the floor


        # variable changes if the player has moved for the first time in the game
        if (plyr.velocity[0] > 0 or plyr.velocity[1] > 0) and has_moved == False:
            has_moved = True
        
        if plyr.velocity[0] < 0:
            plyr.flipSprite = True
        elif plyr.velocity[0] > 0:
            plyr.flipSprite = False

        # add the velocity to the player's position
        plyr.rect.x += plyr.velocity[0]
        plyr.rect.y += plyr.velocity[1]

        if enemy.rect.x < 0 or enemy.rect.x + enemy.rect.width > window.width:
            enemy.velocity[0] = -enemy.velocity[0]
        if enemy.rect.y < 0 or enemy.rect.y + enemy.rect.height > window.height:
            enemy.velocity[1] = -enemy.velocity[1]

        

        enemy.rect.x += enemy.velocity[0]


        # Bullets:
        # updating all visible plyr bullets on screen
        for bullet in plyr.bullets:
            # deleting plyr bullets that travel off screen
            if bullet.rect.x + 5 < 0 or bullet.rect.x > window.width or bullet.rect.y < 0 or bullet.rect.y > window.height:
                plyr.bullets.remove(bullet)

            # updating bullet rect
            bullet.rect.x += bullet.velocity[0]
            bullet.rect.y += bullet.velocity[1]

            characterSpriteGroup.add(bullet)

        # Animation Logic:

        for char in charList:

                # if the cooldown for the animation has been reached
                if (curTime - char.anim.timeSinceLastCall >= char.anim.cooldown):
                    try:
                        # deactivate the animation if the maximum number of cycles has been reached
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

        
        
        # drawing background
        window.screen.blit(window.bg, (0, 0))


        if has_moved:
            # commence the next message
            layersDict["aimText"].is_active = True
            layersDict["movementText"].is_active = True
            layersDict["shootText"].is_active = True
            layersDict["skipLogo"].is_active = True

            characterSpriteGroup.add(enemy)
            enemy.anim = enemy.animsDirList[0]

            if has_shot:
                layersDict["enemyText"].is_active = True
                layersDict["lastText"].is_active = True

        # for all of windows layers activated, activate its corresponding buttons
        for windowLayer in window.layers:
            for layerRef in layersDict:
                layersDict[layerRef].is_active = False
            
            layersDict["pauseText"].is_active = True
            layersDict["homeLogo"].is_active = True
            layersDict["resumeLogo"].is_active = True
            layersDict["quitLogo"].is_active = True

            # settings window 
            window.screen.blit(windowLayer, (window.width/2 - windowLayer.get_width()/2, window.height/2 - windowLayer.get_height()/2, 300, 300))

        
        # update layers within scene
        for layerRef in layersDict:
            layer = layersDict[layerRef]
            if layer.is_active:
                layer.Main()
                for windowLayer in window.layers:
                    layersDict["pauseText"].Surface_Renderer(windowLayer, (int(window.width/2 - windowLayer.get_width()/2), int(window.height/2 - windowLayer.get_height()/2)))
                GUISpriteGroup.add(layer)
            elif layer.is_active == False:
                GUISpriteGroup.remove(layer)

        # drawing all GUI sprites onto screen
        GUISpriteGroup.update()
        GUISpriteGroup.draw(window.screen)

        # drawing all sprite groups
        characterSpriteGroup.update()
        characterSpriteGroup.draw(window.screen)

        # updating screen
        pygame.display.update()



# Menu Scene
def TitleScreen(window, layersDict, programState=""):

    if programState != "":
        layersDict[programState] = GUI.Layer([window.width/2, window.height/4], window, text=programState, textFontLocation="Fonts/titlefont.ttf", textFontSize=100, textColour=(255, 255, 255))

    GUISpriteGroup = pygame.sprite.Group()

    while True:
        # framerate
        clock = pygame.time.Clock()
        clock.tick(window.frameRate)

        # mouse visibility during the game
        pygame.mouse.set_visible(True)

        # background
        window.screen.blit(window.bg, (0, 0))

        # for each reference to the layer in the layer dictionary...
        for layerRef in layersDict:
            layer = layersDict[layerRef]
            layer.Main()
            GUISpriteGroup.add(layer)
         
        # events (key presses, mouse presses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"  # exits loop   

            # checks if mouse clicks layers
            if event.type == pygame.MOUSEBUTTONDOWN:
                # loops through all layers within the scene
                for layerRef in layersDict:
                    layer = layersDict[layerRef]
                    # condition for mouse click on layers
                    if layer.IsLayerClicked() == True:
                        # exits loop and returns the name of the layer clicked
                        GUISpriteGroup.empty()
                        return layer.text            
        
        GUISpriteGroup.draw(window.screen)
        pygame.display.update()



# Game Scene
def Game(window, layersDict, charList):
    
    # INITIALISATIONS
    plyr = charList[0]
    enemy = charList[1]

    mouseVisibility = False


    is_dogfight_activated = False
    dogfight = False
    returnfromdogfight = False
    dogfightTimer = 60

    gameState = "Playing"


    pauseMenuBgColour = (200, 200, 200)

    # HUMANS 
    # -------------------------------------------------------------------------------------------------------

    # converting it into an immutable and back to a list so program passes by value 
    humans = list(charList)
    humans.remove(plyr)
    humans.remove(enemy)    

    # instantiating all humans
    for character in charList:
        if character in humans:
            character.Main(window)

    # temp variable   
    # contains: man1, man2, girl1, girl2
    _humans = list(humans)

    no_of_instances = 0
    i = 0

    for _human in _humans:
           
        # counts how many times each human character appears within the "Images/people/" folder 
        for dirs in os.listdir("Images/people/"):
            if search(_human.name, "Images/people/" + dirs):
                no_of_instances += 1

        # if the number of characters are over what is intended
        # then remove the duplicates
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
 

    # generate Human Sprites off the copies that were generated above
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
    for human in humans:
        charList.append(human)


    # spreading all the humans equal distant apart from one another
    for i in range(len(humans)):
        equalSegments = window.width / len(humans)
        humans[i].rect.x = i * equalSegments

    # -------------------------------------------------------------------------------------------------------


    characterSpriteGroup = pygame.sprite.Group()
    characterSpriteGroup.add(character for character in charList)

    GUISpriteGroup = pygame.sprite.Group()

    
    # GAME MAIN LOOP
    # ----------------------------------------------------------------------------
    while True:


        # GAME FUNCTIONS 
        # ---------------------------------------------------------

        def InitAnim(char, anim):
            char.anim = anim
            # reset the cycles of the animation whenever it is called
            char.anim.currentCycles = 0
            char.anim.idx = 0

        def Pause(charList):
            for char in charList:
                char.anim.currentCycles = int(char.anim.maxCycles)
                char.is_moving = False
                if char in humans:
                    char.is_moving = False
                char.speed = list((char.velocity))
                char.velocity = [0, 0]
            return "Paused"

        def Play(charList):
            for char in charList:
                char.anim.currentCycles = 0
                if char in humans:
                    char.is_moving = True
                char.velocity = list((char.speed))
                char.speed = [abs(char.speed[0]), abs(char.speed[1])]
            return "Playing"

        # ---------------------------------------------------------
        

        # TIME
        # ---------------------------------------------------------

        # framerate
        clock = pygame.time.Clock()
        clock.tick(window.frameRate)
        # gets the time since start of Python in milliseconds
        curTime = pygame.time.get_ticks()        

        # ---------------------------------------------------------
        
        

        # PLAYER AND ENEMY
        # ------------------------------------------------------------------------------------------------------------------

        plyrColEnemy = plyr.rect.colliderect(enemy.rect)
        if plyrColEnemy and plyr.health > 0:
            InitAnim(plyr, plyr.animsDirList[1])
            InitAnim(enemy, enemy.animsDirList[1])
            plyr.health -= 1
            enemy.health -= 1

        # ------------------------------------------------------------------------------------------------------------------



        # PLAYER
        # -----------------------------------------------------------------------------------------------

        # Processing Player Input

        # if game is paused, do not get any input from player
        if gameState == "Playing":
            # getting state of all keys
            keys = pygame.key.get_pressed()

            # keys[pygame.(any key)] is always either 0 (if not being pressed) or 1 (if being pressed); boolean value
            plyr_deltaVert = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            plyr_deltaHoriz = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]

        else:
            plyr_deltaVert = 0
            plyr_deltaHoriz = 0

        for event in pygame.event.get():
            # quitting the screen
            if event.type == pygame.QUIT:
                # exits loop
                return "Quit"

            # if player hits escape, mouse is unhidden and player can move their input outside of the window;
            # if player hits mouse down, mouse is hidden and external input is once again hidden,
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mouseVisibility = True
                

                # shoot bullet when space pressed
                if (
                    event.key == pygame.K_SPACE
                    and (curTime - plyr.bullet.timeSinceLastCall >= plyr.bullet.cooldown)
                ):
                    plyr.bullet = Bullet(plyr.bulletImage, [30, 15], [15, 0], (plyr.rect.centerx, plyr.rect.bottom), 400, window)
                    plyr.bullet.InitVelocity(plyr.velocity, plyr.flipSprite)
                    plyr.bullets.append(plyr.bullet)

                    plyr.bullet.timeSinceLastCall = curTime

                    # initialises the animation
                    InitAnim(plyr, plyr.animsDirList[2])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (mouseVisibility == True): 
                    mouseVisibility = False

                # Settings

                if layersDict["pauseLogo"].IsLayerClicked() == True and layersDict["pauseLogo"].is_active and gameState == "Playing":
                    # pause surface
                    window.layers.append(pygame.Surface((250, 325)))
                    settingsLyr = window.layers[-1]
                    settingsLyr.fill(pauseMenuBgColour)
                    # get the most recently added layer and fill it
                    window.layers[-1].fill(pauseMenuBgColour)
                    mouseVisibility = True
                    layersDict["pauseText"].is_active = True
                    layersDict["homeLogo"].is_active = True
                    layersDict["resumeLogo"].is_active = True
                    layersDict["quitLogo"].is_active = True
                    # pause the game
                    gameState = Pause(charList)
                             
                # returns back to homepage
                elif layersDict["homeLogo"].IsLayerClicked() == True and layersDict["homeLogo"].is_active and gameState == "Paused":
                    return "Home"

                # quits the game
                elif layersDict["quitLogo"].IsLayerClicked() == True and layersDict["quitLogo"].is_active and gameState == "Paused":
                    return "Quit"

                # resumes the game
                elif layersDict["resumeLogo"].IsLayerClicked() == True and layersDict["resumeLogo"].is_active and gameState == "Paused":
                    window.layers.pop(len(window.layers) - 1)
                    mouseVisibility = False
                    layersDict["pauseText"].is_active = False
                    layersDict["homeLogo"].is_active = False
                    layersDict["resumeLogo"].is_active = False
                    layersDict["quitLogo"].is_active = False
                    gameState = Play(charList)


        # Velocity

        # assigning the direction to the player's velocity
        # plyr_deltaHoriz and plyr_deltaVert are either 1, 0, -1, which assigns direction correctly        
        plyr.velocity[0] = plyr_deltaHoriz * plyr.speed[0]
        plyr.velocity[1] = plyr_deltaVert * plyr.speed[1]
        # diagonal velocity is to keep the player from travelling quicker 
        # than the normal horizontal and vertical speeds (pythagoras' theorem)
        # --> see Character class for more on diagonal velocity
        plyr.diagonalVelocity[0] = plyr_deltaHoriz * plyr.diagonalSpeed[0] 
        plyr.diagonalVelocity[1] = plyr_deltaVert * plyr.diagonalSpeed[1]
        # if player is going left, flip sprite

        # if the player is going diagonally, assign the diagonal speed
        if 0 not in (plyr_deltaHoriz, plyr_deltaVert):
            plyr.velocity = plyr.diagonalVelocity

        if plyr.velocity[0] < 0:
            plyr.flipSprite = True
        elif plyr.velocity[0] > 0:
            plyr.flipSprite = False


        # Restrictions

        if plyr.rect.x < 0:
            plyr.rect.x = 0
        elif plyr.rect.x + plyr.rect.width > window.width:
            plyr.rect.x = window.width - plyr.rect.width
        
        # if dogfight hasn't begun, then the upper boundaries are enemy location
        if dogfight == False and is_dogfight_activated == False:
            if plyr.rect.y < enemy.rect.height + enemy.rect.y + 40:
                plyr.rect.y = enemy.rect.height + enemy.rect.y + 40
        # else (if the dogfight has begun) then there are no upper boundaries
        else:
            if plyr.rect.y < 0:
                plyr.rect.y = 0
        # if the player is not dead, then the lower boundary is the human location
        if (
            plyr.health > 0
            and (plyr.rect.y + plyr.rect.height > 500 * (window.height / 720))
        ):
            plyr.rect.y = 500 * (window.height / 720) - plyr.rect.height
        # else if the player has died, then they fall through the floor


        # if the player has fallen through the floor, and the player's dead...
        if plyr.rect.y > window.height and plyr.health <= 0:
            return "You Died"


        # add the velocity to the player's position
        plyr.rect.x += plyr.velocity[0]
        plyr.rect.y += plyr.velocity[1]


        # Bullets

        bulletColEnemy = False
        # updating all visible plyr bullets on screen
        for bullet in plyr.bullets:
            if gameState == "Playing":
                # deleting plyr bullets that travel off screen
                if bullet.rect.x + 5 < 0 or bullet.rect.x > window.width or bullet.rect.y < 0 or bullet.rect.y > window.height:
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
                    enemy.health -= 1
                    break
                
                for e_bullet in enemy.bullets:
                    bulletColBullet = bullet.rect.colliderect(e_bullet.rect)
                    if bulletColBullet:
                        plyr.bullets.remove(bullet)
                        characterSpriteGroup.remove(bullet)
                        enemy.bullets.remove(e_bullet)
                        characterSpriteGroup.remove(e_bullet)
                        if dogfight == True:
                            dogfightTimer += 1


        # Player Health Bar

        r = min(255, 255 - (255 * ((2 * plyr.health - plyr.max_health) / plyr.max_health)))
        g = min(255, 255 * (plyr.health / (plyr.max_health / 2)))
        color = (r, g, 0)
        width = int(plyr.rect.width * plyr.health / plyr.max_health)
        plyr.health_bar = pygame.Rect(0, 0, width, 7)
        pygame.draw.rect(plyr.image, color, plyr.health_bar)


        # Player Death Condition
        if plyr.health == 0:
            InitAnim(plyr, plyr.animsDirList[3])
            gameState = Pause(charList)

            for p_bullet in plyr.bullets:
                bullet.velocity[0] = 0
                characterSpriteGroup.remove(p_bullet)

            for e_bullet in enemy.bullets:
                characterSpriteGroup.remove(e_bullet)
            plyr.speed = [0, 0]
            plyr.diagonalSpeed = [0, 0]
            plyr.rect.y += 10
            

        # -----------------------------------------------------------------------------------------------



        # ENEMY
        # ----------------------------------------------------------------------------------------------------------------

        # dogfight begins.
        if dogfightTimer == 0:
            is_dogfight_activated = True
        
        # dogfight ends.
        if dogfightTimer == 90:
            is_dogfight_activated = False
            returnfromdogfight = True

        # enemy returning from dogfight
        if returnfromdogfight:
            enemy.rect.y += 8

        # enemy travelling to dogfight position
        if enemy.rect.x + enemy.rect.width < (window.width - 15) and is_dogfight_activated:
            enemy.rect.x += 8
        if enemy.rect.y < window.height/2 - enemy.rect.y/2 and is_dogfight_activated:
            enemy.rect.y += 8
        
        # if the enemy has reached the dogfight position..
        if enemy.rect.x + enemy.rect.width > (window.width - 16) and enemy.rect.y > (window.height/2 - enemy.rect.y/2 - 1) and is_dogfight_activated:
            enemy.flipSprite = True
            dogfight = True
            is_dogfight_activated = False

        # vertical and horizontal boundaries for enemy
        if enemy.rect.x < 0 or enemy.rect.x + enemy.rect.width > window.width:
            enemy.velocity[0] = -enemy.velocity[0]
        if enemy.rect.y < 0 or enemy.rect.y + enemy.rect.height > window.height:
            enemy.velocity[1] = -enemy.velocity[1]

        # if the game is in a state of playing (as opposed to paused)
        if gameState == "Playing":

            # if the enemy and player are in the dogfight session and the enemy is ready to shoot
            if (dogfight == True) and (curTime - enemy.bullet.timeSinceLastCall >= enemy.bullet.cooldown):
                vector = math.atan((plyr.rect.y-enemy.rect.y)/(plyr.rect.x-enemy.rect.x))
                velx = 15 * math.cos(vector)
                vely = 15 * math.sin(vector)
                print(vector)
                enemy.bullet = Bullet(enemy.bulletImage, [30, 15], [0-velx, 0-vely], (enemy.rect.centerx, enemy.rect.bottom), 800, window)
                enemy.bullets.append(enemy.bullet)
                InitAnim(enemy, enemy.animsDirList[2])

                enemy.bullet.timeSinceLastCall = curTime

            # if the enemy is not in a dogfight and its not going to be in a dogfight
            elif (dogfight == False) and (is_dogfight_activated == False):
                enemy.rect.x += enemy.velocity[0]

                if (curTime - enemy.bullet.timeSinceLastCall >= enemy.bullet.cooldown):
                    enemy.bullet = Bullet(enemy.bulletImage, [30, 20], [0, 10], (enemy.rect.centerx, enemy.rect.bottom), 800, window)
                    enemy.bullet.rect.size = (int(enemy.bullet.rect.width),int(enemy.bullet.rect.height))
                    enemy.bullets.append(enemy.bullet)
                    InitAnim(enemy, enemy.animsDirList[0])
                    dogfightTimer -= 1

                    enemy.bullet.timeSinceLastCall = curTime

        
        # Bullets
     
        for bullet in enemy.bullets: 
            if gameState == "Playing":
                # deleting enemy bullets that travel off screen
                if bullet.rect.x < 0 or bullet.rect.x > window.width or bullet.rect.y < 0 or bullet.rect.y > window.height:
                    enemy.bullets.remove(bullet)
                    characterSpriteGroup.remove(bullet)

                # updating bullet rect
                bullet.rect.x += bullet.velocity[0]
                bullet.rect.y += bullet.velocity[1]

                characterSpriteGroup.add(bullet)

                bulletColPlyr = bullet.rect.colliderect(plyr.rect)
                if bulletColPlyr:
                    enemy.bullets.remove(bullet)
                    characterSpriteGroup.remove(bullet)
                    InitAnim(plyr, plyr.animsDirList[1])
                    plyr.health -= 1

            for human in humans:
                bulletColHuman = bullet.rect.colliderect(human.rect)
                if bulletColHuman:
                    try:
                        enemy.bullets.remove(bullet)
                        characterSpriteGroup.remove(bullet)
                    except:
                        pass
                    humans.remove(human)
                    characterSpriteGroup.remove(human)


        # Enemy Health Bar

        r = min(255, 255 - (255 * ((2 * enemy.health - enemy.max_health) / enemy.max_health)))
        g = min(255, 255 * (enemy.health / (enemy.max_health / 2)))
        color = (r, g, 0)
        width = int(enemy.rect.width * enemy.health / enemy.max_health)
        enemy.health_bar = pygame.Rect(0, 0, width, 7)
        pygame.draw.rect(enemy.image, color, enemy.health_bar)



        # Enemy Death
        if enemy.health <= 0:
            InitAnim(enemy, enemy.animsDirList[2])
            gameState = Pause(charList)

            for p_bullet in plyr.bullets:
                p_bullet.velocity[0] = 0
                plyr.bullets.remove(p_bullet)
                characterSpriteGroup.remove(p_bullet)

            for e_bullet in enemy.bullets:
                e_bullet.velocity[0] = 0
                enemy.bullets.remove(e_bullet)
                characterSpriteGroup.remove(e_bullet)

            plyr.speed = [0, 0]
            plyr.diagonalSpeed = [0, 0]
            enemy.rect.y -= 10

            if enemy.rect.y + enemy.rect.height < 0:
                return "Victory"



        # ------------------------------------------------------------------------------------------------------------------



        # HUMANS        
        # ---------------------------------------------------------------------------

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
            
            # cooldown for stopping and is_dogfight_activated humans
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
            
        # if all humans die
        if len(humans) == 0:
            return "All Humans Died"


        # ---------------------------------------------------------------------------


        # ALL CHARACTERS
        # -------------------------------------------------------------------------------------------------------

        # for every character present in the game
        for char in charList:
            if gameState == "Playing":
                # adding humans velocities
                if char in humans and char.is_moving:
                    char.rect.x += char.velocity[0]

                # Animation Logic:

                # if the cooldown for the animation has been reached
                if (curTime - char.anim.timeSinceLastCall >= char.anim.cooldown):
                    try:
                        # deactivate the animation if the maximum number of cycles has been reached
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

        # -------------------------------------------------------------------------------------------------------

        # MISCELLANEOUS
        # ---------------------------------------------------------

        # update layers within scene
        for layerRef in layersDict:
            layer = layersDict[layerRef]
            if layer.is_active:
                layer.Main()
                GUISpriteGroup.add(layer)
            elif layer.is_active == False:
                GUISpriteGroup.remove(layer)

        # mouse visibility during the game
        pygame.mouse.set_visible(mouseVisibility)
        # ---------------------------------------------------------

        
        # DRAWING SURFACES
        # ------------------------------------------------------------------

        # drawing background
        window.screen.blit(window.bg, (0, 0))   


        # drawing all sprite groups 
        characterSpriteGroup.update()
        characterSpriteGroup.draw(window.screen)
        
        # drawing pause window
        for layer in window.layers:
            window.screen.blit(layer, (window.width/2 - layer.get_rect().width/2, window.height/2 - layer.get_rect().height/2, 300, 300))

        GUISpriteGroup.draw(window.screen)

        # updating screen
        pygame.display.update()

        # ------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------------


