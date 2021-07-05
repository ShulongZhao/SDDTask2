from typing import Sized
import pygame

import menu
import game
import GUI

# initalises all pygame processes 
pygame.init()


# time
clock = pygame.time.Clock()
framerate = 40


# stores the (x,y) coordinates as a tuple
mouse = pygame.mouse.get_pos()


window = {
    "size": [1280, 720],
    "display": None,
    # window backgrounds
    "menuBG": pygame.image.load("Images/menu.bmp"),
    "gameBG": pygame.image.load("Images/maxcheng1.bmp"),
    "title": pygame.display.set_caption("Game Title")

}
# cannot define keys with other values in the same dict
# therefore, assigned outside dict  
window["display"] = pygame.display.set_mode(window["size"])
# created for easier referencing to dict
windowSize = window["size"] 


# plyr dictionary, containing all player properties
plyr = {
    "coordinates": (0, 0),
    "height": 64,
    "width": 64,
    "speed": 7.5,
    "sprite": pygame.image.load('Images/playerCharacter.bmp')
}

# instances of custom text class
titleText = GUI.Text("Max Cheng Is God", "Fonts/titlefont.ttf", 35, (255, 255, 255))
startText = GUI.Text("Start", "Fonts/titlefont.ttf", 24, (0, 0, 0))
quitText = GUI.Text("Quit", "Fonts/titlefont.ttf", 24, (0, 0, 0))

# dictionary containing instances of custom button class, located on menu window
menuButtons = {
    titleText.originalText: 
        GUI.Button(titleText, (0, 0, 0, 0), (0, 0, 0, 0), 
        [windowSize[0]/2, windowSize[1]/3], window,
        # doesn't treat title rect as rect surface
        is_rect= False),

    startText.originalText: 
        GUI.Button(startText, (170, 170, 170), (100, 100, 100), 
        [windowSize[0]/2, windowSize[1]/2], window),

    quitText.originalText: 
        GUI.Button(quitText, (170, 170, 170), (100, 100, 100), 
        [windowSize[0]/2, 2*windowSize[1]/3], window)
}

if __name__ == "__main__":

    menuState = menu.Menu(framerate, window, menuButtons)

    if menuState == "Start":
        # start the game
        game.Game(framerate, window, plyr)
    elif menuState == "Quit":
        # passes the sequence to quit pygame and quit python
        pass



    pygame.quit()
    exit()
