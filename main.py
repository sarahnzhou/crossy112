#handle game flow of switching btwn gameplay modes
from cmu_graphics import *
from player import Player
from terrain import randomGenerateTerrain
from helpers import Helper
from movingobjects import Obstacle

def onAppStart(app):
    app.score = 0
    x = app.width / 2 - 65
    y = app.height - 300
    app.rightdogLink='scottieright.png'
    app.leftdogLink = 'scottieleft.png'
    moveSound=Sound('dogbark.mp3')

    redCarLink = 'car.png'
    tree1Link = 'blocktree.png'
    boatLink = 'plank.png'
    trainLink = 'bus.png'

    app.obsImages = {'car': redCarLink, 'tree': tree1Link, 'boat': boatLink, 'train': trainLink}

    app.gameOver = False
    app.restartButtonHovered = False
    app.player = Player(x, y, app.rightdogLink, app.leftdogLink, moveSound)
    app.terrain = randomGenerateTerrain(app.height, app.width, app.obsImages) #100 is block height, 5 is terrainmovespeed

def restart(app):
    onAppStart(app)

def onStep(app):
    if app.gameOver:
        return
    #app.terrain.updateObstacles()
    screenMiddle = app.height / 2
    if not app.terrain.terrainStarted and app.player.y <= screenMiddle:
        app.terrain.terrainStarted = True

    if not app.terrain.terrainStarted and app.terrain.obstaclesMoving:
        app.terrain.updateObstacles()

    if app.terrain.terrainStarted:
        app.terrain.updateTerrain(app.player)

def onMousePress(app, mouseX, mouseY):
    if app.gameOver:
        buttonX, buttonY, buttonWidth, buttonHeight = app.width / 2 - 100, app.height / 2 - 20, 200, 70
        if buttonX <= mouseX <= buttonX + buttonWidth and buttonY <= mouseY <= buttonY + buttonHeight:
            restart(app)

def onMouseMove(app, mouseX, mouseY):
    if app.gameOver:
        buttonX, buttonY, buttonWidth, buttonHeight = app.width / 2 - 100, app.height / 2 - 20, 200, 70
        app.restartButtonHovered = buttonX <= mouseX <= buttonX + buttonWidth and buttonY <= mouseY <= buttonY + buttonHeight
    
def onKeyPress(app, key):
    if app.gameOver:
        return
    
    if key in {'left', 'right', 'up', 'down'}:
        success = app.player.move(key, app.width, app.height, app.terrain)
        if success and key != 'left' and key != 'right': #NEED TO CHANGE LATER TO SUCCESFUL MOVEMENT NOT BLOCKED
            app.score +=1
        app.terrain.terrainStarted = True

def redrawAll(app):
    app.terrain.drawTerrain()
    app.player.draw()
    drawLabel(f"Score: {app.score}", 10, 10, size=50, fill='gold', align='left-top', bold=True, border = 'black', borderWidth = 2)

    if app.gameOver:
        drawLabel('Game Over', app.width/2, app.height/2 - 80, size=70, bold=True, fill='red', align='center', border = 'black', borderWidth = 2)

        buttonX, buttonY, buttonWidth, buttonHeight = app.width / 2 - 100, app.height / 2 - 20, 200, 70
        buttonColor = 'lightGray' if not app.restartButtonHovered else 'white'
        drawRect(buttonX, buttonY, buttonWidth, buttonHeight, fill=buttonColor, border='black', borderWidth=2)
        drawLabel('Restart', app.width / 2, app.height / 2 + 15, size=30, fill='black', bold=True, align='center')

def main():
    runApp(width=800, height=800)

main()