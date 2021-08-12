import pygame


# custom modules
import Scenes
import GUI
from Sprites import Character, Human
from Animations import Animation

# initalises all pygame processes 
pygame.init()

# declaring variables in the global scope
menuWindow = None
gameWindow = None
menuLayersDict = None
gameLayersDict = None
charList = None
tutorialLayersDict = None
endgameLayersDict = None

def Initialisations():
    global menuWindow, gameWindow, menuLayersDict, gameLayersDict, tutorialLayersDict, endgameLayersDict, charList
    # time
    framerate = 40

    # game properties
    gameTitle = "Invasions"

    menuWindow = GUI.Window(gameTitle, framerate, bg="Images/backgroundsprites/TitleBG.bmp")
    gameWindow = GUI.Window(gameTitle, framerate, bg="Images/backgroundsprites/Background.bmp")

    # instances of custom text class
    titleLayerText = GUI.LayerRenderer(text="Invasions", textFontLocation="Fonts/titlefont.ttf", textFontSize=150, textColour=(255, 255, 255))
    startLayerText = GUI.LayerRenderer(text="Start", textFontLocation="Fonts/gasalt-regular.ttf", textFontSize=36, textColour=(0, 0, 0))
    tutorialLayerText = GUI.LayerRenderer(text="Tutorial", textFontLocation="Fonts/gasalt-regular.ttf", textFontSize=36, textColour=(0, 0, 0))
    quitLayerText = GUI.LayerRenderer(text="Quit", textFontLocation="Fonts/gasalt-regular.ttf", textFontSize=36, textColour=(0, 0, 0))

    homeLogoLayer = GUI.LayerRenderer(renderedImage=pygame.transform.scale(pygame.image.load("Images/menusprites/home.bmp"), (30, 30)))



    # dictionary containing instances of custom button class, located on menu window
    menuLayersDict = {
        titleLayerText.originalText:    GUI.Layer(titleLayerText, [menuWindow.width/2, menuWindow.height/4], has_rect=False),

        startLayerText.originalText:    GUI.Layer(startLayerText, [menuWindow.width/3, 2*menuWindow.height/3], 
                                                  clr=(83, 70, 50), hoverClr=(102, 255, 71), is_button=True, has_rect=False),


        tutorialLayerText.originalText: GUI.Layer(tutorialLayerText, [menuWindow.width/2, 2*menuWindow.height/3],
                                                      clr=(83, 70, 50), hoverClr=(102, 255, 71), is_button=True, has_rect=False),

        quitLayerText.originalText:     GUI.Layer(quitLayerText, [2*menuWindow.width/3, 2*menuWindow.height/3], 
                                                  clr=(83, 70, 50), hoverClr=(102, 255, 71), is_button=True, has_rect=False),

        "skipLogo":                     GUI.Layer(homeLogoLayer, [40, 40], is_button=False, is_active=True),

    }


    pauseLayer = GUI.LayerRenderer(renderedImage=pygame.transform.scale(pygame.image.load("Images/menusprites/pause.bmp"), (35, 35)))
    pauseTextLayer = GUI.LayerRenderer(text="Settings", textFontLocation="Fonts/titlefont.ttf", textFontSize=35, textColour=(0, 0, 0))
    homeLayer = GUI.LayerRenderer(renderedImage=pygame.transform.scale(pygame.image.load("Images/menusprites/home.bmp"), (30, 30)))
    backLayer = GUI.LayerRenderer(renderedImage=pygame.transform.scale(pygame.image.load("Images/menusprites/play.bmp"), (30, 30)))
    quitLayer = GUI.LayerRenderer(renderedImage=pygame.transform.scale(pygame.image.load("Images/menusprites/quit.bmp"), (30, 30)))

    gameLayersDict = {
        "pauseLogo": GUI.Layer(pauseLayer, [gameWindow.width - 35, 35], is_button=True),
        "pauseText": GUI.Layer(pauseTextLayer, [gameWindow.width/2, 260], is_active=False),
        "homeLogo": GUI.Layer(homeLayer, [gameWindow.width / 2, 320], is_button=True, is_active=False),
        "quitLogo": GUI.Layer(quitLayer, [gameWindow.width / 2, 395], is_button=True, is_active=False),
        "resumeLogo": GUI.Layer(backLayer, [gameWindow.width / 2, 475], is_button=True, is_active=False),
    }


    skipLogoLayer = GUI.LayerRenderer(renderedImage=pygame.transform.scale(pygame.image.load("Images/menusprites/skip.bmp"), (75, 75)))
    aimMessageLayer = GUI.LayerRenderer(text="To win the game, don't let all the humans die and kill the invader",textFontLocation="Fonts/ferrum.ttf", textFontSize=35, textColour=(0, 0, 0))
    movementMessageLayer = GUI.LayerRenderer(text="Use WASD keys to move your character. Try it now!", textFontLocation="Fonts/ferrum.ttf", textFontSize=35, textColour=(0, 0, 0))
    shootMessageLayer = GUI.LayerRenderer(text="Press SPACE to shoot bullets. Give it a shot!", textFontLocation="Fonts/ferrum.ttf", textFontSize=35, textColour=(0, 0, 0))
    enemyMessageLayer = GUI.LayerRenderer(text="Watch out for the enemy as they come down and shoot at you. Use that chance to destroy the alien invader!", textFontLocation="Fonts/ferrum.ttf", textFontSize=33, textColour=(0, 0, 0))
    lastMessage = GUI.LayerRenderer(text="GOOD LUCK SOLDIER!", textFontLocation="Fonts/ferrum.ttf", textFontSize=50, textColour=(240, 240, 240))


    tutorialLayersDict = {
        "skipLogo": GUI.Layer(skipLogoLayer, [gameWindow.width - 75, gameWindow.height - 100], is_button=True, is_active=True),

        "aimText": GUI.Layer(aimMessageLayer, [gameWindow.width/2, 150], is_active=True),
        "movementText": GUI.Layer(movementMessageLayer, [gameWindow.width/2, 250], is_active=True),
        "shootText": GUI.Layer(shootMessageLayer, [gameWindow.width/2, 350], is_active=False),
        "enemyText": GUI.Layer(enemyMessageLayer, [gameWindow.width/2, 450], is_active=False),
        "lastText": GUI.Layer(lastMessage, [gameWindow.width/2, 550], is_active=False),

        "pauseLogo": GUI.Layer(pauseLayer, [gameWindow.width - 35, 35], is_button=True),
        "pauseText": GUI.Layer(pauseTextLayer, [gameWindow.width/2, 260], is_active=False),
        "homeLogo": GUI.Layer(homeLayer, [gameWindow.width / 2, 320], is_button=True, is_active=False),
        "quitLogo": GUI.Layer(quitLayer, [gameWindow.width / 2, 395], is_button=True, is_active=False),
        "resumeLogo": GUI.Layer(backLayer, [gameWindow.width / 2, 475], is_button=True, is_active=False),
    }

       # instances of custom text class
    homeLayer = GUI.LayerRenderer(renderedImage=pygame.transform.scale(pygame.image.load("Images/menusprites/home.bmp"), (30, 30)))
    backLayer = GUI.LayerRenderer(renderedImage=pygame.transform.scale(pygame.image.load("Images/menusprites/replay.bmp"), (30, 30)))
    quitLayer = GUI.LayerRenderer(renderedImage=pygame.transform.scale(pygame.image.load("Images/menusprites/quit.bmp"), (30, 30)))

    # dictionary containing instances of custom button class, located on menu window
    endgameLayersDict = {
        "homeLogo": GUI.Layer(homeLayer, [45*gameWindow.width/100, 1*gameWindow.height/2], is_button=True, is_active=False),
        "quitLogo": GUI.Layer(quitLayer, [55*gameWindow.width/100, 1*gameWindow.height/2], is_button=True, is_active=False),
    }

    # list of the directories containing PLAYER animation frames 
    plyr_animList = [
        Animation("Images/playersprites/idle", 30, -1),
        Animation("Images/playersprites/hit", 64, 1),
        Animation("Images/playersprites/shooting", 30, 1),
        Animation("Images/playersprites/defeated", 64, -1)
    ]
    enemy_animList = [
        Animation("Images/enemysprites/idle", 64, -1),
        Animation("Images/enemysprites/hit", 64, 1),
        Animation("Images/enemysprites/shooting", 30, 1),
        Animation("Images/enemysprites/defeated", 64, -1)]

    man1_animList = [Animation("Images/people/man1", 100, -1)]
    man2_animList = [Animation("Images/people/man2", 100, -1)]
    woman1_animList = [Animation("Images/people/girl1", 100, -1)]
    woman2_animList = [Animation("Images/people/girl2", 100, -1)]

    # instance of Player class, representing player
    # (player and enemy sizes were configured to 1280x720, so scales changes as window size changes)
    plyr = Character(1/7, [10, 100], [10, 10], plyr_animList, 5, "Images/playersprites/bullet/bullet.bmp", gameWindow)
    enemy = Character(1/8, [1000, 10], [8, 8], enemy_animList, 50, "Images/enemysprites/bullet/enemybullet-1.png.bmp", gameWindow)

    man1 = Human("man1", 1/8, [3, 0], man1_animList, window=gameWindow, health=1, walkTime=1775, waitTime=3000, max_no_of_instances=4)
    man2 = Human("man2", 1/8, [3, 0], man2_animList, window=gameWindow, health=1, walkTime=2222, waitTime=3000, max_no_of_instances=4)
    girl1 = Human("girl1", 1/8, [3, 0],woman1_animList, window=gameWindow, health=1, walkTime=575, waitTime=3000, max_no_of_instances=4)
    girl2 = Human("girl2", 1/8, [3, 0],woman2_animList, window=gameWindow, health=1, walkTime=1828, waitTime=3000, max_no_of_instances=4)

    charList = [plyr, enemy, man1, man2, girl1, girl2]


def Main():
    global menuWindow, gameWindow, menuLayersDict, gameLayersDict, tutorialLayersDict, endgameLayersDict, charList

    menuState = Scenes.TitleScreen(menuWindow, menuLayersDict)

    if menuState == "Start":
        pass

    elif menuState == "Tutorial":

        tutorialState = Scenes.Tutorial(gameWindow, charList, tutorialLayersDict)

        if (tutorialState == "Skip"):
            pass
        else:
            # input from settings: quit or home
            return tutorialState


    elif menuState == "Quit":
        return menuState


    gameState = Scenes.Game(gameWindow, gameLayersDict, charList)

    if gameState == "You Died" or gameState == "All Humans Died" or gameState == "Victory":
        gameState = Scenes.TitleScreen(menuWindow, endgameLayersDict, gameState)

    return gameState
        

if __name__ == "__main__":
    # programs asks for input before
    Initialisations()
    programState = Main()

    # if when running the game, it doesn't request to quit
    # then keep running the game
    while programState != "Quit":
        Initialisations()
        programState = Main()



    # otherwise exit the program
    exit()


