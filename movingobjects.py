from cmu_graphics import *
import random

obsTypes = {'road': 'car', 'grass': 'tree', 'water': 'boat', 'tracks': 'train'}

# game over when hit cars or trains or fall into water
# move player w/boat
# must go around trees

class Obstacle:
    def __init__(self, obstacleType, obstacleX, obstacleY, images, direction):
        self.obstacleType = obstacleType
        self.obstacleX = obstacleX
        self.obstacleY = obstacleY
        self.width = 100
        self.height = 100
        self.speed = 0
        self.images = images
        self.direction = direction

    def draw(self):
        if self.obstacleType in self.images:
            drawImage(self.images[self.obstacleType], self.obstacleX, self.obstacleY, width = self.width, height = self.height)

    def collision(self, player):
        return (self.obstacleX < player.x + player.width and self.obstacleX + self.width > player.x and self.obstacleY < player.y + player.height and self.obstacleY + self.height > player.y)

    def move(self, terrainSpeed):
        if self.obstacleType == 'car':
            self.speed = 10 * self.direction #IF DOG HITS THIS GAME OVER
        elif self.obstacleType == 'tree':
            self.speed = 0 # doesnt move, dog just cant walk through it
        elif self.obstacleType == 'boat':
            self.speed = 5 * self.direction # WE WANT DOG TO MOVE W/ BOAT, IF MISS BOAT GAME OVER
        elif self.obstacleType == 'train':
            self.speed = 20 * self.direction

        if self.speed != 0:
            self.obstacleX-= self.speed - terrainSpeed
            if self.obstacleX > 800:
                self.obstacleX = -self.width
            elif self.obstacleX < -self.width:
                self.obstacleX = 800