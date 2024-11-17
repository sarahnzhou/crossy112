from cmu_graphics import *
#terrain generator (random)
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
        drawRect(0, sectY, self.screenWidth, self.blockHeight, fill = terrainColors[self.sectType])

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
    def __init__(self, screenHeight, screenWidth, blockHeight, playerInfo, terrainMoveSpeed):
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.blockHeight = blockHeight
        self.playerInfo = playerInfo
        #needs to have player position y
        self.terrainBlocks = []
        self.terrainMoveSpeed = 2 # start at 3, later when difficulty component added then change it to a slowly increasing terrainMoveSpeed
        self.maxStopTime = 100

        self.generateInitialTerrain()

    def generateInitialTerrain(self):
        numBlocks = self.screenHeight // TerrainSection.blockHeight 
        for i in range(numBlocks):
            terrType = random.choice['road', 'grass', 'water', 'tracks']
            yPos = self.screenHeight - (i+1)*TerrainSection.blockHeight
            self.terrainBlocks.append(TerrainSection(terrType, yPos, self.blockHeight, self.screenWidth))
            
    def updateTerrain(self):
        for block in self.terrainBlocks:
            block.yPos += self.terrainMoveSpeed

        #remove blocks that are past
        self.terrainBlocks = [block for block in self.terrainBlocks if block.yPos < self.screenHeight]

        #check if at top
        if len(self.terrainBlocks) == 0 or self.terrain_blocks[-1].y_position >= self.block_height:
            terrType = random.choice['road', 'grass', 'water', 'tracks']
            newBlock = TerrainSection(terrType, -self.blockHeight, self.blockHeight, self.screenWidth)
            self.terrainBlocks.append(newBlock)

        for block in self.terrainBlocks:
            if block.yPos + block.blockHeight >= self.playerInfo.posY:
                self.gameOver()

    def drawTerrain(self):
        for block in self.terrainBlocks:
            block.drawBlock()

    def gameOver():
        print("Game Over") # can later rework game over to reset coordinates and generate new map
        app.stop()

        
