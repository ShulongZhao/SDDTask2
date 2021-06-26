import pygame

import menu
import game

if __name__ == "__main__":
    # returns the player's input (play or quit) as a boolean
    menuState = menu.Menu()
    # uses menuState as a condition for running game.Game()
    game.Game(is_game_running=menuState)
    pygame.quit()
    exit()
