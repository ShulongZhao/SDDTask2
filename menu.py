import pygame

pygame.init()


def Menu(_frameRate, _clock, _windowSize, _windowBG):

    # opens up a window
    window = pygame.display.set_mode(_windowSize)

    # stores the width and height of the screen
    width = window.get_width()
    height = window.get_height()

    color = (0, 0, 0)
    # different shades of the button
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)

    # fonts
    titlefont = pygame.font.Font('Fonts/titlefont.ttf', 35)
    # rendering fonts
    quit = titlefont.render('quit', True, color)
    title = titlefont.render('Max Cheng is god', True, color)
    start = titlefont.render('start', True, color)

    # positioning the text based on the center of a rectangle drawn around it
    titleRect = title.get_rect(center=(width/2, height/3))
    quitRect = quit.get_rect(center=(width/2, 2*height/3))
    startRect = start.get_rect(center=(width/2, height/2))

    gameState = True
    while gameState:
        # framerate
        _clock.tick(_frameRate)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                gameState = False  # exits loop

            # checks if mouse clicks buttons
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # conditions for mouse click on buttons
                if (quitRect.left <= mouse[0] <= quitRect.right) and (quitRect.top <= mouse[1] <= quitRect.bottom):
                    gameState = False  # exits loop, returning a false value to indicate quitting
                elif (startRect.left <= mouse[0] <= startRect.right) and (startRect.top <= mouse[1] <= startRect.bottom):
                    return gameState  # exits loop and returns gameState = True

        # stores the (x,y) coordinates as a tuple
        mouse = pygame.mouse.get_pos()

        # background
        window.blit(_windowBG, (0, 0))

        # mouse hover over buttons logic
        if (quitRect.left <= mouse[0] <= quitRect.right) and (quitRect.top <= mouse[1] <= quitRect.bottom):
            pygame.draw.rect(window, color_light, quitRect)
        else:
            pygame.draw.rect(window, color_dark, quitRect)

        if (startRect.left <= mouse[0] <= startRect.right) and (startRect.top <= mouse[1] <= startRect.bottom):
            pygame.draw.rect(window, color_light, startRect)
        else:
            pygame.draw.rect(window, color_dark, startRect)

        # rendering text last so that it covers buttons
        window.blit(quit, quitRect)
        window.blit(start, startRect)
        window.blit(title, titleRect)

        pygame.display.update()

    return gameState  # returns the game's state
