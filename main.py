#initialize app cmu graphics stuff
#handle game flow of switching btwn gameplay modes
from cmu_graphics import *
from player import Player

def onAppStart(app):
    app.player = Player(x=app.width / 2 - 65, y=app.height - 100, imageLink='scottie.png', moveSound=Sound('dogbark.mp3'))

#def onStep(app):
    

def onKeyPress(app, key):
    if key in {'left', 'right', 'up', 'down'}:
        app.player.move(key, app.width, app.height)

def redrawAll(app):
    #draw user
    app.player.draw()

def main():
    runApp(width=800, height=800)

main()