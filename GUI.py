import pygame

class Window:

    def __init__(self, title, frameRate, bg=(0, 0, 0)):
        self.title = title

        self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        self.size = self.screen.get_size()

        try:
            self.bg = pygame.transform.scale(pygame.image.load(bg), self.size)
        except:
            self.bg = pygame.Surface(self.screen.get_size()).fill(bg)
        

        self.width = self.size[0]
        self.height = self.size[1]
        self.frameRate = frameRate
        self.layers = []

    def Main(self):
        self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        self.size = self.screen.get_size()
        self.width = self.size[0]
        self.height = self.size[1]
        pygame.display.set_caption(self.title)
        self.bg = pygame.transform.scale(pygame.image.load(self.bg), self.size)

class Layer (pygame.sprite.Sprite):

    def __init__(self, layerRender, pos, window, clr=None, hoverClr=None, is_button=False):

        pygame.sprite.Sprite.__init__(self)
        
        # custom Text class
        self.layerRender = layerRender                
        self.clr = clr
        self.hoverClr = hoverClr
        self.pos = pos
        self.is_button = is_button

        self.rect = self.layerRender.renderedSurface.get_rect(center=(self.pos[0] * window.height / 720, self.pos[1] * window.height / 720))
        if self.layerRender.originalText == "":
            self.image = self.layerRender.renderedSurface
        else:
            self.image = pygame.Surface(self.rect.size)

    def Main(self):
        # stores the (x, y) coordinates as a tuple
        self.mouse = pygame.mouse.get_pos()

        try:
            self.image.fill(self.clr)
        except TypeError:
            # excepting the condition that there is no colour provided
            pass

        if self.is_button == True:
            self.OnHover() 

        self.image.blit(self.layerRender.renderedSurface, self.layerRender.renderedSurface.get_rect())

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


# renders the image for the layer
class LayerRenderer:
    def __init__(self, window, text=None, textFontLocation=None, textFontSize=None, textColour=None, renderedImage=None):

        self.originalText = text
        try:
            self.renderedSurface = pygame.font.Font(textFontLocation, textFontSize * window.height / 720).render(text, True, textColour)
        except TypeError:
            self.renderedSurface = renderedImage
        

        
