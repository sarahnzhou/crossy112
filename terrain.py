from cmu_graphics import *
import random
from helpers import Helper
from player import Player
from movingobjects import Obstacle

# TO DO: 
#has diff sections - road, grass, water
#increase difficulty over time

obsTypes = {'road': ['car'], 'grass': ['tree'], 'water': ['boat'], 'tracks': ['train']}
#obsTypes = {'road': 'car', 'grass': ['tree', 'lectureHall'], 'water': ['boat', 'lilypads'], 'tracks': 'train'} #self.sectType to a certain obstacle
#can make it cmu themed like 61d bus lol
terrainColors = {'road': 'silver', 'grass': 'darkSeaGreen', 'water': 'skyBlue', 'tracks': 'dimGray'}
#need to: alternate grass colors, maybe lines between roads, maybe alternate water colors
#maybe use image for tracks
#need to make some types more frequent

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
        playerStartingX = 335
        playerStartingY = 700
        #for _ in range(self.difficulty):
        obsCount = random.randint(1, 3)
        for _ in range(obsCount): #later associate self.difficulty with obsCount
            #print(obsTypes)
            typeO = random.choice(obsTypes[self.sectType]) #if isinstance(obsTypes[self.sectType], list) else obsTypes[self.sectType]
            y = self.sectY
            x = self.getNoOverlapX()
            if typeO == 'tree' and (playerStartingX - 100 <= x <= playerStartingX + 100 and playerStartingY - 50 <= y <= playerStartingY + 50):
                continue
            self.obstacles.append(Obstacle(typeO, x, y, self.obsImages, self.direction))

    def getNoOverlapX(self):
        for _ in range(100):
            x = Helper.randomPosition()
            if not any(self.isOverlapping(x, obs.obstacleX) for obs in self.obstacles):
                return x

    def isOverlapping(self, x1, x2):
        return abs(x1 - x2) < 100 # 100 is object width

    def drawBlock(self):
        #drawImage(self.obsImages['car'], 300, 300)
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
    def __init__(self, screenHeight, screenWidth, obsImages):
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.obsImages = obsImages
        self.blockHeight = 100
        #needs to have player position y
        self.terrainBlocks = []
        self.terrainStarted = False
        self.baseTerrainMoveSpeed = 1.2
        self.terrainMoveSpeed = self.baseTerrainMoveSpeed # start at 1.2, later when difficulty component added then change it to a slowly increasing terrainMoveSpeed
        self.slowDownRate = 0.1 #speed of terrain movement gradually decreases when player doesn't move
        self.generateInitialTerrain()

    def updateObstacles(self):
        for block in self.terrainBlocks:
            block.moveObstacles()

    #track which block the player is on so it can keep player on it
    def getPlayerBlock(self, player):
        for block in self.terrainBlocks:
            if block.sectY <= player.y < block.sectY + self.blockHeight:
                return block
        return None
    
    def findNextBlock(self, player):
        for block in self.terrainBlocks:
            if block.sectY > player.y:
                return block
        return None

    def generateInitialTerrain(self):
        numBlocks = self.screenHeight // self.blockHeight
        for i in range(numBlocks):
            if i == 0: #ensure always start on grass
                terrType = 'grass'
            else:
                terrType = random.choice(['road', 'grass', 'water', 'tracks'])
            sectY = self.screenHeight - (i+1)*self.blockHeight 
            self.terrainBlocks.append(TerrainSection(terrType, sectY, self.blockHeight, self.screenWidth, self.obsImages, self.terrainMoveSpeed))
            
    def findClosestBlock(self, player):
        closest = None
        smallestDistance =  float('inf')  # start with biggest distance
        for block in self.terrainBlocks:
            distance = abs(block.sectY - player.y)
            if distance < smallestDistance:
                smallestDistance = distance
                closest = block
        return closest
    
    def updateTerrain(self, player):
        if not self.terrainStarted:
            #self.terrainStarted = True
            return 
        
        player.onBoat = False

        targetY = self.screenHeight // 2 #area to keep player in - roughly middle
        veryTopY = self.blockHeight # keep area out of this area - speed up more when it is

        frequencyMultiplier = player.playerMoveCount * 0.01 # based on how frequent player moves
        proximityMultiplier = max((veryTopY - player.y) / self.blockHeight, 0) # based on how close to top player gets when it makes moves more frequently
        scalingFactor = 1 + frequencyMultiplier + (proximityMultiplier * 0.01) 

        currBlock = self.getPlayerBlock(player)

        # if not currBlock: # if not centered on a block find 'closest' block / aka block itself but right
        #     currBlock = self.findClosestBlock(player)

        # align position to terrain blocks so it moves together
        if currBlock:
            player.y = currBlock.sectY + (self.blockHeight // 2) - (player.height // 2)
        else:
            nextBlock = self.findNextBlock(player)
            if nextBlock:
                player.y = nextBlock.sectY + (self.blockHeight // 2) - (player.height // 2)

        #make sure moving fast enough so ideally top not reached
        if player.y < veryTopY + self.blockHeight:
            distanceFromVeryTop = max(veryTopY - player.y, 1)
            self.terrainMoveSpeed += (self.baseTerrainMoveSpeed * scalingFactor) / distanceFromVeryTop
        elif player.y < targetY:
            distanceFromTarget = targetY - player.y
            self.terrainMoveSpeed += (self.baseTerrainMoveSpeed * scalingFactor) * (distanceFromTarget / self.screenHeight)
        else: 
            if self.terrainMoveSpeed >= 1.8:
                self.terrainMoveSpeed -= self.terrainMoveSpeed * 0.3 # slow down when below middle
        
        #cap speed
        self.terrainMoveSpeed = min(self.terrainMoveSpeed, 20)

        for block in self.terrainBlocks:
            block.moveObstacles()
            for obs in block.obstacles:
                if obs.collision(player):
                    if obs.obstacleType in ['car', 'train']:
                        self.terrainStarted = False
                        app.gameOver = True
                        return
                    elif obs.obstacleType == 'boat':
                        player.updateBoat(obs)        
        block.sectY += self.terrainMoveSpeed

        playerBlock = self.getPlayerBlock(player)
        if playerBlock and playerBlock.sectType == 'water' and not player.onBoat:
            self.terrainStarted = False
            app.gameOver = True        
        
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
        if player.y + player.height > self.screenHeight:
            Helper.printGameOver(app)
            self.terrainStarted = False  # Stop further terrain updates
    
    # make sure terrain blocks have no gaps
    def alignTerrainBlocks(self):
        for i in range(1, len(self.terrainBlocks)):
            self.terrainBlocks[i].sectY = self.terrainBlocks[i - 1].sectY - self.blockHeight

    def drawTerrain(self):
        for block in self.terrainBlocks:
            block.drawBlock()