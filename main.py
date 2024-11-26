#handle game flow of switching btwn gameplay modes
from cmu_graphics import *
from player import Player
from terrain import randomGenerateTerrain
from helpers import Helper
from movingobjects import Obstacle

def onAppStart(app):
    x = app.width / 2 - 65
    y = app.height - 100
    dogLink='scottie.png'
    moveSound=Sound('dogbark.mp3')

    redCarLink = 'redcar.png'
    tree1Link = 'tree.png'
    boatLink = 'boat.png'
    trainLink = 'train.png'

    app.obsImages = {'car': redCarLink, 'tree': tree1Link, 'boat': boatLink, 'train': trainLink}

    app.gameOver = False
    app.player = Player(x, y, dogLink, moveSound)
    app.terrain = randomGenerateTerrain(app.height, app.width, app.obsImages) #100 is block height, 5 is terrainmovespeed
    #app.terrain.updateObstacles()
    #app.terrain.terrainStarted = True

def onStep(app):
    app.terrain.updateObstacles()

    screenMiddle = app.height / 2
    if not app.terrain.terrainStarted and app.player.y <= screenMiddle:
        app.terrain.terrainStarted = True

    # if not app.gameOver:
    if app.terrain.terrainStarted:
        app.terrain.updateTerrain(app.player)
    
def onKeyPress(app, key):
    if key in {'left', 'right', 'up', 'down'}:
        app.terrain.terrainStarted = True
        app.player.move(key, app.width, app.height, app.terrain)
        #print(f"Key pressed: {key}")

def redrawAll(app):
    #draw user
    app.terrain.drawTerrain()
    app.player.draw()

    #drawImage(app.obsImages['car'], 100, 100)
    if app.gameOver:
        drawRect(0, 0, app.width, app.height, fill='black') 
        drawLabel('Game Over', app.width/2, app.height/2, size=50, bold=True, fill='red', align='center')

def main():
    runApp(width=800, height=800)

main()