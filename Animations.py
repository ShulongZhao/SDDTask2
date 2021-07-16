import os

class Animation:
    # increments every iteration to cycle through all frames
    plyrAnimIdx = 0

    def __init__(self, animsDir, frameTime, maxCycles, isActive=False):  
        # directory containing all the animations 
        self.animsDir = animsDir
        # time for frame to stay on screen 
        self.frameTime = frameTime
        # number of current cycles of the animation
        self.currentCycles = 0
        # max number of cycles for the animation
        self.maxCycles = maxCycles

        self.isActive = isActive
        # for the directories in the animation directory list provided...
        # generate and sort a list of all the animation frames within the directory
        self.animFramesList = os.listdir(animsDir)
        self.animFramesList.sort()

        i = 0
        while i < len(self.animFramesList):
            try:
                # give all frames their correct directory, and not just their filename
                self.animFramesList[i] = os.path.join(animsDir, self.animFramesList[i])
                # remove any files that aren't '.bmp'
                if self.animFramesList[i].endswith(".bmp") == False:
                    self.animFramesList.remove(self.animFramesList[i])
                    # when element is removed, the next element becomes the same index as the one removed, 
                    # therefore i should be looped again for next element
                    i -= 1   
                i += 1
            except IndexError:
                # debuging statement
                print("Index Error: i = " + i)
                break
    
    def ResetAnimCycles():
        pass

            


