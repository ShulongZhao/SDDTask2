import pygame

import Scenes
import GUI
from Sprites import Character
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
    Animation("Images/playersprites/idle", 0.5, -1),
    Animation("Images/playersprites/hit", 0, 1),
    Animation("Images/playersprites/pre-shooting", 0.15, 10),
    Animation("Images/playersprites/shooting", 0, -1)
]

enemy_animList = [
    Animation("Images/enemysprites/idle", 0, -1),
]

# instance of Player class, representing player
plyr = Character(1/8, [10, 100], (7.5, 7.5), plyr_animList, "Images/playersprites/bullet/bullet.bmp")
enemy = Character(1/8, [1280, 10],(8, 8), enemy_animList, "Images/enemysprites/bullet/enemybullet-1.png.bmp")

if __name__ == "__main__":

    menuState = Scenes.Menu(menuWindow, menuButtonsDict)

    if menuState == "Start":
        # start the game
        Scenes.Game(gameWindow, plyr, enemy)
    elif menuState == "Quit":
        # passes the sequence to quit python
        pass

    exit()
