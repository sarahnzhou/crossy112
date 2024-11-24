from cmu_graphics import *
#user moving
#obstacle - cars? moving
#the water things to jump on moving

obsTypes = {'road': 'car', 'grass': 'tree', 'water': 'boat', 'tracks': 'train'}

class Obstacle:
    def __init__(self, obstacleType, obstacleX, obstacleY, images):
        self.obstacleType = obstacleType
        self.obstacleX = obstacleX
        self.obstacleY = obstacleY
        self.width = 100
        self.height = 100
        self.speed = 0
        self.images = images

    def draw(self):
        if self.obstacleType in self.images:
            drawImage(self.images[self.obstacleType], self.obstacleX, self.obstacleY, width = self.width, height = self.height)

    def move(self, terrainSpeed):
        if self.obstacleType == 'car':
            self.speed = 10 #IF DOG HITS THIS GAME OVER
        elif self.obstacleType == 'tree':
            self.speed = 0 # doesnt move, dog just cant walk through it
        elif self.obstacleType == 'boat':
            self.speed = 15 # WE WANT DOG TO MOVE W/ BOAT, IF MISS BOAT GAME OVER
        elif self.obstacleType == 'train':
            self.speed = 30
        self.obstacleX+=self.speed - terrainSpeed
        if self.obstacleX > 800:
            self.obstacleX = -self.width
        elif self.obstacleX < -self.width:
            self.obstacleX = 800