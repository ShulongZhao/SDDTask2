import pygame
from pygame.locals import *

pygame.init()

size = 700, 700
width, height = size

window = pygame.display.set_mode(size)

running = True
background = (50, 50, 50)

while True:
    for event in pygame.event.get():
        # initialising window
        pygame.display.set_caption("Naga's Pygame")
        window.fill(background)
        pygame.display.update()
        # quitting the window
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        # loading player UI
        # ball = pygame.image.load(
        #     "/Users/nagamaddali/Desktop/untitled folder/download.bmp")
        # rect = ball.get_rect()
        # speed = [2, 2]

        # rect = rect.move(speed)
        # if rect.left < 0 or rect.right > width:
        #     speed[0] = -speed[0]
        # if rect.top < 0 or rect.bottom > height:
        #     speed[1] = -speed[1]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                background = (255, 0, 0)
            elif event.key == pygame.K_g:
                background = (0, 255, 0)
            elif event.key == pygame.K_b:
                background = (0, 0, 255)
