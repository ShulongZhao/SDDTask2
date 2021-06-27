import pygame

import menu
import game
import GUI

pygame.init()

# time
clock = pygame.time.Clock()
framerate = 40

# stores the (x,y) coordinates as a tuple
mouse = pygame.mouse.get_pos()

# universal game window
windowSize = [1280, 720]
window = pygame.display.set_mode(windowSize)

# separate window backgrounds
menuWindowBG = pygame.image.load("Images/menu.bmp")
gameWindowBG = (50, 50, 50)

# plyr dictionary, containing all player properties
plyr = {
    "coordinates": [0, 0],
    "height": 20,
    "width": 20,
    "speed": 7.5,
    "sprite": pygame.image.load("Images/playerCharacter.bmp")
}

# instances of custom text class
titleText = GUI.Text("Max Cheng Is God", "Fonts/titlefont.ttf", 35, (255, 255, 255))
startText = GUI.Text("Start", "Fonts/titlefont.ttf", 24, (0, 0, 0))
quitText = GUI.Text("Quit", "Fonts/titlefont.ttf", 24, (0, 0, 0))

# dictionary containing instances of custom button class, located on menu window
menuButtons = {
    titleText.originalText: GUI.Button(titleText, (0, 0, 0), (0, 0, 0), [windowSize[0]/2, windowSize[1]/3], window),
    startText.originalText: GUI.Button(startText, (170, 170, 170), (100, 100, 100), [windowSize[0]/2, windowSize[1]/2], window),
    quitText.originalText: GUI.Button(quitText, (170, 170, 170), (100, 100, 100), [windowSize[0]/2, 2*windowSize[1]/3], window)
}


#sceneOrder = ["menu", "start", ]

if __name__ == "__main__":
    
    pygame.display.set_caption("Game Title")

    menuState = menu.Menu(framerate, clock, window, menuWindowBG, menuButtons)

    # for buttonName in menuButtons:
    #     if menuState == buttonName:
    #         pass

    game.Game(framerate, clock, window, gameWindowBG, plyr)

    pygame.quit()
    exit()
