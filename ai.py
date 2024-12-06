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
    
    # def evaluateCollisions(self, obs, coords, block = None):
    #     x, y = coords 
    #     if block and block.sectType == 'water':
    #         if obs.obstacleType == 'boat' and obs.collisionSoon((x, y), 3):
    #             return -1, False  
    #         else:
    #             return float('inf'), True #no boat in water dont go yet
    #     if obs.obstacleType == 'tree':
    #         if obs.collisionSoon((x, y), 0):
    #             return float('inf'), True
    #     if obs.obstacleType in ['car', 'train']:
    #         if obs.collisionSoon((x, y), 3): #almost immediate collision
    #             return float('inf'), True
    #         elif obs.collisionSoon((x, y), 5): #nearby
    #             return 5, False 
    #     return 1, False
    
    # def possibleMoves(self, x, y, terrain):
    #     neighbors = []
    #     possibleMoves = [(-50, 0), (50, 0), (0, -100), (0, 100)]
    #     for possibleX, possibleY in possibleMoves:
    #         newX, newY = x + possibleX, y + possibleY
    #         if 0 <= newX < self.dimension and 0 <= newY < self.dimension:
    #             block = terrain.getAIBlock(newY)
    #             print(f"Checking new position: ({newX}, {newY}), Block: {block}")
    #             if block:
    #                 totalWeight = 1
    #                 collides = False
    #                 for obs in block.obstacles:
    #                     print(f"Checking obstacle: {obs.obstacleType} at ({obs.obstacleX}, {obs.obstacleY})")
    #                     weight, collides = self.evaluateCollisions(obs, (newX, newY), block)
    #                     totalWeight+=weight
    #                     if collides:
    #                         break
    #                 if not collides: #and totalWeight < float('inf'):
    #                     neighbors.append((newX, newY, totalWeight))
    #     return neighbors
    # 
    def evaluateCollisions(self, obs, coords, block=None):
        x, y = coords
        if block and block.sectType == 'water':
            if obs.obstacleType == 'boat' and self.collision(obs, x, y):
                return -1, False  # Encourage moving onto the boat
            elif obs.obstacleType == 'boat':
                return 10, False  # Penalize without a boat
            return float('inf'), True  # Avoid water otherwise

        if obs.obstacleType == 'tree':
            if self.collision(obs, x, y):
                return float('inf'), True  # Completely avoid trees

        if obs.obstacleType in ['car', 'train']:
            if obs.collisionSoon((x, y), 3):
                return float('inf'), True  # Immediate collision
            if obs.collisionSoon((x, y), 5):
                return 5, False  # Penalize but allow
        return 1, False  # Default: no collision


    def possibleMoves(self, x, y, terrain):
        neighbors = []
        possibleMoves = [(-50, 0), (50, 0), (0, -100), (0, 100)]  # Possible movement directions
        for dx, dy in possibleMoves:
            newX, newY = x + dx, y + dy
            if 0 <= newX < self.dimension and 0 <= newY < self.dimension:
                block = terrain.getAIBlock(newY)
                print(f"Checking new position: ({newX}, {newY}), Block: {block}")
                if block:
                    totalWeight = 1  # Default weight for normal movement
                    collides = False
                    for obs in block.obstacles:
                        print(f"Checking obstacle: {obs.obstacleType} at ({obs.obstacleX}, {obs.obstacleY})")
                        weight, collides = self.evaluateCollisions(obs, (newX, newY), block)
                        if collides:
                            totalWeight = float('inf')  # If a collision occurs, mark as impassable
                            break
                        totalWeight += weight  # Accumulate weight for obstacles
                    if totalWeight < float('inf'):  # Add as a valid move if not completely blocked
                        neighbors.append((newX, newY, totalWeight))
        return neighbors

    # #works
    # def aStar(self, terrain):
    #     print("Starting A* algorithm")
    #     start = (self.x, self.y)
    #     finish = (self.eX, self.eY)

    #     openList = []
    #     heapq.heappush(openList, (0, start))  # Priority queue with f-value
    #     prevSteps = {}
    #     gCounts = {start: 0}  # Cost from start to the current node
    #     fCounts = {start: self.calcH(self.x, self.y)}  # Estimated cost from start to finish

    #     while openList:
    #         priority, current = heapq.heappop(openList)  # Get the node with the smallest f-value
    #         print(f"Processing node: {current} with priority {priority}")

    #         if current == finish:
    #             print("Path to finish found!")
    #             self.path = []
    #             while current in prevSteps:
    #                 self.path.append(current)
    #                 current = prevSteps[current]
    #             self.path.reverse()
    #             print(f"Reconstructed path: {self.path}")
    #             return  # Exit once the path is reconstructed

    #         currX, currY = current
    #         currG = gCounts[current]

    #         neighbors = self.possibleMoves(currX, currY, terrain)
    #         print(f"Neighbors for ({currX}, {currY}): {neighbors}")

    #         for newX, newY, weight in neighbors:
    #             if weight == float('inf'):  # Skip impassable nodes
    #                 continue
    #             neighbor = (newX, newY)
    #             newG = currG + weight
    #             if neighbor not in gCounts or newG < gCounts[neighbor]:
    #                 prevSteps[neighbor] = current
    #                 gCounts[neighbor] = newG
    #                 fCounts[neighbor] = newG + self.calcH(newX, newY)
    #                 heapq.heappush(openList, (fCounts[neighbor], neighbor))
    #                 print(f"Added {neighbor} to openList with f-value {fCounts[neighbor]}")

    def aStar(self, terrain):
        openList = []
        closedSet = set()
        heapq.heappush(openList, (0, (self.x, self.y)))  # Priority queue with (f-value, position)
        prevSteps = {}
        gCounts = {(self.x, self.y): 0}  # Cost from start
        fCounts = {(self.x, self.y): self.calcH(self.x, self.y)}  # Total estimated cost

        while openList:
            _, current = heapq.heappop(openList)

            if current in closedSet:
                continue  # Skip already processed nodes

            if current == (self.eX, self.eY):  # Reached destination
                self.path = []
                while current in prevSteps:
                    self.path.append(current)
                    current = prevSteps[current]
                self.path.reverse()
                return

            closedSet.add(current)  # Mark node as processed
            currX, currY = current

            neighbors = self.possibleMoves(currX, currY, terrain)
            for newX, newY, weight in neighbors:
                if weight == float('inf'):
                    continue  # Skip impassable nodes

                neighbor = (newX, newY)
                newG = gCounts[current] + weight

                if neighbor not in gCounts or newG < gCounts[neighbor]:
                    prevSteps[neighbor] = current
                    gCounts[neighbor] = newG
                    fCounts[neighbor] = newG + self.calcH(newX, newY)
                    heapq.heappush(openList, (fCounts[neighbor], neighbor))


        #print("No path found")
       # self.path = []  # Clear the path if no valid route is found


    # def aStar(self, terrain):
    #     print('using a star')
    #     start = (self.x, self.y)
    #     finish = (self.eX, self.eY)
    #     openList = []
    #     heapq.heappush(openList, (0, start))
    #     prevSteps = {}
    #     gCounts = {start: 0}
    #     fCounts = {start: self.calcH(self.x, self.y)}

    #     while openList:
    #         priority, current = heapq.heappop(openList) #get smallest fVal
    #         if current == finish:
    #             # reconstruct path
    #             self.path = []
    #             while current in prevSteps:
    #                 self.path.append(current)
    #                 current = prevSteps[current]
    #             self.path.reverse()
    #             return
            
    #         print(self.path, "hi hih hi")

    #         currG = gCounts[current]
    #         currX, currY = current
    #         neighbors = self.possibleMoves(currX, currY, terrain)
    #         print("hi at neigbors")
    #         for newX, newY, weight in neighbors:
    #             if weight == float('inf'):  #skip possible collisions
    #                 continue
    #             neighbor = (newX, newY)
    #             newG = currG + weight
    #             if neighbor not in gCounts or newG < gCounts[neighbor]:
    #                 prevSteps[neighbor] = current
    #                 gCounts[neighbor] = newG
    #                 fCounts[neighbor] = newG + self.calcH(newX, newY)
    #                 heapq.heappush(openList, (fCounts[neighbor], neighbor))

    def moveAI(self, terrain):
        currTime = time()
        currBlock = terrain.getAIBlock(self.y)
        print(f"Current Block at Y={self.y}: {currBlock}")
        if currTime - self.lastMoved >= 0.5:
            if not self.path:
                self.aStar(terrain) #recalculate path
                print('recalculating')
            if self.path:
                print(f"Moving along path: {self.path}")
                newX, newY = self.path.pop(0)
                if currBlock:
                    for obs in currBlock.obstacles:
                        weight, collision = self.evaluateCollisions(obs, (newX, newY), currBlock)
                        if collision:
                            self.aStar(terrain)  # Recalculate path
                            return
                        # if obs.obstacleType == 'tree' and self.collision(obs, newX, newY):
                        #     return 
                        # elif obs.obstacleType == 'boat' and self.collision(obs, newX, newY):
                        #     self.updateBoat(obs, terrain) 
                        #     break
                self.x, self.y = newX, newY
            self.lastMoved = currTime

    def draw(self):
        super().draw()