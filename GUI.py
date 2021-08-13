from typing import Text
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

    def __init__(self, pos, window, text=None, textFontLocation=None, textFontSize=None, textColour=None, textHoverClr=None, renderedImage=None,  is_button=False, is_active=True):

        pygame.sprite.Sprite.__init__(self)

        self.mouse = pygame.mouse.get_pos()


        self.pos = pos
        self.window = window
        self.text = text
        self.textFontLocation = textFontLocation
        self.textFontSize = textFontSize
        self.textColour = textColour
        self.textHoverClr = textHoverClr
        self.renderedImage = renderedImage
        self.is_button = is_button
        self.is_active = is_active
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()

        self.Main()


        self.rect = self.renderedSurface.get_rect(center=(self.pos[0], self.pos[1]))
        self.image = pygame.Surface(self.rect.size)

    def On_Hover(self):
        try:
            if self.renderedImage == None:
                self.renderedSurface = self.renderedFont.render(self.text, True, self.textHoverClr)
        except TypeError:
            pass

    def Main(self):
        # stores the (x, y) coordinates as a tuple
        self.mouse = pygame.mouse.get_pos()

        self.Surface_Renderer(self.window.screen, (0, 0))

        try:
            if self.renderedImage == None:
                self.renderedSurface = self.renderedFont.render(self.text, True, self.textColour)
        # excepting the condition that there is no colour provided
        except TypeError:
            pass

        # if the layer is being hovered over and its a button
        if self.is_button == True and ((self.rect.left <= self.mouse[0] <= self.rect.right) and (self.rect.top <= self.mouse[1] <= self.rect.bottom)):            
            self.On_Hover()

        self.image.blit(self.renderedSurface, self.renderedSurface.get_rect())

    
    def Surface_Renderer(self, surface, surfaceLocation):

        # if layer being rendered is text then..
        if self.renderedImage == None and (self.text and self.textFontLocation and self.textFontSize and self.textColour) != None:
            self.renderedFont = pygame.font.Font(self.textFontLocation, self.textFontSize)
            self.renderedSurface = self.renderedFont.render(self.text, True, self.textColour, (255, 255, 255, 0))
        # else if the layer rendered is an image
        elif self.renderedImage != None and (self.text and self.textFontLocation and self.textFontSize and self.textColour) == None:
            self.renderedSurface = self.renderedImage
        else:
            print("Crash from GUI")
            exit()

    def IsLayerClicked(self):
        # if layer is a button
        if (self.is_button and (self.rect.left <= self.mouse[0] <= self.rect.right) and (self.rect.top <= self.mouse[1] <= self.rect.bottom)):
            return True

        
