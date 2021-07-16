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

class Button:

    def __init__(self, myText, buttClr, buttHoverClr, buttPos, window, is_rect=True):
        
        # custom Text class
        self.myText = myText                
        self.buttClr = buttClr
        self.buttHoverClr = buttHoverClr
        self.buttPos = buttPos
        # specifying only the display, and not all the properties of 'window'
        self.windowDisplay = window.screen
        self.is_rect = is_rect

    def main(self):
        # stores the (x,y) coordinates as a tuple
        self.mouse = pygame.mouse.get_pos()

        self.TextRect()
        self.OnButtonHover()

    # automatically-called
    def TextRect(self):
        #forms a rect surface from the rendered text 
        self.textRect = (self.myText.renderedText).get_rect(center=self.buttPos)

    def OnButtonHover(self):
        if (self.textRect.left <= self.mouse[0] <= self.textRect.right) and (self.textRect.top <= self.mouse[1] <= self.textRect.bottom):
            pygame.draw.rect(self.windowDisplay, self.buttHoverClr, self.textRect)
        else:
            pygame.draw.rect(self.windowDisplay, self.buttClr, self.textRect)

    # manually-called 
    def IsButtonClick(self):
        # if the button has as a rect...
        if self.is_rect:
            if (self.textRect.left <= self.mouse[0] <= self.textRect.right) and (self.textRect.top <= self.mouse[1] <= self.textRect.bottom):
                return True
        # else if the button should not have a rect component
        elif self.is_rect == False:
            pass


class Text:
    originalText = ""      
    renderedText = None  
    def __init__(self, text, textFontLocation, textFontSize, textColour):
        self.originalText = text
        renderedText = pygame.font.Font(textFontLocation, textFontSize).render(text, True, textColour)
        self.renderedText = renderedText


        
