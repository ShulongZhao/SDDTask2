import pygame

pygame.init()
res = (540, 720)
screen = pygame.display.set_mode(res)
bg = pygame.image.load("images\gamebackground.jpeg")

while True:

    # background
    screen.fill((135, 206, 235))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        pygame.display.update()