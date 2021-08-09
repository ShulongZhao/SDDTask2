import pygame

# custom modules
import Scenes
import GUI
from Sprites import Character, Human
from Animations import Animation

# initalises all pygame processes 
pygame.init()

# time
framerate = 40

# game properties
gameTitle = "Game Title"
gameWindowSize = [1280, 720]

menuWindow = GUI.Window(gameTitle, gameWindowSize, framerate, "Images/backgroundsprites/Background.bmp")
gameWindow = GUI.Window(gameTitle, gameWindowSize, framerate, "Images/backgroundsprites/Background.bmp")

# instances of custom text class
titleLayerText = GUI.Text("Max Cheng Is God", "Fonts/titlefont.ttf", 35, (255, 255, 255))
startLayerText = GUI.Text("Start", "Fonts/titlefont.ttf", 24, (0, 0, 0))
quitLayerText = GUI.Text("Quit", "Fonts/titlefont.ttf", 24, (0, 0, 0))

# dictionary containing instances of custom button class, located on menu window
menuButtonsDict = {
    titleLayerText.originalText:    GUI.Layer(titleLayerText, [menuWindow.width/2, menuWindow.height/3], menuWindow),

    startLayerText.originalText:    GUI.Layer(startLayerText, [menuWindow.width/2, menuWindow.height/2], menuWindow, 
                                    clr=(170, 170, 170), hoverClr=(100, 100, 100), is_button=True),

    quitLayerText.originalText:     GUI.Layer(quitLayerText, [menuWindow.width/2, 2*menuWindow.height/3], menuWindow, 
                                    clr=(170, 170, 170), hoverClr=(100, 100, 100), is_button=True),
}

# list of the directories containing PLAYER animation frames 
plyr_animList = [
    Animation("Images/playersprites/idle", 30, -1),
    Animation("Images/playersprites/hit", 64, 1),
    Animation("Images/playersprites/shooting", 30, -1),
    Animation("Images/playersprites/defeated", 64, -1)
]
enemy_animList = [
    Animation("Images/enemysprites/idle", 64, -1),
    Animation("Images/enemysprites/hit", 64, 1),
    Animation("Images/enemysprites/shooting", 30, -1),
    Animation("Images/enemysprites/defeated", 64, -1)]

man1_animList = [Animation("Images/people/man1", 100, -1)]
man2_animList = [Animation("Images/people/man2", 100, -1)]
woman1_animList = [Animation("Images/people/girl1", 100, -1)]
woman2_animList = [Animation("Images/people/girl2", 100, -1)]

# instance of Player class, representing player
plyr = Character(1/7, [10, 100], [7.5, 7.5], plyr_animList, 3, "Images/playersprites/bullet/bullet.bmp")
enemy = Character(1/8, [1000, 10],[8, 8], enemy_animList, 50, "Images/enemysprites/bullet/enemybullet-1.png.bmp")

man1 = Human("man1", 1/8, [3, 0], man1_animList, window=gameWindow, health=1, walkTime=1775, waitTime=3000, max_no_of_instances=4)
man2 = Human("man2", 1/8, [3, 0], man2_animList, window=gameWindow, health=1, walkTime=2222, waitTime=3000, max_no_of_instances=4)
girl1 = Human("girl1", 1/8, [3, 0], woman1_animList, window=gameWindow, health=1, walkTime=575, waitTime=3000, max_no_of_instances=4)
girl2 = Human("girl2", 1/8, [3, 0], woman2_animList, window=gameWindow, health=1, walkTime=1828, waitTime=3000, max_no_of_instances=4)

charList = [plyr, enemy, man1, man2, girl1, girl2]

if __name__ == "__main__":

    menuState = Scenes.Menu(menuWindow, menuButtonsDict)

    if menuState == "Start":
        # start the game
        Scenes.Game(gameWindow, charList)
    elif menuState == "Quit":
        # passes the sequence to quit python    
        pass
    
    exit()
