import pygame

class Window:

    def __init__(self, title, size, frameRate, bgFileLocation):
        self.title = title
        self.size = size
        self.width = self.size[0]
        self.height = self.size[1]
        self.screen = pygame.display.set_mode(self.size)
        self.bg = pygame.image.load(bgFileLocation)
        self.frameRate = frameRate

class Layer (pygame.sprite.Sprite):

    def __init__(self, myText, pos, window, clr=None, hoverClr=None, is_button=False):

        pygame.sprite.Sprite.__init__(self)
        
        # custom Text class
        self.myText = myText                
        self.clr = clr
        self.hoverClr = hoverClr
        self.pos = pos
        self.windowScreen = window.screen
        self.is_button = is_button

        self.rect = (self.myText.renderedSurface).get_rect(center=self.pos)
        self.image = pygame.Surface(self.rect.size)

    def main(self):
        # stores the (x,y) coordinates as a tuple
        self.mouse = pygame.mouse.get_pos()

        try:
            self.image.fill(self.clr)
        except:
            pass

        if self.is_button == True:
            self.OnHover() 

        self.image.blit(self.myText.renderedSurface, self.myText.renderedSurface.get_rect())

    def OnHover(self):
        if (self.rect.left <= self.mouse[0] <= self.rect.right) and (self.rect.top <= self.mouse[1] <= self.rect.bottom):
            self.image.fill(self.hoverClr)

    # manually-called 
    def IsLayerClicked(self):
        # if layer is a button
        if self.is_button:
            if (self.rect.left <= self.mouse[0] <= self.rect.right) and (self.rect.top <= self.mouse[1] <= self.rect.bottom):
                return True
        # else if not a button
        else:
            pass


class Text:
    def __init__(self, text, textFontLocation, textFontSize, textColour):
        self.originalText = text
        self.renderedSurface = pygame.font.Font(textFontLocation, textFontSize).render(text, True, textColour)


        
