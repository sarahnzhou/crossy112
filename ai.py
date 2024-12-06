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

    def calcH(self, x, y):
        return abs(x - self.eX) + abs(y - self.eY)
    
    def possibleMoves(self, x, y, terrain):
        neighbors = []
        possibleMoves = [(-50, 0), (50, 0), (0, -100), (0, 100)]
        # if 0 <= newX < self.dimension and 0 <= newY < self.dimension:
        for possibleX, possibleY in possibleMoves:
            newX, newY = x + possibleX, y + possibleY
            block = terrain.getAIBlock(newY)
            print(f"Checking new position: ({newX}, {newY}), Block: {block}")
            if block:
                weight = 1
                collides = False
                for obs in block.obstacles:
                    if obs.obstacleType == 'tree': 
                        print("hi tree")
                        if self.collision(obs, newX, newY):
                            print(f"Collision with tree at ({newX}, {newY})")
                            collides = True
                            break
                        else:
                            print("no collide tree")
                    elif obs.obstacleType == 'boat': 
                        print("hi boat")
                        if self.collision(obs, newX, newY):
                            weight -= 1  
                            self.onBoat = True
                            break
                    if obs.obstacleType in ['car', 'train']:
                        print(f"hi {obs.obstacleType}")
                        if obs.impendingCollision((newX, newY)): #need to calc time + distance
                            weight = float('inf')  #completely avoid 
                            print(f"Collision with car/train at ({newX}, {newY})")
                            collides = True
                            break
                        elif obs.nearby((newX, newY)):
                            weight += 5  # ok for nodes near obstacles further away
                if not collides and weight < float('inf'):
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
        print('using a star')
        start = (self.x, self.y)
        finish = (self.eX, self.eY)
        openList = []
        heapq.heappush(openList, (0, start))
        prevSteps = {}
        gCounts = {start: 0}
        fCounts = {start: self.calcH(self.x, self.y)}

        while openList:
            priority, current = heapq.heappop(openList) #get smallest fVal
            if current == finish:
                # reconstruct path
                self.path = []
                while current in prevSteps:
                    self.path.append(current)
                    current = prevSteps[current]
                self.path.reverse()
            
            print(self.path, "hi hih hi")

            currX, currY = current
            currG = gCounts[current]
            neighbors = self.possibleMoves(currX, currY, terrain)
            print("hi at neigbors")
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
        currTime = time()
        currBlock = terrain.getAIBlock(self.y)
        print(f"Current Block at Y={self.y}: {currBlock}")
        #if currTime - self.lastMoved >= 0.5:
        if not self.path or not self.isValidPath(terrain):
            self.aStar(terrain) #recalculate path
            print('recalculating')
        if self.path:
            print(f"Moving along path: {self.path}")
            newX, newY = self.path.pop(0)
            if currBlock:
                for obs in currBlock.obstacles:
                    if obs.obstacleType == 'tree' and self.collision(obs, newX, newY):
                        return 
                    elif obs.obstacleType == 'boat' and self.collision(obs, newX, newY):
                        self.updateBoat(obs, terrain) 
                        break
            self.x, self.y = newX, newY
        # else:
        #     print("No valid path found.")
        # self.lastMoved = currTime

    def draw(self):
        super().draw()