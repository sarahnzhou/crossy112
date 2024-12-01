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
        self.horizontalStepSize = 50
        self.playerMoveCount = 0 #terrain faster as more moves made per time frame
        self.speedDecay = 0.1
        self.hasMoved = False
        self.onBoat = False
        #self.boat = None

    def collision(self, obstacle, newX, newY):
        marginOfError = 10
        collides = (newX + marginOfError < obstacle.obstacleX + obstacle.width - marginOfError and 
                    newX + self.width > obstacle.obstacleX + marginOfError and
                    newY + marginOfError < obstacle.obstacleY + obstacle.height - marginOfError and 
                    newY + self.height - marginOfError > obstacle.obstacleY + marginOfError)    
        return collides
    
    def snapToGrid(self, xCoord, gridSize):
        #grid size player step size for now - 50
        return rounded(xCoord/50)*50

    def move(self, direction, canvasWidth, canvasHeight, terrain, gridSize = 50):
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
                    self.updateBoat(obs, terrain)
        
        if moved:
            self.x = self.snapToGrid(newX, gridSize)
            self.y = newY
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
                        self.updateBoat(obs, terrain)   

    def isNearOtherBoats(self, currBoat, otherBoats): # can jump to other boats
        for otherBoat in otherBoats:
            if otherBoat != currBoat:
                if self.x + self.width > otherBoat.obstacleX and self.x < otherBoat.obstacleX + otherBoat.width:
                    return True
        return False  
    
    def playerPercentInWater(self, boat, otherBoats):
        overlapXStart = max(self.x, boat.obstacleX)
        overlapXEnd = min(self.x + self.width, boat.obstacleX + boat.width)
        overlapWidth = max(0, overlapXEnd - overlapXStart)
        
        leftHangingStart = self.x
        leftHangingEnd = overlapXStart
        rightHangingStart = overlapXEnd
        rightHangingEnd = self.x + self.width

        if overlapWidth >= (self.width / 2):
            return False

        # Check if hanging regions overlap with other boats
        for otherBoat in otherBoats:
            if otherBoat != boat:
                if (leftHangingStart < otherBoat.obstacleX + otherBoat.width and leftHangingEnd > otherBoat.obstacleX) or \
                (rightHangingStart < otherBoat.obstacleX + otherBoat.width and rightHangingEnd > otherBoat.obstacleX):
                    return False  # Hanging region is over another boat

        # If no overlap with other boats, the player is in water
        return True
        
    def hangingRegion(self, startX, endX, otherBoats, currBoat):
        for other in otherBoats:
            if other != currBoat:
                if startX < other.obstacleX + other.width and endX > other.obstacleX:
                    return False #overlap other boat
        return True #overlap water

    def updateBoat(self, boat, terrain):
        if boat and self.collision(boat, self.x, self.y):
            overlapXStart = max(self.x, boat.obstacleX)
            overlapXEnd = min(self.x + self.width, boat.obstacleX + boat.width)
            overlapWidth = max(0, overlapXEnd - overlapXStart)

            if overlapWidth >= (self.width / 2):
                self.x -= boat.totalDiff
                self.onBoat=True

                otherBoats = terrain.getBoats(self)
                if self.playerPercentInWater(boat, otherBoats):
                    if not self.isNearOtherBoats(boat, otherBoats):
                        self.onBoat = False
                        app.gameOver = True
            else:
                otherBoats = terrain.getBoats(self)
                if not self.isNearOtherBoats(boat, otherBoats): 
                    self.onBoat = False
                    app.gameOver = True
        else:
            self.onBoat = False
            currBlock = terrain.getPlayerBlock(self)
            if currBlock and currBlock.sectType not in ['water']:
                self.snapToGrid(self.x, 50)
            else:
                self.onBoat = True

    def draw(self):
        drawImage(self.imageLink, self.x, self.y, width = self.width, height = self.height)