#determine collision --> game restart
#make random positions for terrain things
from cmu_graphics import *
import random


# NEED TO MODIFY GAME OVER TO DETECT RIGHT WHEN BOTTOM OF DOG HITS
# FIGURE OUT IF GAME OVER DIRECTS TO RESTART

class Helper:
    def randomPosition(): 
        rangeMin, rangeMax = 0, 800 #edges of screen
        return random.randint(rangeMin, rangeMax)