from cmu_graphics import *

class Player:
    def __init__(self, userX, userY, imageLink, soundLink):
        #later can add more than 1 character (rn its just dog)
        self.x = userX
        self.y = userY
        self.imageLink = imageLink
        self.moveSound = soundLink
        self.width = 110 #size of image
        self.height = 90
        self.stepSize = 100
        self.playerMoveCount = 0 #terrain faster as more moves made per time frame
        self.speedDecay = 0.1
        self.hasMoved = False
        self.onBoat = False

    def move(self, direction, canvasWidth, canvasHeight, terrain):
        newX, newY = self.x, self.y
        moved = False
        if direction == 'left' and self.x - 25 >= 0: # make sure no going off canvas
            newX-=self.stepSize
            moved = True
        if direction == 'right' and self.x + 25 + self.width <= canvasWidth: 
            newX+=self.stepSize
            moved = True
        if direction == 'up' and self.y - 25 >= 0: 
            newY-=self.stepSize
            moved = True
        if direction == 'down' and self.y + 25 + self.height <= canvasHeight: 
            newY+=self.stepSize
            moved = True

        block = terrain.getPlayerBlock(self)
        if block:
            for obs in block.obstacles:
                if obs.obstacleType == 'tree' and obs.collision(Player(newX, newY, self.imageLink, self.moveSound)):
                    newX, newY = self.x, self.y

                    return  #just make sure no moving
        self.x, self.y = newX, newY
        if moved:
            #print(f"Moving {direction}. New position: ({self.x}, {self.y})")
            self.moveSound.play(restart=False)
            self.playerMoveCount += 1
            self.hasMoved = True
    
    def updateBoat(self, boat):
        if boat and boat.collision(self):
            #if boat.direction > 0:
            self.x += boat.speed * boat.direction #maybe need to do speed * something like what boat starts out on
            self.onBoat=True

        else:
            self.onBoat = False

    # def decaySpeed(self):
    #     if self.playerMoveCount > 0 and not self.hasMoved:
    #         self.playerMoveCount -= self.speedDecayRate

    def draw(self):
        drawImage(self.imageLink, self.x, self.y, width = self.width, height = self.height)