from cmu_graphics import *
import random
from helpers import Helper
from player import Player
from movingobjects import Obstacle

#obsTypes = {'road': 'car', 'grass': ['tree', 'lectureHall'], 'water': ['boat', 'lilypads'], 'tracks': 'train'} #self.sectType to a certain obstacle
obsTypes = {
    'road': ['car'], 
    'grass': ['tree'], 
    'water': ['boat'], 
    'tracks': ['train']
}
terrainColors = {
    'road': 'silver', 
    'grass': 'darkSeaGreen',
    'water': 'skyBlue', 
    'tracks': 'dimGray'
}
obsSizes = {
    'car': (100, 100), #width, height
    'tree': (50, 100),
    'train': (220, 100),
    'boat': (200, 100)
}
obsCounts = {
    'car': random.randint(1, 2),
    'tree': random.randint(1, 4),
    'train': 1,
    'boat': random.randint(2, 2)
}

class TerrainSection:
    def __init__(self, sectType, sectY, blockHeight, screenWidth, obsImages, terrainMoveSpeed):
        self.sectType = sectType
        self.sectY = sectY #y coords of where it is
        self.blockHeight = blockHeight
        self.screenWidth = screenWidth
        self.obsImages = obsImages
        #self.difficulty = #do later - has to do w/ # obstacles
        self.obstacles = []
        self.terrainMoveSpeed = terrainMoveSpeed
        self.direction = random.choice([-1, 1]) #can move left or right
        self.makeObstacles()

    def makeObstacles(self):
        playerStartingXs = [335, 150, 550] # account for AI + player in AI mode as well
        playerStartingY = 500
        typeO = random.choice(obsTypes[self.sectType]) #if isinstance(obsTypes[self.sectType], list) else obsTypes[self.sectType]
        count = obsCounts[typeO]
        width, height = obsSizes[typeO]
        #for _ in range(self.difficulty):
        for _ in range(count): #later associate self.difficulty with obsCount
            y = self.sectY
            x = self.getNoOverlapX(width)
            if typeO == 'tree' and (any(pStartX <= x <= pStartX + 100 for pStartX in playerStartingXs) and playerStartingY - 100<= y <= playerStartingY):
                continue
            self.obstacles.append(Obstacle(typeO, x, y, self.obsImages, self.direction, width, height))

    def getNoOverlapX(self, width):
        for _ in range(100):
            xOptions = []
            for i in range(self.screenWidth // 100):
                xOptions.append(50+i*100)
            x = random.choice(xOptions)
            if not any(self.isOverlapping(x, obs.obstacleX, width, obs.width) for obs in self.obstacles):
                return x
        return random.choice([i * 100 for i in range(self.screenWidth // 100)]) # just in case all 100 dont work

    def isOverlapping(self, x1, x2, w1, w2):
        return x1 < x2 + w2 and x2 < x1 + w1

    def drawBlock(self):
        drawRect(0, self.sectY, self.screenWidth, self.blockHeight+1, fill = terrainColors[self.sectType])
        self.drawObstacles()

    def drawObstacles(self):
        for obs in self.obstacles:
            obs.draw()

    def moveObstacles(self):
        for obs in self.obstacles:
            obs.move(self.terrainMoveSpeed)
            obs.obstacleY= self.sectY

class randomGenerateTerrain:
    #shared methods btwn AI + regular
    def __init__(self, screenHeight, screenWidth, obsImages):
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.obsImages = obsImages
        self.blockHeight = 100
        #needs to have player position y
        self.terrainBlocks = []
        self.terrainStarted = False
        self.obstaclesMoving = True
        self.baseTerrainMoveSpeed = 1.2
        self.terrainMoveSpeed = self.baseTerrainMoveSpeed # start at 1.2, later when difficulty component added then change it to a slowly increasing terrainMoveSpeed
        self.slowDownRate = 0.1 #speed of terrain movement gradually decreases when player doesn't move
        self.generateInitialTerrain()
        
    def updateObstacles(self):
        for block in self.terrainBlocks:
            block.moveObstacles()

    def generateInitialTerrain(self):
        numBlocks = self.screenHeight // self.blockHeight 
        for i in range(numBlocks):
            if i<3: #ensure always start on grass
                terrType = 'grass'
            else:
                terrType = random.choice(['road', 'grass', 'water', 'tracks'])
            sectY = self.screenHeight - (i+1)*self.blockHeight 
            self.terrainBlocks.append(TerrainSection(terrType, sectY, self.blockHeight, self.screenWidth, self.obsImages, self.terrainMoveSpeed))
            
    # make sure terrain blocks have no gaps
    def alignTerrainBlocks(self):
        for i in range(1, len(self.terrainBlocks)):
            self.terrainBlocks[i].sectY = self.terrainBlocks[i - 1].sectY - self.blockHeight

    def drawTerrain(self):
        for block in self.terrainBlocks:
            block.drawBlock()

    def getAIBlock(self, y):
        for block in self.terrainBlocks:
            if block.sectY <= y < block.sectY + self.blockHeight:
                return block
        return self.findClosestAIBlock(y)
    
    def findClosestAIBlock(self, y):
        closest = None
        smallestDistance = float('inf')  
        yPos = y * self.blockHeight

        for block in self.terrainBlocks:
            distance = abs(block.sectY - yPos)
            if distance < smallestDistance:
                smallestDistance = distance
                closest = block
        return closest

    #track which block the player is on so it can keep player on it
    def getPlayerBlock(self, player, intendedY=None):
        yPos = intendedY if intendedY is not None else player.y
        for block in self.terrainBlocks:
            if block.sectY <= yPos < block.sectY + self.blockHeight:
                return block
        return self.findClosestBlock(player)

    def findClosestBlock(self, player):
        closest = None
        smallestDistance =  float('inf')  # start with biggest distance
        for block in self.terrainBlocks:
            distance = abs(block.sectY - player.y)
            if distance < smallestDistance:
                smallestDistance = distance
                closest = block
        return closest
    
    def findNextBlock(self, player):
        for block in self.terrainBlocks:
            if block.sectY > player.y:
                return block
        return None
    
    def regularModeUpdateTerr(self, player):
        self.updateTerrain(player)
    
    def aiModeUpdateTerr(self, player, ai):
        self.updateTerrain(player, ai)
        # if either player "falls" off visible screen
        if player.y + player.height > self.screenHeight or ai.y  + 100 > self.screenHeight:
            app.gameOver = True
            self.terrainStarted = False
    
    def updateTerrain(self, player, ai = None):
        if not self.terrainStarted:
            return 
    
        player.onBoat = False
        if ai:
            ai.onBoat = False

        targetY = self.screenHeight // 2 #area to keep player in - roughly middle
        veryTopY = self.blockHeight # keep area out of this area - speed up more when it is

        # frequencyMultiplier = player.playerMoveCount * 0.01 # based on how frequent player moves
        # proximityMultiplier = max((veryTopY - player.y) / self.blockHeight, 0) # based on how close to top player gets when it makes moves more frequently
        # scalingFactor = 1 + frequencyMultiplier + (proximityMultiplier * 0.01) 

        frequencyMultiplier = player.playerMoveCount * 0.01 if not ai else max(player.playerMoveCount * 0.01, 0)
        proximityMultiplier = max((veryTopY - player.y) / self.blockHeight, 0) if not ai else max((veryTopY - player.y) / self.blockHeight, (veryTopY - ai.y) / self.blockHeight)
        scalingFactor = 1 + frequencyMultiplier + (proximityMultiplier * 0.01)

        if ai:
            currBlock = self.getPlayerBlock(player)
            currAIBlock = self.getAIBlock(ai.y)

            if currBlock:
                if currBlock.sectY <= player.y < currBlock.sectY + self.blockHeight:
                    player.y += self.terrainMoveSpeed 

            if currAIBlock:
                if currAIBlock.sectY <= ai.y * 100 < currAIBlock.sectY + self.blockHeight:
                    ai.y += self.terrainMoveSpeed
             
            
        else:
            currBlock = self.getPlayerBlock(player)
            if currBlock:
                if currBlock.sectY <= player.y < currBlock.sectY + self.blockHeight:
                    player.y += self.terrainMoveSpeed

        #determine how fast to move terrain
        closestY = min(player.y, ai.y) if ai else player.y
        if closestY < veryTopY + self.blockHeight:
            distanceFromVeryTop = max(veryTopY - closestY, 1)
            self.terrainMoveSpeed += (self.baseTerrainMoveSpeed * scalingFactor)/distanceFromVeryTop
        elif closestY < targetY:
            distanceFromTarget = targetY - closestY
            self.terrainMoveSpeed += (self.baseTerrainMoveSpeed * scalingFactor) * (distanceFromTarget/self.screenHeight)
        else:
            if self.terrainMoveSpeed >= 1.8:
                self.terrainMoveSpeed -= self.terrainMoveSpeed * 0.4 

        self.terrainMoveSpeed = min(self.terrainMoveSpeed, 15)

        for block in self.terrainBlocks:
            #if self.terrainStarted:
            block.sectY += self.terrainMoveSpeed
            block.moveObstacles()
            player.handleCollisions(block, self)

        # if ai:
        #     aiBlock = self.getAIBlock(ai.y)
        #     if aiBlock and aiBlock.sectType == 'water':
        #         boats = self.getAIBoats(ai)
        #         if not any(ai.collision(boat, ai.x, ai.y) for boat in boats):
        #             app.gameOver = True
        #             self.terrainStarted = False
        #             print("ai water")

        playerBlock = self.getPlayerBlock(player)
        if playerBlock:
            if playerBlock.sectY <= player.y < playerBlock.sectY + self.blockHeight:
                player.y += self.terrainMoveSpeed
            if playerBlock.sectType == 'water' and not player.onBoat:
                self.terrainStarted = False
                app.gameOver = True
                return 
        
        # move player w curr block
        player.y = currBlock.sectY + (self.blockHeight // 2) - (player.height // 2)

        #remove blocks that are past
        self.terrainBlocks = [block for block in self.terrainBlocks if block.sectY < self.screenHeight]

        #check if at top
        while len(self.terrainBlocks) == 0 or self.terrainBlocks[-1].sectY >= 0:
            terrType = random.choice(['road', 'grass', 'water', 'tracks'])
            newBlock = TerrainSection(terrType, -self.blockHeight, self.blockHeight, self.screenWidth, self.obsImages, self.terrainMoveSpeed)
            self.terrainBlocks.append(newBlock)

        self.alignTerrainBlocks()

        bottomBlock = self.terrainBlocks[0]
        for block in self.terrainBlocks:
            if block.sectY > bottomBlock.sectY:
                bottomBlock = block

        # check if player at bottom if so game over        
        if player.y + player.height > self.screenHeight or (ai and ai.y + 100 > self.screenHeight):
            app.gameOver = True
            self.terrainStarted = False  # Stop further terrain updates
    
    def getBoats(self, player):
        boats = []
        for block in self.terrainBlocks:
            if block.sectY <= player.y < block.sectY + block.blockHeight and block.sectType == 'water':
                for obs in block.obstacles:
                    if obs.obstacleType == 'boat': 
                        boats.append(obs)
        return boats
    
    def getAIBoats(self, ai):
        boats = []
        for block in self.terrainBlocks:
            if block.sectY <= ai.y < block.sectY + block.blockHeight and block.sectType == 'water':
                for obs in block.obstacles:
                    if obs.obstacleType == 'boat': 
                        boats.append(obs)
        return boats