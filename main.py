import pygame

import Scenes
import GUI
from Sprites import Character
from Animations import Animation

# initalises all pygame processes 
pygame.init()

# time
framerate = 40

# game properties: external
gameTitle = "Game Title"
gameWindowSize = [1280, 720]

menuWindow = GUI.Window(gameTitle, gameWindowSize, framerate, "Images/backgroundsprites/Background.bmp")
gameWindow = GUI.Window(gameTitle, gameWindowSize, framerate, "Images/backgroundsprites/Background.bmp")

# instances of custom text class
titleText = GUI.Text("Max Cheng Is God", "Fonts/titlefont.ttf", 35, (255, 255, 255))
startText = GUI.Text("Start", "Fonts/titlefont.ttf", 24, (0, 0, 0))
quitText = GUI.Text("Quit", "Fonts/titlefont.ttf", 24, (0, 0, 0))

# dictionary containing instances of custom button class, located on menu window
menuButtons = {
    titleText.originalText: 
        GUI.Button(titleText, (0, 0, 0), (0, 0, 0), 
        [menuWindow.width/2, menuWindow.height/3], menuWindow,
        # doesn't treat title rect as rect surface
        is_rect=False),

    startText.originalText: 
        GUI.Button(startText, (170, 170, 170), (100, 100, 100), 
        [menuWindow.width/2, menuWindow.height/2], menuWindow),

    quitText.originalText: 
        GUI.Button(quitText, (170, 170, 170), (100, 100, 100), 
        [menuWindow.width/2, 2*menuWindow.height/3], menuWindow)
}

# list of the directories containing PLAYER animation frames 
plyr_animList = [
    Animation("Images/playersprites/idle", 0.5, -1),
    Animation("Images/playersprites/hit", 0, 1),
    Animation("Images/playersprites/pre-shooting", 0.15, 10),
    Animation("Images/playersprites/shooting", 0, -1)
]

# instance of Player class, representing player
plyr = Character([100, 100], 7.5, plyr_animList, "Images/playersprites/bullet/bullet.bmp")

if __name__ == "__main__":

    menuState = Scenes.Menu(menuWindow, menuButtons)

    if menuState == "Start":
        # start the game
        Scenes.Game(gameWindow, plyr)
    elif menuState == "Quit":
        # passes the sequence to quit python
        pass

    exit()
