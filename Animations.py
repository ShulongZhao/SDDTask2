import os

class animations:
    def __init__(self, animDirectoryList):
        self.animFramesDict = {}
        # loop through all the directories providied, containing animation frames
        for animDirectory in animDirectoryList:
            # generate a list of all the animation frames within the directory
            animFramesList = os.listdir(animDirectory)
            # sort through all the animation frames, to give their locations
            i = 0
            for animFrame in animFramesList:
                animFramesList[i] = os.path.join(animDirectory, animFrame)
                i += 1

            # separated loops, although they possess the same condition, 
            # to not conflict their functioanlities with one another 
            for animFrame in animFramesList:
                if animFrame.endswith(".bmp") == False:
                    animFramesList.remove(animFrame)

            animFramesList.sort()
            self.animFramesDict[animDirectory] = [animFramesList, False]



                    
