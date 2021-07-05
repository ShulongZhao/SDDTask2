import pygame

import Scenes
import GUI
from Characters import Player

# initalises all pygame processes 
pygame.init()

# time
framerate = 40

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

# instance of player class, representing player 
plyr = Player([0, 0], [160, 160], 7.5, "Images/playerCharacter.bmp")

# instances of custom text class
titleText = GUI.Text("Max Cheng Is God", "Fonts/titlefont.ttf", 35, (255, 255, 255))
startText = GUI.Text("Start", "Fonts/titlefont.ttf", 24, (0, 0, 0))
quitText = GUI.Text("Quit", "Fonts/titlefont.ttf", 24, (0, 0, 0))

# dictionary containing instances of custom button class, located on menu window
menuButtons = {
    titleText.originalText: 
        GUI.Button(titleText, (0, 0, 0, 0), (0, 0, 0, 0), 
        [window["size"][0]/2, window["size"][1]/3], window,
        # doesn't treat title rect as rect surface
        is_rect=False),

    startText.originalText: 
        GUI.Button(startText, (170, 170, 170), (100, 100, 100), 
        [window["size"][0]/2, window["size"][1]/2], window),

    quitText.originalText: 
        GUI.Button(quitText, (170, 170, 170), (100, 100, 100), 
        [window["size"][0]/2, 2*window["size"][1]/3], window)
}

if __name__ == "__main__":

    menuState = Scenes.Menu(framerate, window, menuButtons)

    if menuState == "Start":
        # start the game
        Scenes.Game(framerate, window, plyr)
    elif menuState == "Quit":
        # passes the sequence to quit pygame and quit python
        pass


    pygame.quit()
    exit()
