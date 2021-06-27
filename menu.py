from types import TracebackType
import pygame


def Menu(_frameRate, _window, _windowBG, buttonDict):
    pygame.init()
    
    while True:
        # framerate
        clock = pygame.time.Clock()
        clock.tick(_frameRate)

        # background
        _window.blit(_windowBG, (0, 0))

        # events (key presses, mouse presses)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return None # exits loop                                              

            # created a loop so any number of buttons 
            # can be added without altering this file
            for buttonName in buttonDict:
                button = buttonDict[buttonName]
                # checks if mouse clicks buttons
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # condition for mouse click on buttons
                    if button.IsButtonClick() == True:
                        return button.myText.originalText # exits loop
                
        # calls main() in all buttons of buttonDict
        for buttonName in buttonDict:
            button = buttonDict[buttonName]
            button.main()
            # rendering text so it is on the uppermost layer
            _window.blit(button.myText.renderedText, button.textRect)

        pygame.display.update()

