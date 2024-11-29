from cmu_graphics import *

class Player:
    def __init__(self, userX, userY, imageLink, soundLink):
        #later can add more than 1 character (rn its just dog)
        self.x = userX
        self.y = userY
        self.imageLink = imageLink
        self.moveSound = soundLink
        self.width = 110 #size of image
        self.height = 95
        self.stepSize = 100
        self.playerMoveCount = 0 #terrain faster as more moves made per time frame
        self.speedDecay = 0.1
        self.hasMoved = False
        self.onBoat = False

    def collision(self, obstacle, newX, newY):
        marginOfError = 0
        # horizontal = (newX < obstacle.obstacleX + obstacle.width and newX + self.width - 100 > obstacle.obstacleX)
        # vertical = (newY < obstacle.obstacleY + obstacle.height and newY + self.height > obstacle.obstacleY)
        # return horizontal and vertical
        collides = (newX + marginOfError < obstacle.obstacleX + obstacle.width - marginOfError and 
                    newX + self.width - 90 > obstacle.obstacleX + marginOfError and
                    newY + marginOfError < obstacle.obstacleY + obstacle.height - marginOfError and 
                    newY + self.height - marginOfError > obstacle.obstacleY + marginOfError)    
        return collides
    
    def move(self, direction, canvasWidth, canvasHeight, terrain):
        newX, newY = self.x, self.y
        moved = False
        if direction == 'left' and self.x - 25 >= 0: # make sure no going off canvas
            newX-=self.stepSize
            moved = True
        if direction == 'right' and self.x + 25 + self.width <= canvasWidth: 
            newX+=self.stepSize
            moved = True
        if direction == 'up' and self.y - 25 >= 0: 
            newY-=self.stepSize
            moved = True
        if direction == 'down' and self.y + 25 + self.height <= canvasHeight: 
            newY+=self.stepSize
            moved = True

        block = terrain.getPlayerBlock(self, intendedY = newY)
        if block:
            for obs in block.obstacles:
                if obs.obstacleType == 'tree':
                    if self.collision(obs, newX, newY):
                        return  #just make sure no moving
        
        if moved:
            self.x, self.y = newX, newY
            self.moveSound.play(restart=False)
            self.playerMoveCount += 1
            self.hasMoved = True
    
    def updateBoat(self, boat):
        if boat and self.collision(boat, self.x, self.y):
            #if boat.direction > 0:
            self.x += boat.speed * boat.direction #maybe need to do speed * something like what boat starts out on
            self.onBoat=True

        else:
            self.onBoat = False

    # def decaySpeed(self):
    #     if self.playerMoveCount > 0 and not self.hasMoved:
    #         self.playerMoveCount -= self.speedDecayRate

    def draw(self):
        drawImage(self.imageLink, self.x, self.y, width = self.width, height = self.height)