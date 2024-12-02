import heapq
#determine ai's move (shortest/fastest path to finish line)
class AIplayer:
    def __init__ (self, startX, startY, endX, endY):
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
        possibleMoves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for possibleX, possibleY in possibleMoves:
            newX, newY = x + possibleX, y + possibleY
            if 0 <= newX < self.dimension and 0 <= newY < self.dimension:
                block = terrain.getPlayerBlock(newX * 100, newY * 100) # getPlayerBlock(self, player, intendedY=None):
                if block:
                    weight = 1  # Default movement cost
                    for obs in block.obstacles:
                        if obs.obstacleType in ['car', 'train']:
                            if obs.impendingCollision((newX, newY)): #need to calc time + distance
                                weight = float('inf')  # Completely avoid 
                            elif obs.nearby(newX, newY):
                                weight += 5  # ok for nodes near obstacles further away
                    neighbors.append((newX, newY, weight))
        return neighbors

    def isValidPath(self, terrain):
        for x, y in self.path:
            block = terrain.getPlayerBlock(x * 100, y * 100)
            if not block or block.sectType == 'water': 
                return False
            for obs in block.obstacles:
                if obs.obstacleType in ['car', 'train'] and obs.impendingCollision((x, y)):
                    return False 
        return True

    def aStar(self):
        start = (self.sX, self.sY)
        finish = (self.eX, self.eY)
        openList = []
        heapq.heappush(openList, (0, start))
        prevSteps = {}
        