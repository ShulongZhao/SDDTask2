import pygame

class Button:
    myText = None
    buttonColour = None
    buttonHoverColour = ()
    buttonPos = []
    window = None
    textRect = None
    mouse = []

    def __init__(self, myText, buttonColour, buttonHoverColour, buttonPos, window):
        global textRect

        self.myText = myText
        self.buttonColour = buttonColour
        self.buttonHoverColour = buttonHoverColour
        self.buttonPos = buttonPos
        self.window = window

    def main(self):
        # stores the (x,y) coordinates as a tuple
        self.mouse = pygame.mouse.get_pos()
        #calls following subroutines
        self.TextRect()
        self.OnButtonHover()

    def TextRect(self):
        self.textRect = self.myText.renderedText.get_rect(center=(self.buttonPos[0], self.buttonPos[1]))

    def OnButtonHover(self):
        if (self.textRect.left <= self.mouse[0] <= self.textRect.right) and (self.textRect.top <= self.mouse[1] <= self.textRect.bottom):
            pygame.draw.rect(self.window, self.buttonHoverColour, self.textRect)
        else:
            pygame.draw.rect(self.window, self.buttonColour, self.textRect)


    def OnButtonClick(self):
        if (self.textRect.left <= self.mouse[0] <= self.textRect.right) and (self.textRect.top <= self.mouse[1] <= self.textRect.bottom):
            return self.myText.originalText


class Text:
    originalText = ""      
    renderedText = None  
    def __init__(self, text, textFontLocation, textFontSize, textColour):
        self.originalText = text
        renderedText = pygame.font.Font(
            textFontLocation, textFontSize).render(text, True, textColour)
        self.renderedText = renderedText


        
