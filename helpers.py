#make random positions for terrain things
from cmu_graphics import *
import random

class Helper:
    def randomPosition(): 
        rangeMin, rangeMax = 0, 800 #edges of screen
        return random.randint(rangeMin, rangeMax)