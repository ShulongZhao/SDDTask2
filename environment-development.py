from os import environ
import pygame

pygame.init()

class Sprites:
    def __init__(self, fileLocation, size, pixelLocation):
        self.size = [int(size[0]), int(size[1])]
        self.sprite = pygame.image.load(fileLocation)
        # scaling
        self.sprite = pygame.transform.scale(self.sprite, (int(size[0]), int(size[1])))
        self.pixelLocation = pixelLocation




sprites = {
    "ground" : Sprites("Images/maxcheng2.bmp", [100.0, 100.0], [0, 0])
}

 
scaleFactor = 1.5

running = True
while running:

    window = pygame.display.set_mode((1280, 720))
    window.fill((50, 50, 50))

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

    window.blit(_sprite.sprite, _sprite.pixelLocation)
            
    pygame.display.update()
    
exit()
