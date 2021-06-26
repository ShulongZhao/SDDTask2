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

# game windows
windowSize = [1280, 720]
window = pygame.display.set_mode(windowSize)
# window backgrounds
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

# instances of custom button class
titleButton = GUI.Button(titleText.renderedText, (0, 0, 0), (0, 0, 0), [windowSize[0]/2, windowSize[1]/3], window)
startButton = GUI.Button(startText.renderedText, (170, 170, 170), (100, 100, 100), [windowSize[0]/2, windowSize[1]/2], window)
quitButton = GUI.Button(quitText.renderedText, (170, 170, 170), (100, 100, 100), [windowSize[0]/2, 2*windowSize[1]/3], window)


# dictionary containing all menu buttons
menuButtons = {
    "title": titleButton,
    "start": startButton,
    "quit": quitButton
}

if __name__ == "__main__":
    
    pygame.display.set_caption(str(titleText.text))

    # returns a boolean
    menuState = menu.Menu(framerate, clock, window, menuWindowBG, menuButtons)

    game.Game(framerate, clock, window, gameWindowBG, plyr,
              # uses menuState as a condition for running game.Game()
              is_game_running=menuState)

    pygame.quit()
    exit()
