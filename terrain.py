from cmu_graphics import *
import random
from helpers import Helper
from player import Player

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
    def __init__(self, screenHeight, screenWidth, blockHeight, playerInfo):
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.blockHeight = blockHeight
        self.playerInfo = playerInfo
        #needs to have player position y
        self.terrainBlocks = []
        self.terrainStarted = False
        self.terrainMoveSpeed = 1 # start at 3, later when difficulty component added then change it to a slowly increasing terrainMoveSpeed

        self.generateInitialTerrain()

    #track which block the player is on so it can keep player on it
    def getPlayerBlock(self):
        for block in self.terrainBlocks:
            if block.sectY <= self.playerInfo.y < block.sectY + self.blockHeight:
                return block

    def generateInitialTerrain(self):
        numBlocks = self.screenHeight // self.blockHeight 
        for i in range(numBlocks):
            terrType = random.choice(['road', 'grass', 'water', 'tracks'])
            sectY = self.screenHeight - (i+1)*self.blockHeight
            self.terrainBlocks.append(TerrainSection(terrType, sectY, self.blockHeight, self.screenWidth))
            
    def updateTerrain(self):
        if not self.terrainStarted:
            return 
        
        currBlock = self.getPlayerBlock()

        for block in self.terrainBlocks:
            block.sectY += self.terrainMoveSpeed

        if currBlock:
            self.playerInfo.y += self.terrainMoveSpeed
        #remove blocks that are past
        self.terrainBlocks = [block for block in self.terrainBlocks if block.sectY < self.screenHeight]

        #check if at top
        if len(self.terrainBlocks) == 0 or self.terrainBlocks[-1].sectY >= self.blockHeight:
            terrType = random.choice(['road', 'grass', 'water', 'tracks'])
            newBlock = TerrainSection(terrType, -self.blockHeight, self.blockHeight, self.screenWidth)
            self.terrainBlocks.append(newBlock)

        bottomBlock = None
        for block in self.terrainBlocks:
            if bottomBlock is None or block.sectY > bottomBlock.sectY:
                bottomBlock = block

        #check if player moved to bottom and will be scrolled past
        #need to fix logic
        for block in self.terrainBlocks:
            if bottomBlock and self.playerInfo.y + self.playerInfo.height > bottomBlock.sectY:
                Helper.printGameOver(app)

    def drawTerrain(self):
        for block in self.terrainBlocks:
            block.drawBlock()

        
