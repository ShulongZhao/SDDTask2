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

if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption("(insert game title here)")

    # returns the player's input (play or quit) as a boolean
    menuState = menu.Menu()
    # uses menuState as a condition for running game.Game()
    game.Game(_framerate=40, _windowSize=(700, 700),
              _windowBackground=(50, 50, 50), _plyr=plyr, is_game_running=menuState)
    pygame.quit()
    exit()
