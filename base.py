from cmu_graphics import *
class basePlayer:
    def __init__(self, x, y, rightImageLink, leftImageLink):
        self.x = x
        self.y = y
        self.rightImageLink = rightImageLink
        self.leftImageLink = leftImageLink
        self.imageLink = rightImageLink
        self.width = 110
        self.height = 95
        self.verticalstepSize = 100
        self.horizontalStepSize = 50
        self.onBoat = False

    def collision(self, obstacle, newX, newY):
        marginOfError = 10
        collides = (newX + marginOfError < obstacle.obstacleX + obstacle.width - marginOfError and 
                    newX + self.width > obstacle.obstacleX + marginOfError and
                    newY + marginOfError < obstacle.obstacleY + obstacle.height - marginOfError and 
                    newY + self.height - marginOfError > obstacle.obstacleY + marginOfError)    
        return collides
    
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