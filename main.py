import pygame

import Scenes
import GUI
from Characters import Player

# initalises all pygame processes 
pygame.init()

# time
framerate = 40

# game properties: external
gameTitle = "Game Title"
gameWindowSize = [1280, 720]

menuWindow = GUI.Window(gameTitle, gameWindowSize, "Images/menu.bmp")
gameWindow = GUI.Window(gameTitle, gameWindowSize, "Images/maxcheng1.bmp")

# instance of Player class, representing player 
plyr = Player((0, 0), [80, 80], 7.5, "Images/playerCharacter.bmp")

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

if __name__ == "__main__":

    menuState = Scenes.Menu(framerate, menuWindow, menuButtons)

    if menuState == "Start":
        # start the game
        Scenes.Game(framerate, gameWindow, plyr)
    elif menuState == "Quit":
        # passes the sequence to quit python
        pass

    exit()
