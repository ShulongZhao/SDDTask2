import pygame


def Menu(_frameRate, _clock, _window, _windowBG, buttonDict):
    pygame.init()

    # assigned the instances of the Button class in the menuButtons dict
    title = buttonDict["title"]
    start = buttonDict["start"]
    quit = buttonDict["quit"]

    gameState = True
    while gameState:
        # framerate
        _clock.tick(_frameRate)

        # background
        _window.blit(_windowBG, (0, 0))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                gameState = False  # exits loop

            # checks if mouse clicks buttons
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # conditions for mouse click on buttons
                start.ButtonClick(returnValue=True)
                quit.ButtonClick(returnValue=False)

        # rendering text last so that it covers buttons
        _window.blit(quit.myText, quit.textRect)
        _window.blit(start.myText, start.textRect)
        _window.blit(title.myText, title.textRect)

        pygame.display.update()

    return gameState  # returns the game's state
