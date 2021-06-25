from pygame.locals import *
import pygame

pygame.init()  # initialise python

size = [700, 700]
image_height, image_width = 400, 400

screen = pygame.display.set_mode(size)

background = (50, 50, 50)

while True:
    for event in pygame.event.get():
        # initialising screen
        pygame.display.set_caption("Naga's Pygame")
        screen.fill(background)

        # quitting the screen
        if event.type == pygame.QUIT:
            exit()

        # loading player character
        ball = pygame.image.load("playerCharacter.bmp")
        ball = pygame.transform.scale(ball, (image_height, image_width))
        screen.blit(source=ball, dest=(200, 200))
        rect = ball.get_rect()  # forms a rect around image for collision detection

        pygame.display.update()