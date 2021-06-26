import pygame

import menu
import game

# plyr dictionary, containing all player properties
plyr = {
    "coordinates": [0, 0],
    "height": 20,
    "width": 20,
    "speed": 7.5,
    "sprite": pygame.image.load("Images/playerCharacter.bmp")
}

menuButtons = {

}

clock = pygame.time.Clock()
framerate = 40

menuWindowSize = [1280, 720]
menuWindowBG = pygame.image.load("Images/menu.bmp")

gameWindowSize = [700, 700]
gameWindowBG = (50, 50, 50)

if __name__ == "__main__":

    pygame.display.set_caption("(insert game title here)")

    # returns a boolean
    menuState = menu.Menu(framerate, clock, menuWindowSize, menuWindowBG)

    game.Game(framerate, clock, gameWindowSize, gameWindowBG, plyr,
              # uses menuState as a condition for running game.Game()
              is_game_running=menuState)

    pygame.quit()
    exit()
