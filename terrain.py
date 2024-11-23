from cmu_graphics import *
import random
from helpers import Helper
from player import Player

# TO DO: NEED TO MAKE SURE YOU START ON GRASS
#has diff sections - road, grass, water
#increase difficulty over time

obsTypes = {'road': 'cars', 'grass': ['trees', 'lectureHall'], 'water': ['logs', 'lilypads'], 'tracks': 'train'} #self.sectType to a certain obstacle
#can make it cmu themed like 61d bus lol
terrainColors = {'road': 'silver', 'grass': 'darkSeaGreen', 'water': 'skyBlue', 'tracks': 'dimGray'}
#need to: alternate grass colors, maybe lines between roads, maybe alternate water colors
#maybe use image for tracks

class TerrainSection:
    def __init__(self, sectType, sectY, blockHeight, screenWidth):
        self.sectType = sectType
        self.sectY = sectY #y coords of where it is
        self.blockHeight = blockHeight
        self.screenWidth = screenWidth
        #self.difficulty = #do later - has to do w/ # obstacles
        #self.obstacles = []

    def drawBlock(self):
        drawRect(0, self.sectY, self.screenWidth, self.blockHeight, fill = terrainColors[self.sectType])

    # def makeObstacles(self):
    #     for _ in range(self.difficulty):
    #         self.obstacles.append(Obstacle(type = obsType[self.sectType], x = randomPosition(), y = randomPosition()))

    # def drawObstacles(self):
    #     for obs in self.obstacles:
    #         #draw

    # def moveObstacles(self, speed):
    #     for obs in self.obstacles:
    #         obs.move(speed) #write a move thing to update coordinates

class randomGenerateTerrain:
    def __init__(self, screenHeight, screenWidth, blockHeight):
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.blockHeight = blockHeight
        #needs to have player position y
        self.terrainBlocks = []
        self.terrainStarted = False
        self.baseTerrainMoveSpeed = 1.2
        self.terrainMoveSpeed = self.baseTerrainMoveSpeed # start at 1.2, later when difficulty component added then change it to a slowly increasing terrainMoveSpeed
        self.slowDownRate = 0.1 #speed of terrain movement gradually decreases when player doesn't move
        self.generateInitialTerrain()

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
            terrType = random.choice(['road', 'grass', 'water', 'tracks'])
            sectY = self.screenHeight - (i+1)*self.blockHeight
            self.terrainBlocks.append(TerrainSection(terrType, sectY, self.blockHeight, self.screenWidth))
            
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
            return 
        
        targetY = self.screenHeight // 2 #area to keep player in - roughly middle
        veryTopY = self.blockHeight # keep area out of this area - speed up more when it is

        speedMultiplier = min(1 + player.playerMoveCount * 0.01, 2)  # max multiplier of 5

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

        #make sure centered once certain area reached
        #make sure moving fast enough so ideally top not reached
        if player.y < veryTopY + self.blockHeight:
            distanceFromVeryTop = max(veryTopY - player.y, 1)
            self.terrainMoveSpeed += self.terrainMoveSpeed * 0.01 + (1 / distanceFromVeryTop) * speedMultiplier
        elif player.y < targetY:
            distanceFromTarget = targetY - player.y
            self.terrainMoveSpeed += self.terrainMoveSpeed * (0.004 + distanceFromTarget/self.screenHeight) * speedMultiplier
        else: 
            self.terrainMoveSpeed -= self.terrainMoveSpeed * 0.002 # slow down when below middle
        
        if self.terrainMoveSpeed > self.baseTerrainMoveSpeed:
            self.terrainMoveSpeed += self.terrainMoveSpeed * 0.001

        #cap speed
        #self.terrainMoveSpeed = min(self.terrainMoveSpeed, 10)

        for block in self.terrainBlocks:
            block.sectY += self.terrainMoveSpeed
        
        # move player w curr block
        player.y = currBlock.sectY + (self.blockHeight // 2) - (player.height // 2)

        #remove blocks that are past
        self.terrainBlocks = [block for block in self.terrainBlocks if block.sectY < self.screenHeight]

        #check if at top
        while len(self.terrainBlocks) == 0 or self.terrainBlocks[-1].sectY >= 0:
            terrType = random.choice(['road', 'grass', 'water', 'tracks'])
            newBlock = TerrainSection(terrType, -self.blockHeight, self.blockHeight, self.screenWidth)
            self.terrainBlocks.append(newBlock)

        bottomBlock = self.terrainBlocks[0]
        for block in self.terrainBlocks:
            if block.sectY > bottomBlock.sectY:
                bottomBlock = block

        #check if player moved to bottom and will be scrolled past
        #need to fix logic
        for block in self.terrainBlocks:
            if bottomBlock and player.y + player.height > bottomBlock.sectY + self.blockHeight:
                Helper.printGameOver(app)

    def drawTerrain(self):
        for block in self.terrainBlocks:
            block.drawBlock()

        
