import heapq
from cmu_graphics import *

#determine ai's move (shortest/fastest path to finish line)
class AIplayer:
    def __init__ (self, startX, startY, endX, endY, rightimageLink):
        self.imageLink = rightimageLink
        self.sX = startX
        self.sY = startY
        self.eX = endX
        self.eY = endY
        self.dimension = 800
        self.path = []

    def calcH(self, x, y):
        return abs(x - self.eX) + abs(y - self.eY)
    
    def possibleMoves(self, x, y, terrain):
        neighbors = []
        possibleMoves = [(-50, 0), (50, 0), (0, -50), (0, 50)]
        for possibleX, possibleY in possibleMoves:
            newX, newY = x + possibleX, y + possibleY
            if 0 <= newX < self.dimension and 0 <= newY < self.dimension:
                block = terrain.getAIBlock(newY) # getPlayerBlock(self, player, intendedY=None):
                if block:
                    weight = 1  # Default movement cost
                    for obs in block.obstacles:
                        if obs.obstacleType in ['car', 'train']:
                            if obs.impendingCollision((newX, newY)): #need to calc time + distance
                                weight = float('inf')  # Completely avoid 
                            elif obs.nearby((newX, newY)):
                                weight += 5  # ok for nodes near obstacles further away
                    neighbors.append((newX, newY, weight))
        return neighbors

    def isValidPath(self, terrain):
        for x, y in self.path:
            block = terrain.getAIBlock(y)
            if not block or block.sectType == 'water': 
                return False
            for obs in block.obstacles:
                if obs.obstacleType in ['car', 'train'] and obs.impendingCollision((x, y)):
                    return False 
        return True

    def aStar(self, terrain):
        start = (self.sX, self.sY)
        finish = (self.eX, self.eY)
        openList = []
        heapq.heappush(openList, (0, start))
        prevSteps = {}
        gCounts = {start: 0}
        fCounts = {start: self.calcH(self.sX, self.sY)}

        while openList:
            priority, current = heapq.heappop(openList) #get smallest fVal
            if current == finish:
                # reconstruct path
                self.path = []
                while current in prevSteps:
                    self.path.append(current)
                    current = prevSteps[current]
                self.path.reverse()

            currG = gCounts[current]
            currX, currY = current
            neighbors = self.possibleMoves(currX, currY, terrain)
            for newX, newY, weight in neighbors:
                if weight == float('inf'):  #skip possible collisions
                    continue
                neighbor = (newX, newY)
                newG = currG + weight
                if neighbor not in gCounts or newG < gCounts[neighbor]:
                    prevSteps[neighbor] = current
                    gCounts[neighbor] = newG
                    fCounts[neighbor] = newG + self.calcH(newX, newY)
                    heapq.heappush(openList, (fCounts[neighbor], neighbor))

    def moveAI(self, terrain):
        if not self.path or not self.isValidPath(terrain):
            self.aStar(terrain) #recalculate path
        if self.path:
            self.sX, self.sY = self.path.pop(0)

    def draw(self):
        drawImage(self.imageLink, self.sX, self.sY, width = 110, height = 95)