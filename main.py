#initialize app cmu graphics stuff
#handle game flow of switching btwn gameplay modes
from cmu_graphics import *

def onAppStart(app):
    app.userURL = 'scottie.png'
    app.userX = app.width/2-65 #start position
    app.userY = app.height - 100 #start position

def onKeyPress(app, key):
    # need to modify these so object moves at an angle
    # need to make left and right borders -> dog cant go offscreen
    if key == 'left':
        app.userX-=25
    if key == 'right':
        app.userX+=25
    if key == 'up':
        app.userY-=25
    if key == 'down':
        app.userY+=25

def redrawAll(app):
    #draw user
    drawImage(app.userURL, app.userX, app.userY, width = 110, height = 90)

def main():
    runApp(width=800, height=800)

main()