import pygame
import os
from ast import literal_eval

class Player:
    def __init__(self, coordinates, size, speed):
        self.coordinates = coordinates
        self.size = size
        self.speed = speed
        self.surface = None

        # idle animation dictionary
        self.idleAnim = []

        self.InitAnimations()

    # managing all animation work
    def InitAnimations(self): # need to add animDict parameter, to automate animations
        idleDirectory = "Images/Player Sprites"
        idleFramesList = os.listdir(idleDirectory)

        for idleFrame in idleFramesList:
            if idleFrame.endswith(".bmp"):
                self.idleAnim.append(os.path.join(idleDirectory, idleFrame))
