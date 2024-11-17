#initialize app cmu graphics stuff
#handle game flow of switching btwn gameplay modes
from cmu_graphics import *

def onAppStart(app):
    app.userURL = 'cmu://872593/35007339/scottie.png'
    app.userX = 380 #start position
    app.userY = 20 #start position

def onKeyPress(app, key):
    if key == 'left':
        app.userX-=10
    if key == 'right':
        app.userX+=10
    if key == 'up':
        app.userY-=10
    if key == 'down':
        app.userY+=10

def redrawAll(app):
    #draw user
    drawImage(app.userURL, app.userX, app.userY, width = 20, height = 20)

def main():
    runApp()

main()
cmu_graphics.run()
