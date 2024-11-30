from cmu_graphics import *

class Player:
    def __init__(self, userX, userY, rightimageLink, leftimageLink, soundLink):
        self.x = userX
        self.y = userY
        self.imageLink = rightimageLink
        self.leftimageLink = leftimageLink
        self.rightimageLink = rightimageLink
        self.moveSound = soundLink
        self.width = 110 #size of image
        self.height = 95
        self.verticalstepSize = 100
        self.horizontalStepSize = 25
        self.playerMoveCount = 0 #terrain faster as more moves made per time frame
        self.speedDecay = 0.1
        self.hasMoved = False
        self.onBoat = False
        #self.boat = None

    def collision(self, obstacle, newX, newY):
        marginOfError = 0
        # horizontal = (newX < obstacle.obstacleX + obstacle.width and newX + self.width - 100 > obstacle.obstacleX)
        # vertical = (newY < obstacle.obstacleY + obstacle.height and newY + self.height > obstacle.obstacleY)
        # return horizontal and vertical
        collides = (newX + marginOfError < obstacle.obstacleX + obstacle.width - marginOfError and 
                    newX + self.width > obstacle.obstacleX + marginOfError and
                    newY + marginOfError < obstacle.obstacleY + obstacle.height - marginOfError and 
                    newY + self.height - marginOfError > obstacle.obstacleY + marginOfError)    
        return collides
    
    def move(self, direction, canvasWidth, canvasHeight, terrain):
        newX, newY = self.x, self.y
        self.prevX = self.x
        moved = False
        if direction == 'left' and self.x - 25 >= 0: # make sure no going off canvas
            newX-=self.horizontalStepSize
            self.imageLink = self.leftimageLink
            moved = True
        if direction == 'right' and self.x + 25 + self.width <= canvasWidth: 
            newX+=self.horizontalStepSize
            self.imageLink = self.rightimageLink
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
                    self.updateBoat(obs)
        
        if moved:
            self.x, self.y = newX, newY
            self.moveSound.play(restart=False)
            self.playerMoveCount += 1
            self.hasMoved = True
            return True
    
    def handleCollisions(self, block, terrain):
        for obs in block.obstacles:
                if self.collision(obs, self.x, self.y):
                    print(f"Collision detected with {obs.obstacleType} at ({obs.obstacleX}, {obs.obstacleY})")
                    if obs.obstacleType in ['car', 'train']:
                        print("Game Over: Hit a car or train.")
                        terrain.terrainStarted = False
                        app.gameOver = True
                        return
                    elif obs.obstacleType == 'boat':
                        self.updateBoat(obs)        

    def updateBoat(self, boat):
        if boat and self.collision(boat, self.x, self.y):
            self.x -= boat.totalDiff
            self.onBoat=True
        else:
            self.onBoat = False

    def draw(self):
        drawImage(self.imageLink, self.x, self.y, width = self.width, height = self.height)