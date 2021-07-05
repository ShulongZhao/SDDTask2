import pygame


def Menu(_frameRate, _window, buttonDict):

    windowDisplay = _window["display"]
    
    while True:
        # framerate
        clock = pygame.time.Clock()
        clock.tick(_frameRate)

        # background
        windowDisplay.blit(_window["menuBG"], (0, 0))

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
                        # exits loop and returns the name of the button
                        return button.myText.originalText 
                
        # calls main() in all buttons of buttonDict
        for buttonName in buttonDict:
            button = buttonDict[buttonName]
            button.main()
            # rendering text so it is on the uppermost layer
            windowDisplay.blit(button.myText.renderedText, button.textRect)

        pygame.display.update()

