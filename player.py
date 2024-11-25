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
        moved = False
        if direction == 'left' and self.x - 25 >= 0: # make sure no going off canvas
            self.x-=self.stepSize
            moved = True
        if direction == 'right' and self.x + 25 + self.width <= canvasWidth: 
            self.x+=self.stepSize
            moved = True
        if direction == 'up' and self.y - 25 >= 0: 
            self.y-=self.stepSize
            moved = True
        if direction == 'down' and self.y + 25 + self.height <= canvasHeight: 
            self.y+=self.stepSize
            moved = True

        block = terrain.getPlayerBlock(self)
        if block:
            for obs in block.obstacles:
                if obs.obstacleType == 'tree' and obs.collision(self):
                    #self - Player(self.x, self.y, self.imageLink, self.moveSound)
                    return  #just make sure no moving
        
        if moved:
            #print(f"Moving {direction}. New position: ({self.x}, {self.y})")
            self.moveSound.play(restart=False)
            self.playerMoveCount += 1
            self.hasMoved = True
    
    def updateBoat(self, boat):
        if boat and boat.collision(self):
            if boat.direction > 0:
                self.x += boat.speed #* boat.direction 
                self.onBoat=True
        else:
            self.onBoat = False

    # def decaySpeed(self):
    #     if self.playerMoveCount > 0 and not self.hasMoved:
    #         self.playerMoveCount -= self.speedDecayRate

    def draw(self):
        drawImage(self.imageLink, self.x, self.y, width = self.width, height = self.height)