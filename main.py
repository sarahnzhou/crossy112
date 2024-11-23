#handle game flow of switching btwn gameplay modes
from cmu_graphics import *
from player import Player
from terrain import randomGenerateTerrain
from helpers import Helper

def onAppStart(app):
    x = app.width / 2 - 65
    y = app.height - 100
    imageLink='scottie.png'
    moveSound=Sound('dogbark.mp3')

    app.gameOver = False
    app.player = Player(x, y, imageLink, moveSound)
    app.terrain = randomGenerateTerrain(app.height, app.width, 100) #100 is block height, 5 is terrainmovespeed

def onStep(app):
    app.terrain.updateTerrain(app.player)
    
def onKeyPress(app, key):
    app.terrain.terrainStarted = True
    if key in {'left', 'right', 'up', 'down'}:
        app.player.move(key, app.width, app.height)

def redrawAll(app):
    #draw user
    app.terrain.drawTerrain()
    app.player.draw()

    if app.gameOver:
        drawLabel('Game Over', app.width/2, app.height/2, size=50, bold=True, fill='red', align='center')

def main():
    runApp(width=800, height=800)

main()