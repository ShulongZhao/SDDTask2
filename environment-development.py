from os import environ
import pygame

pygame.init()

class Sprites:
    sprite = ""
    def __init__(self, fileLocation, size, pixelLocation):
        global sprite

        self.size = size
        sprite = pygame.image.load(fileLocation)
        # scaling
        sprite = pygame.transform.scale(sprite, size)
        self.sprite = sprite
        self.pixelLocation = pixelLocation




sprites = {
    "ground" : Sprites("Images/maxcheng2.bmp", [100, 100], [0, 0])
}

 

def environment():
    while True:

        window = pygame.display.set_mode((1280, 720))
        window.fill((50, 50, 50))

        for sprite in sprites:
            # instantiate all sprites
            window.blit(sprites[sprite].sprite, sprites[sprite].pixelLocation)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # exits loop
                return


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

            
                # elif event.type == pygame.MOUSEMOTION:
                #     if (_sprite_X - 10 <= mouse[0] <= _sprite_X + 10) and (_sprite_Y <= mouse[1] <= _sprite_Y + _sprite_h) or (_sprite_X + _sprite_w - 10 <= mouse[0] <= _sprite_X + _sprite_w + 10) and (_sprite_Y <= mouse[1] <= _sprite_Y + _sprite_h):
                #         pygame.transform.scale(_sprite.sprite, (int(_sprite.pixelLocation[0] * (mouse[0] - _sprite.size[0]/2)), int(_sprite.pixelLocation[1] * mouse[1] - _sprite.size[1]/2)))
                #     elif (_sprite_Y - 10 <= mouse[1] <= _sprite_Y + 10) and (_sprite_X <= mouse[0] <= _sprite_X + _sprite_w) or (_sprite_Y + _sprite_h - 10 <= mouse[1] <= _sprite_Y + _sprite_h + 10) and (_sprite_X <= mouse[0] <= _sprite_X + _sprite_w):
                #         pass

        pygame.display.update()
            
            
if __name__ == "__main__":

    environment()
