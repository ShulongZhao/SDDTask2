import pygame


def Menu(_frameRate, _clock, _window, _windowBG, buttonDict):
    pygame.init()

    gameState = True
    while gameState:
        # framerate
        _clock.tick(_frameRate)

        # background
        _window.blit(_windowBG, (0, 0))

        # events (key presses, mouse presses)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                gameState = False  # exits loop

            # automated this process so any number of buttons 
            # can be added without altering this file
            for button in buttonDict:
                # checks if mouse clicks buttons
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # condition for mouse click on buttons
                    if buttonDict[button].OnButtonClick() == buttonDict[button].myText.originalText: 
                        return buttonDict[button].myText.originalText
                    else:
                        #continue with the loop
                        continue

        # calls main() in all buttons of buttonDict
        for button in buttonDict:
            buttonDict[button].main()
            # rendering text last so that it covers buttons
            _window.blit(buttonDict[button].myText.renderedText, buttonDict[button].textRect)

        pygame.display.update()

    return gameState  # returns the game's state
