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


    # need to update flipped surfaces because of ever-changing sprites of player
    def UpdateFlippedSurfaces(self):    
        self.surface_original = self.surface
        self.surface_flipped = pygame.transform.flip(self.surface, True, False)

    # managing all animation work
    def Animations(self): # need to add animDict parameter, to automate animations
        idleDirectory = "Images/Player Sprites"
        idleFramesList = os.listdir(idleDirectory)

        for idleFrame in idleFramesList:
            if idleFrame.endswith(".bmp"):
                self.idleAnim.append(os.path.join(idleDirectory, idleFrame))
