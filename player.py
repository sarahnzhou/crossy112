from cmu_graphics import *
from base import basePlayer

class Player(basePlayer):
    def __init__(self, userX, userY, rightimageLink, leftimageLink, soundLink):
        super().__init__(userX, userY, rightimageLink, leftimageLink)
        self.moveSound = soundLink
        self.playerMoveCount = 0 #terrain faster as more moves made per time frame
        self.speedDecay = 0.1
        self.hasMoved = False
   
   # https://stackoverflow.com/questions/63926261/python-how-to-make-drawn-elements-snap-to-grid-in-pygame
    def snapToGrid(self, xCoord, gridSize):
        #grid size player step size for now - 50
        return rounded(xCoord/50)*50

    def move(self, direction, canvasWidth, canvasHeight, terrain, gridSize = 50):
        newX, newY = self.x, self.y
        self.prevX = self.x
        moved = False
        if direction == 'left' and self.x - 25 >= 0: # make sure no going off canvas
            newX-=self.horizontalStepSize
            self.imageLink = self.leftImageLink
            moved = True
        if direction == 'right' and self.x + 25 + self.width <= canvasWidth: 
            newX+=self.horizontalStepSize
            self.imageLink = self.rightImageLink
            moved = True
        if direction == 'up' and self.y - 25 >= 0: 
            newY-=self.verticalstepSize
            moved = True
        if direction == 'down' and self.y + 25 + self.height <= canvasHeight: 
            newY+=self.verticalstepSize
            moved = True

        block = terrain.getPlayerBlock(self, intendedY = newY)
        if block:
            for obs in block.obstacles:
                if obs.obstacleType == 'tree':
                    if self.collision(obs, newX, newY):
                        return  #just make sure no moving
                elif obs.obstacleType == 'boat' and self.collision(obs, newX, newY):
                    self.updateBoat(obs, terrain)
        
        if moved:
            self.x = self.snapToGrid(newX, gridSize)
            self.y = newY
            self.moveSound.play(restart=False)
            self.playerMoveCount += 1
            self.hasMoved = True
            return True