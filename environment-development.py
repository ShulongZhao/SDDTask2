from os import environ
import pygame

pygame.init()

class Sprites (pygame.sprite.Sprite):

    def __init__(self, fileLocation, size, pixelLocation):
        pygame.sprite.Sprite().__init__(self)

        self.size = [int(size[0]), int(size[1])]
        self.name = fileLocation[7:]
        self.image = pygame.transform.scale(pygame.image.load(fileLocation), (int(size[0]), int(size[1])))
        self.rect = self.image.get_rect()
        self.pixelLocation = pixelLocation
        self.spriteGroup = None


sprites = {
    "ground" : Sprites("Images/maxcheng2.bmp", [100.0, 100.0], [0, 0])
}

scaleFactor = 1.5

windowSize = (1280, 720)

running = True
while running:

    window = pygame.display.set_mode(windowSize)
    window.fill((50, 50, 50))

    for sprite in sprites:
        sprites[sprite]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # exits loop
            running = False

        for sprite in sprites:
            _sprite = sprites[sprite] 

            # sprite x and y's are the top-left coordiantes of the sprite
            _sprite_X = _sprite.pixelLocation[0]
            _sprite_Y = _sprite.pixelLocation[1]
            _sprite_w = _sprite.size[0]
            _sprite_h = _sprite.size[1]

            mouse = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed() == (1, 0, 0):
                # if user has clicked on item, immediately center it to the mouse pos
                if (_sprite_X <= mouse[0] <= _sprite_X + _sprite_w) and (_sprite_Y <= mouse[1] <= _sprite_Y + _sprite_h):
                    _sprite.pixelLocation = (mouse[0] - _sprite_w/2), (mouse[1] - _sprite_h/2)
                
                if event.type == pygame.MOUSEMOTION:
                    # if the user has picked up an item..
                    if (_sprite_X <= mouse[0] <= _sprite_X + _sprite_w) and (_sprite_Y <= mouse[1] <= _sprite_Y + _sprite_h):
                        _sprite.pixelLocation = (mouse[0] - _sprite_w/2), (mouse[1] - _sprite_h/2)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        _sprite.size[0] *= scaleFactor
                    elif event.key == pygame.K_d:
                        _sprite.size[0] /= scaleFactor
                    elif event.key == pygame.K_w:
                        _sprite.size[1] *= scaleFactor
                    elif event.key == pygame.K_s:
                        _sprite.size[1] /= scaleFactor
                    _sprite.sprite = pygame.transform.scale(_sprite.sprite, [int(_sprite.size[0]), int(_sprite.size[1])])

    for sprite in sprites:
        spriteGroup = pygame.sprite.Group()
        spriteGroup.add(sprites[sprite])
        spriteGroup.draw(window)
            
    pygame.display.update()
    
exit()
