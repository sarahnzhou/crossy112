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