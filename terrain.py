#terrain generator (random)
#has diff sections - road, grass, water
#increase difficulty over time

obs = {'road': 'cars', 'grass': 'trees', 'water': 'logs'} #self.sectType to a certain obstacle

class TerrainSection:
    def __init__(self, sectType, sectY, difficulty):
        self.sectType = sectType
        self.sectY = sectY
        self.difficulty = difficulty
        self.obstacles = []

    def makeObstacles(self):
        for _ in range(self.difficulty):
            self.obstacles.append(Obstacle(type = obs[self.sectType], x = randomPosition(), y = randomPosition()))

    def drawObstacles(self):
        for obs in self.obstacles:
            #draw

    def moveObstacles(self, speed):
        for obs in self.obstacles:
            obs.move(speed) #write a move thing to update coordinates