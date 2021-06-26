import pygame

pygame.init()

# screen resolution
res = (1280, 720)
# opens up a window
screen = pygame.display.set_mode(res)

# background image
bg = pygame.image.load("Images/menu.bmp")

# colours
color = (0, 0, 0)
# different shades of the button
color_light = (170, 170, 170)
color_dark = (100, 100, 100)

# stores the width and height of the screen
width = screen.get_width()
height = screen.get_height()

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


def Menu():
    gameState = True
    while gameState:

        # stores the (x,y) coordinates as a tuple
        mouse = pygame.mouse.get_pos()

        screen.fill((135, 206, 235))
        # background
        screen.blit(bg, (0, 0))

        # lighter shade if mouse is hovered over button
        if quitRect.left <= mouse[0] <= quitRect.right and quitRect.top <= mouse[1] <= quitRect.bottom:
            pygame.draw.rect(screen, color_light, quitRect)
        else:
            pygame.draw.rect(screen, color_dark, quitRect)

        if startRect.left <= mouse[0] <= startRect.right and startRect.top <= mouse[1] <= startRect.bottom:
            pygame.draw.rect(screen, color_light, startRect)
        else:
            pygame.draw.rect(screen, color_dark, startRect)

        # rendering text last so that it covers buttons
        screen.blit(quit, quitRect)
        screen.blit(start, startRect)
        screen.blit(title, titleRect)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                gameState = False  # exits loop

            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
                # conditions for mouse click on buttons
                if quitRect.left <= mouse[0] <= quitRect.right and quitRect.top <= mouse[1] <= quitRect.bottom:
                    gameState = False  # exits loop
                elif startRect.left <= mouse[0] <= startRect.right and startRect.top <= mouse[1] <= startRect.bottom:
                    return gameState  # exits loop and returns gameState = True

        pygame.display.update()

    return gameState  # returns the game's state
