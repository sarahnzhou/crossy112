#handle game flow of switching btwn gameplay modes
from cmu_graphics import *
from player import Player
from terrain import randomGenerateTerrain
from helpers import Helper
from movingobjects import Obstacle
from ai import AIplayer

def onAppStart(app):
    app.mode = 'menu'
    app.aiMode = False
    app.regularMode = False
    app.terrain = None
    app.player = None
    app.ai = None

    app.score = 0
    app.gameOver = False
    app.isPaused = False
    app.menuButtonHovered = None
    app.restartButtonHovered = False

    redCarLink = 'car.png'
    tree1Link = 'blocktree.png'
    boatLink = 'plank.png'
    trainLink = 'bus.png'
    app.rightdogLink='scottieright.png'
    app.leftdogLink = 'scottieleft.png'
    app.obsImages = {'car': redCarLink, 'tree': tree1Link, 'boat': boatLink, 'train': trainLink}
    app.moveSound=Sound('dogbark.mp3')

def generateNewTerrain(app):
    app.terrain = randomGenerateTerrain(app.height, app.width, app.obsImages)

def startRegularMode(app):
    generateNewTerrain(app)

    x = app.width / 2 - 50
    y = app.height - 300
    app.player = Player(x, y, app.rightdogLink, app.leftdogLink, app.moveSound)

def startAIMode(app):
    generateNewTerrain(app)

    x = 0.25 * app.width
    y = app.height - 300
    app.player = Player(x, y, app.rightdogLink, app.leftdogLink, app.moveSound)

    startX = 0.75 * app.width
    startY = app.height - 300
    endX = 0.75 * app.width
    endY = 0 # change to somehow be 25 steps length
    app.ai = AIplayer(startX, startY, endX, endY, app.rightdogLink) # change AI image capabilities

def restart(app):
    onAppStart(app)

def onStep(app):
    if app.mode == 'menu':
        return
    
    if app.gameOver or app.isPaused:
        return
    
    if app.mode == 'regular':
        if app.terrain.terrainStarted:
            app.terrain.regularModeUpdateTerr(app.player)
        else:
            screenMiddle = app.height / 2
            if app.player.y <= screenMiddle:
                app.terrain.terrainStarted = True
            if app.terrain.obstaclesMoving:
                app.terrain.updateObstacles()
    elif app.mode == 'ai':
        app.ai.moveAI(app.terrain)
        if app.terrain.terrainStarted:
            app.terrain.aiModeUpdateTerr(app.player, app.ai)

def onMousePress(app, mouseX, mouseY):
    if app.mode == 'menu':
        if 300 <= mouseX <= 500 and 350 <= mouseY <= 400:
            app.mode = 'ai'
            startAIMode(app)
        elif 300 <= mouseX <= 500 and 450 <= mouseY <= 500:
            app.mode = 'regular'
            startRegularMode(app)
    elif app.mode == 'regular' or app.mode == 'ai':
        if app.gameOver:
            buttonX, buttonY, buttonWidth, buttonHeight = app.width / 2 - 100, app.height / 2 - 20, 200, 70
            if buttonX <= mouseX <= buttonX + buttonWidth and buttonY <= mouseY <= buttonY + buttonHeight:
                restart(app)

        pauseButtonX, pauseButtonY, pauseButtonSize = app.width - 110, 10, 100
        if pauseButtonX <= mouseX <= pauseButtonX + pauseButtonSize and pauseButtonY <= mouseY <= pauseButtonY + 40:
            app.isPaused = not app.isPaused

def onMouseMove(app, mouseX, mouseY):
    if app.mode == 'menu':
        if 300 <= mouseX <= 500 and 350 <= mouseY <= 400:
            app.menuButtonHovered = 'ai'   
        elif 300 <= mouseX <= 500 and 450 <= mouseY <= 500:
            app.menuButtonHovered = 'regular'  
        else:
            app.menuButtonHovered = None

    if app.gameOver:
        buttonX, buttonY, buttonWidth, buttonHeight = app.width / 2 - 100, app.height / 2 - 20, 200, 70
        app.restartButtonHovered = buttonX <= mouseX <= buttonX + buttonWidth and buttonY <= mouseY <= buttonY + buttonHeight
    
def onKeyPress(app, key):
    if app.gameOver or app.isPaused:
        return
    
    if app.mode == 'regular' or app.mode == 'ai':
        if key in {'left', 'right', 'up', 'down'}:
            success = app.player.move(key, app.width, app.height, app.terrain)
            if success and key != 'left' and key != 'right': 
                app.score +=1
            app.terrain.terrainStarted = True

def redrawAll(app):

    if app.mode == 'menu':
        aiButtonColor = 'white' if app.menuButtonHovered == 'ai' else 'deepSkyBlue'
        regularButtonColor = 'white' if app.menuButtonHovered == 'regular' else 'deepSkyBlue'
        drawRect(0, 0, app.width, app.height, fill='lightBlue')
        drawLabel("CROSSY112", app.width / 2, 250, size=70, font='Arial Black', bold=True, fill='white', align='center', border='black', borderWidth=5)
        drawRect(300, 350, 200, 60, fill=aiButtonColor, border='black', borderWidth=3)
        drawLabel("AI", 400, 380, size=30, font='Arial Black', bold=True, fill='black', align='center')
        drawRect(300, 450, 200, 60, fill=regularButtonColor, border='black', borderWidth=3)
        drawLabel("REGULAR", 400, 480, size=30, font='Arial Black', bold=True, fill='black', align='center')
        drawLabel("Choose a mode to start!", app.width / 2, 600, size=40, font='Arial', bold=False, fill='black', align='center')
    elif app.mode == 'regular':
        app.terrain.drawTerrain()
        app.player.draw()
        drawLabel(f"Score: {app.score}", 10, 10, size=50, fill='gold', align='left-top', bold=True, border = 'black', borderWidth = 2)

        pauseButtonX, pauseButtonY, pauseButtonSize = app.width - 110, 10, 100
        buttonFill = 'green' if app.isPaused else 'red'
        buttonText = 'Play' if app.isPaused else 'Pause'
        drawRect(pauseButtonX, pauseButtonY, pauseButtonSize, 40, fill=buttonFill, border='black', borderWidth=2)
        drawLabel(buttonText, pauseButtonX + 50, pauseButtonY + 20, size=20, fill='white', bold=True, align='center')

        if app.gameOver:
            drawLabel(f'Game Over: Final Score {app.score}', app.width/2, app.height/2 - 80, size=50, bold=True, fill='red', align='center', border = 'black', borderWidth = 2)

            buttonX, buttonY, buttonWidth, buttonHeight = app.width / 2 - 100, app.height / 2 - 20, 200, 70
            buttonColor = 'lightGray' if not app.restartButtonHovered else 'white'
            drawRect(buttonX, buttonY, buttonWidth, buttonHeight, fill=buttonColor, border='black', borderWidth=2)
            drawLabel('Restart', app.width / 2, app.height / 2 + 15, size=30, fill='black', bold=True, align='center')
    elif app.mode == 'ai':
        app.terrain.drawTerrain()
        app.player.draw()
        app.ai.draw()

def main():
    runApp(width=800, height=800)

main()