import os

class animations:
    def __init__(self, animDirectoryList):
        # loop through all the directories providied, containing animation frames
        for animDirectory in animDirectoryList:
            # generate a list of all the animation frames within the directory
            self.animFramesList = os.listdir(animDirectory)
            # sort through all the animation frames, to give their locations
            for animFrame in self.animFramesList:
                for i in range(len(self.animFramesList)):
                    self.animFramesList[i].replace(animFrame, os.path.join(animDirectory, animFrame))
                if animFrame.endswith(".bmp") == False:
                    self.animFramesList.remove(animFrame)
            
            self.animFramesDict = {}
            self.animFramesDict[animDirectory] = [self.animFramesList, False]


                    
