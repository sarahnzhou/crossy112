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

    def move(self, direction, canvasWidth, canvasHeight):
        if direction == 'left' and self.x - 25 >= 0: # make sure no going off canvas
            self.x-=self.stepSize
            self.moveSound.play(restart=False)
        if direction == 'right' and self.x + 25 + self.width <= canvasWidth: # make sure no going off canvas
            self.x+=self.stepSize
            self.moveSound.play(restart=False)
        if direction == 'up' and self.y - 25 >= 0: # make sure no going off canvas
            self.y-=self.stepSize
            self.moveSound.play(restart=False)
        if direction == 'down' and self.y + 25 + self.height <= canvasHeight: # make sure no going off canvas
            self.y+=self.stepSize
            self.moveSound.play(restart=False)

    def draw(self):
        drawImage(self.imageLink, self.x, self.y, width = self.width, height = self.height)