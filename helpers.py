#determine collision --> game restart
#make random positions for terrain things
import random

def randomPosition(): 
    rangeMin, rangeMax = 0, 800 #edges of screen
    pos = random.randRange(rangeMin, rangeMax)