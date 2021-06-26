import pygame

import menu
import game

if __name__ == "__main__":
    menuState = menu.Menu()
    game.Game(is_game_running=menuState)
    pygame.quit()
    exit()
