import heapq
from cmu_graphics import *
from time import time

#determine ai's move (shortest/fastest path to finish line)
class AIplayer:
    def __init__ (self, startX, startY, endX, endY, rightimageLink):
        self.imageLink = rightimageLink
        self.sX = startX
        self.sY = startY
        self.eX = endX
        self.eY = endY
        self.width = 110
        self.height = 95
        self.dimension = 800
        self.path = []
        self.lastMoved = time()
        self.stepsPerSec = 0.5 

    def collision(self, obstacle, newX, newY):
        marginOfError = 10
        collides = (newX + marginOfError < obstacle.obstacleX + obstacle.width - marginOfError and 
                    newX + self.width > obstacle.obstacleX + marginOfError and
                    newY + marginOfError < obstacle.obstacleY + obstacle.height - marginOfError and 
                    newY + self.height - marginOfError > obstacle.obstacleY + marginOfError)    
        return collides

    def updateBoat(self, boat, terrain):
        if boat and self.collision(boat, self.sX, self.sY):
            overlapXStart = max(self.sX, boat.obstacleX)
            overlapXEnd = min(self.sX + self.width, boat.obstacleX + boat.width)
            overlapWidth = max(0, overlapXEnd - overlapXStart)

            if overlapWidth >= (self.width / 2): 
                self.sX -= boat.totalDiff
                self.onBoat = True
            else:
                self.onBoat = False
                app.gameOver = True
            self.onBoat = False

    def calcH(self, x, y):
        return abs(x - self.eX) + abs(y - self.eY)
    
    def possibleMoves(self, x, y, terrain):
        neighbors = []
        possibleMoves = [(-50, 0), (50, 0), (0, -100), (0, 100)]
        for possibleX, possibleY in possibleMoves:
            newX, newY = x + possibleX, y + possibleY
            if 0 <= newX < self.dimension and 0 <= newY < self.dimension:
                block = terrain.getAIBlock(newY) # getPlayerBlock(self, player, intendedY=None):
                if block:
                    weight = 1  #default movement cost
                    collides = False
                    for obs in block.obstacles:
                        if obs.obstacleType == 'tree': 
                            if self.collision(obs, newX, newY):
                                collides = True
                                break
                        elif obs.obstacleType == 'boat': 
                            if self.collision(obs, newX, newY):
                                weight -= 1  
                                self.onBoat = True
                                break
                        if obs.obstacleType in ['car', 'train']:
                            if obs.impendingCollision((newX, newY)): #need to calc time + distance
                                weight = float('inf')  #completely avoid 
                                collides = True
                                break
                            elif obs.nearby((newX, newY)):
                                weight += 5  # ok for nodes near obstacles further away
                    if not collides:
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
        currTime = time()
        currBlock = terrain.getAIBlock(self.sY)
        if currTime - self.lastMoved >= self.stepsPerSec:
            if not self.path or not self.isValidPath(terrain):
                self.aStar(terrain) #recalculate path
            if self.path:
                newX, newY = self.path.pop(0)
                if currBlock:
                    for obs in currBlock.obstacles:
                        if obs.obstacleType == 'tree' and self.collision(obs, newX, newY):
                            return 
                        elif obs.obstacleType == 'boat' and self.collision(obs, newX, newY):
                            self.updateBoat(obs, terrain) 
                            break
                self.sX, self.sY = newX, newY
            self.lastMoved = currTime

    def draw(self):
        drawImage(self.imageLink, self.sX, self.sY, width = 110, height = 95)