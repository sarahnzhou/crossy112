from base import basePlayer
import heapq
from cmu_graphics import *
from time import time

#determine ai's move (shortest/fastest path to finish line)
class AIplayer(basePlayer):
    def __init__ (self, startX, startY, endX, endY, rightimageLink, leftImageLink):
        super().__init__(startX, startY, rightimageLink, leftImageLink)
        self.imageLink = rightimageLink
        self.eX = endX
        self.eY = endY
        self.dimension = 800
        self.path = []
        self.lastMoved = time()
        self.isMoving = False

    def calcH(self, x, y):
        return abs(x - self.eX) + abs(y - self.eY)
    
    def evaluateCollisions(self, obs, coords, block=None):
        x, y = coords
        if block and block.sectType == 'water':
            if obs.obstacleType == 'boat' and self.collision(obs, x, y):
                return -1, False
            elif obs.obstacleType == 'boat':
                return 10, False
            return float('inf'), True

        if obs.obstacleType == 'tree':
            if self.collision(obs, x, y):
                return float('inf'), True
            #return float('inf'), True
        if obs.obstacleType in ['car', 'train']:
            if obs.collisionSoon((x, y), 3):
                return float('inf'), True
            if obs.collisionSoon((x, y), 5):
                return 5, False
        return 1, False

    def possibleMoves(self, x, y, terrain):
        neighbors = []
        possibleMoves = [(-50, 0), (50, 0), (0, -100), (0, 100)]
        for dx, dy in possibleMoves:
            newX, newY = x + dx, y + dy
            if 0 <= newX < self.dimension and 0 <= newY < self.dimension:
                block = terrain.getAIBlock(newY)
                print(f"Checking new position: ({newX}, {newY}), Block: {block}")
                if block:
                    totalWeight = 1
                    collides = False
                    for obs in block.obstacles:
                        print(f"Checking obstacle: {obs.obstacleType} at ({obs.obstacleX}, {obs.obstacleY})")
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
       # self.path = []  # Clear the path if no valid route is found

    def moveAI(self, terrain):
        self.isMoving = True
        currTime = time()
        currBlock = terrain.getAIBlock(self.y)
        print(f"Current Block at Y={self.y}: {currBlock}")
        if currTime - self.lastMoved >= 0.5:
            if not self.path:
                self.aStar(terrain)
                print('recalculating')
            if self.path:
                print(f"Moving along path: {self.path}")
                newX, newY = self.path.pop(0)
                if currBlock:
                    for obs in currBlock.obstacles:
                        weight, collision = self.evaluateCollisions(obs, (newX, newY), currBlock)
                        if collision:
                            self.aStar(terrain)
                            return
                self.x, self.y = newX, newY
            self.isMoving = False
            self.lastMoved = currTime

    def draw(self):
        super().draw()