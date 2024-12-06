from base import basePlayer
import heapq
from cmu_graphics import *
from time import time

class AIplayer(basePlayer):
    def __init__(self, startX, startY, endX, endY, rightimageLink, leftImageLink):
        super().__init__(startX, startY, rightimageLink, leftImageLink)
        self.imageLink = rightimageLink
        self.eX = endX
        self.eY = endY
        self.dimension = 800
        self.path = []
        self.lastMoved = time()

    def calcH(self, x, y):
        return abs(x - self.eX) + abs(y - self.eY)

    def evaluateCollisions(self, obs, coords, block=None):
        x, y = coords
        if self.collision(obs, x, y):
            return float('inf'), True 
        return 1, False

    def possibleMoves(self, x, y, terrain):
        neighbors = []
        possibleMoves = [(-50, 0), (50, 0), (0, -100), (0, 100)] 

        for dx, dy in possibleMoves:
            newX, newY = x + dx, y + dy
            if 0 <= newX < self.dimension and 0 <= newY < self.dimension:
                block = terrain.getAIBlock(newY)
                if block:
                    totalWeight = 1
                    collides = False
                    for obs in block.obstacles:
                        weight, collides = self.evaluateCollisions(obs, (newX, newY), block)
                        if collides:
                            totalWeight = float('inf')
                            break 
                        totalWeight += weight
                    if totalWeight < float('inf'):
                        neighbors.append((newX, newY, totalWeight))
        return neighbors

    def aStar(self, terrain):
        openList = []
        closedSet = set()
        heapq.heappush(openList, (0, (self.x, self.y)))
        prevSteps = {}
        gCounts = {(self.x, self.y): 0}
        fCounts = {(self.x, self.y): self.calcH(self.x, self.y)}

        while openList:
            _, current = heapq.heappop(openList)

            if current in closedSet:
                continue

            if current == (self.eX, self.eY):
                self.path = []
                while current in prevSteps:
                    self.path.append(current)
                    current = prevSteps[current]
                self.path.reverse()
                return

            closedSet.add(current)
            currX, currY = current
            neighbors = self.possibleMoves(currX, currY, terrain)
            for newX, newY, weight in neighbors:
                if weight == float('inf'):
                    continue 

                neighbor = (newX, newY)
                newG = gCounts[current] + weight

                if neighbor not in gCounts or newG < gCounts[neighbor]:
                    prevSteps[neighbor] = current
                    gCounts[neighbor] = newG
                    fCounts[neighbor] = newG + self.calcH(newX, newY)
                    heapq.heappush(openList, (fCounts[neighbor], neighbor))

    def moveAI(self, terrain):
        currTime = time()
        currBlock = terrain.getAIBlock(self.y)
        if currBlock:
            if currBlock.sectType != 'water': 
                self.y = currBlock.sectY + (currBlock.blockHeight // 2) - (self.height // 2)
            elif currBlock.sectType == 'water' and self.onBoat: 
                for obs in currBlock.obstacles:
                    if obs.obstacleType == 'boat' and self.collision(obs, self.x, self.y):
                        self.x -= obs.totalDiff 
                        break

        if currTime - self.lastMoved >= 3:
            if not self.path:
                self.aStar(terrain)
                if not self.path:
                    return

            if self.path:
                newX, newY = self.path.pop(0)
                self.x, self.y = newX, newY
        self.lastMoved = currTime

    def draw(self):
        super().draw()