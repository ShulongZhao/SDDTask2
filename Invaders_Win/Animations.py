import os

class Animation:
    # increments every iteration to cycle through all frames
    animIdx = 0

    def __init__(self, dir, cooldown, maxCycles):  
        # directory containing all the animations 
        self.dir = dir

        # cooldowns and info for anim frame time control
        self.timeSinceLastCall = 0
        self.cooldown = cooldown
        # making temp_cooldown immutable
        self.tempCooldown = list((cooldown, cooldown))[0]

        # for the directories in the animation directory list provided...
        # generate and sort a list of all the animation frames within the directory
        self.framesList = os.listdir(dir)
        self.framesList.sort()

        # number of current cycles of the animation
        self.currentCycles = 0
        # max number of cycles for the animation
        # (multiplied by the number of frames within the folder to account for a whole rotation of the whole folder
        # as opposed to counting the individual images)
        self.maxCycles = maxCycles * len(self.framesList)

        self.idx = 0

        i = 0
        while i <= len(self.framesList) - 1:
            # give all frames their correct directory, and not just their filename
            self.framesList[i] = os.path.join(dir, self.framesList[i])
            # remove any files that aren't '.bmp'
            if self.framesList[i].endswith(".bmp") == False:
                self.framesList.remove(self.framesList[i])
                # when element is removed, the next element becomes the same index as the one removed, 
                # therefore i should be looped again for next element
                i -= 1   
            i += 1




    
            


