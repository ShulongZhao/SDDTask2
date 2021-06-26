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

# instance of custom text class
myText = GUI.Text()

titleText = myText.RenderText("Max Cheng Is God", "Fonts/titlefont.ttf", 35, (0, 0, 0))
startText = myText.RenderText("Start", "Fonts/titlefont.ttf", 12, (0, 0, 0))
quitText = myText.RenderText("Quit", "Fonts/titlefont.ttf", 12, (0, 0, 0))

# instances of custom button class
titleButton = GUI.Button(titleText, (0, 0, 0, 0), (0, 0, 0, 0), [windowSize[0]/2, windowSize[1]/3], mouse, window)
startButton = GUI.Button(startText, (170, 170, 170), (100, 100, 100), [windowSize[0]/2, windowSize[1]/2], mouse, window)
quitButton = GUI.Button(quitText, (170, 170, 170), (100, 100, 100), [windowSize[0]/2, 2*windowSize[1]/3], mouse, window)


# dictionary containing all menu buttons
menuButtons = {
    "title": titleButton,
    "start": startButton,
    "quit": quitButton
}


if __name__ == "__main__":

    print(quitButton.textRect)

    pygame.display.set_caption(str(titleText))

    # returns a boolean
    menuState = menu.Menu(framerate, clock, window, menuWindowBG, menuButtons)

    game.Game(framerate, clock, window, gameWindowBG, plyr,
              # uses menuState as a condition for running game.Game()
              is_game_running=menuState)

    pygame.quit()
    exit()
