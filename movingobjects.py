from cmu_graphics import *
import random 

obsTypes = {'road': 'car', 'grass': 'tree', 'water': 'boat', 'tracks': 'train'}

class Obstacle:
    def __init__(self, obstacleType, obstacleX, obstacleY, images, direction, width, height):
        self.obstacleType = obstacleType
        self.obstacleX = obstacleX
        self.obstacleY = obstacleY
        self.previousX = obstacleX
        self.width = width
        self.height = height
        self.speed = 0
        self.images = images
        self.direction = direction
        self.totalDiff = 0

    def draw(self):
        if self.obstacleType in self.images: 
            drawImage(self.images[self.obstacleType], self.obstacleX, self.obstacleY, width = self.width, height = self.height)

    def move(self, terrainSpeed):
        self.previousX = self.obstacleX
        if self.obstacleType == 'car':
            self.speed = 5 * self.direction 
        elif self.obstacleType == 'tree':
            self.speed = 0  
        elif self.obstacleType == 'boat':
            self.speed = 5 * self.direction  
        elif self.obstacleType == 'train':
            self.speed = 10 * self.direction

        if self.speed != 0: 
            self.totalDiff = (self.speed + terrainSpeed)
            self.obstacleX -= self.totalDiff
            if self.obstacleX > 800:
                self.obstacleX = -self.width
            elif self.obstacleX < -self.width:
                self.obstacleX = 800 

    def nearby(self, nodeCoords):
        nodeX, nodeY = nodeCoords
        proximity = 50

        return (
            nodeX + 100 > self.obstacleX - proximity and nodeX < self.obstacleX + self.width + proximity and
            nodeY + 100 > self.obstacleY - proximity and nodeY < self.obstacleY + self.height + proximity
        )
        return horizNearby and vertNearby

    def impendingCollision(self, nodeCoords):
        nodeX, nodeY = nodeCoords
        predictObsX = self.obstacleX + self.speed #* self.direction
        predictObsY = self.obstacleY 

        return (
            nodeX < predictObsX + self.width and nodeX + 100 > predictObsX and
            nodeY < predictObsY + self.height and nodeY + 100 > predictObsY
        )