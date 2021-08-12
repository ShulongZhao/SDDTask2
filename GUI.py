import pygame


class Window:

    def __init__(self, title, frameRate, bg=(0, 0, 0)):
        self.title = title
        self.bg = bg
        self.frameRate = frameRate
        self.layers = []

        self.Main()

    def Main(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.size = self.screen.get_size()
        self.width = self.size[0]
        self.height = self.size[1]
        pygame.display.set_caption(self.title)
        self.bg = pygame.transform.scale(pygame.image.load(self.bg), self.size)


class Layer (pygame.sprite.Sprite):

    def __init__(self, layerRender, pos, clr=None, hoverClr=None, is_button=False, is_active=True, has_rect=False):

        pygame.sprite.Sprite.__init__(self)

        self.mouse = pygame.mouse.get_pos()

        # custom Text class
        self.layerRender = layerRender
        self.clr = clr
        self.hoverClr = hoverClr
        self.pos = pos
        self.is_button = is_button
        self.is_active = is_active
        self.has_rect = has_rect

        self.rect = self.layerRender.renderedSurface.get_rect(center=(self.pos[0], self.pos[1]))
        self.image = pygame.Surface(self.rect.size)

    def OnHover(self):
        try:
            # if the layer is being hovered over
            if (self.rect.left <= self.mouse[0] <= self.rect.right) and (self.rect.top <= self.mouse[1] <= self.rect.bottom):
                if(self.has_rect):
                    self.layerRender.renderedSurface.fill(self.hoverClr)
                    return True
                # else if the layer possesses text elements but doesn't need a rect behind it
                elif self.has_rect == False and self.layerRender.renderedImage == None:
                    self.layerRender.renderedSurface = self.layerRender.renderedFont.render(self.layerRender.originalText, True, self.hoverClr)

        except TypeError:
            pass

    def Main(self):
        # stores the (x, y) coordinates as a tuple
        self.mouse = pygame.mouse.get_pos()

        try:
            if self.has_rect == True:
                self.layerRender.renderedSurface.fill(self.clr)
            elif self.has_rect == False and self.layerRender.renderedImage == None:
                self.layerRender.renderedSurface = self.layerRender.renderedFont.render(self.layerRender.originalText, True, self.clr)
        # excepting the condition that there is no colour provided
        except TypeError:
            pass

        if self.is_button == True:
            self.OnHover()

        self.image.blit(self.layerRender.renderedSurface, self.layerRender.renderedSurface.get_rect())

    # manually-called

    def IsLayerClicked(self):
        # if layer is a button
        if self.is_button:
            if (self.rect.left <= self.mouse[0] <= self.rect.right) and (self.rect.top <= self.mouse[1] <= self.rect.bottom):
                return True


# renders the image for the layer
class LayerRenderer:
    def __init__(self, text=None, textFontLocation=None, textFontSize=None, textColour=None, renderedImage=None):

        self.originalText = text
        self.renderedImage = renderedImage

        # if layer being rendered is text then..
        if renderedImage == None and (text and textFontLocation and textFontSize and textColour) != None:
            self.renderedFont = pygame.font.Font(textFontLocation, textFontSize)
            self.renderedSurface = self.renderedFont.render(text, True, textColour)
        # else if the layer rendered is an image
        elif renderedImage != None and (text and textFontLocation and textFontSize and textColour) == None:
            self.renderedSurface = renderedImage
        else:
            print("Crash from GUI")
            exit()
