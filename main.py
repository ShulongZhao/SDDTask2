import pygame


# initializing the constructor
pygame.init()

# screen resolution
res = (1280, 720)

# opens up a window
screen = pygame.display.set_mode(res)

# background image
bg = pygame.image.load("images\menu.bmp")

# white color
color = (0, 0, 0)

# light shade of the button
color_light = (170, 170, 170)

# dark shade of the button
color_dark = (100, 100, 100)

# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()

# defining a font
titlefont = pygame.font.Font('titlefont.ttf', 35)

# rendering a text written in
# this font

quit = titlefont.render('quit', True, color)
title = titlefont.render('Max Cheng is god', True, color)
start = titlefont.render('start', True, color)

# positioning the text based on the center of a rectangle drawn around it
titleRect = title.get_rect(center=(width/2, height/3))
quitRect = quit.get_rect(center=(width/2, 2*height/3))
startRect = start.get_rect(center=(width/2, height/2))

while True:

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        # checks if a mouse is clicked
        if ev.type == pygame.MOUSEBUTTONDOWN:

            # if the mouse is clicked on the button it does things
            if quitRect.left <= mouse[0] <= quitRect.right and quitRect.top <= mouse[1] <= quitRect.bottom:
                pygame.quit()

            if startRect.left <= mouse[0] <= startRect.right and startRect.top <= mouse[1] <= startRect.bottom:
                import game
                pygame.quit()

    # fills the screen with a color
    screen.fill((135, 206, 235))

    # background
    screen.blit(bg, (0, 0))

    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()

    # if mouse is hovered on a button it
    # changes to lighter shade
    if quitRect.left <= mouse[0] <= quitRect.right and quitRect.top <= mouse[1] <= quitRect.bottom:
        pygame.draw.rect(screen, color_light, quitRect)

    else:
        pygame.draw.rect(screen, color_dark, quitRect)

    if startRect.left <= mouse[0] <= startRect.right and startRect.top <= mouse[1] <= startRect.bottom:
        pygame.draw.rect(screen, color_light, startRect)

    else:
        pygame.draw.rect(screen, color_dark, startRect)

    # rendering all text last so that it covers the buttons
    screen.blit(quit, quitRect)
    screen.blit(start, startRect)
    screen.blit(title, titleRect)

    # updates the frames of the game
    pygame.display.update()
