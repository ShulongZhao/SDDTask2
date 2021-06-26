import pygame

class Button:
    myText = None
    buttonColour = ()
    buttonHoverColour = ()
    buttonPos = []
    mousePos = []
    window = None
    textRect = None

    def __init__(self, myText, buttonColour, buttonHoverColour, buttonPos, mousePos, window):
        global textRect

        self.myText = myText
        self.buttonColour = buttonColour
        self.buttonHoverColour = buttonHoverColour
        self.buttonPos = buttonPos
        self.mousePos = mousePos
        self.window = window

        self.TextRect()
        self.ButtonHover()

    def TextRect(self):
        self.textRect = self.myText.get_rect(center=(self.buttonPos[0], self.buttonPos[1]))

    def ButtonHover(self):
        if (self.textRect.left <= self.mousePos[0] <= self.textRect.right) and (self.textRect.top <= self.mousePos[1] <= self.textRect.bottom):
            pygame.draw.rect(self.window, self.buttonHoverColour, self.textRect)
        else:
            pygame.draw.rect(self.window, self.buttonColour, self.textRect)

    def ButtonClick(self, returnValue):
        if (self.textRect.left <= self.mousePos[0] <= self.textRect.right) and (self.textRect.top <= self.mousePos[1] <= self.textRect.bottom):
            return returnValue


class Text:
    def RenderText(self, text, textFontLocation, textFontSize, textColour):
        renderedText = pygame.font.Font(textFontLocation, textFontSize).render(text, True, textColour)
        return renderedText
