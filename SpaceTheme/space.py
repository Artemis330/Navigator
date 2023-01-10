import random
import math
import sys
import os
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
pygame.init()

# GAME CONSTANTS
    
# SCREEN
screenSize = [800,800] # Default = [800,800]
screenColor = [0,0,0] # Default = [0,0,0]
screen = pygame.display.set_mode(screenSize)
fps = 60 # Default = 60
timerSize = 75 # Default = 100
timerColor = [255,255,255] # Default = [255,255,255]
timerDelay = 1000 # Default = 1000
levelColor = [255,255,255] # Default = [255,255,255] / Level indicator color
levelSize = 25 # Default = 25 / Level indicator size
# PLAYER
playerColor = [255,255,255] # Default = [255,255,255]
playerSize = 14 # Default = 10            
playerSpeed = 5 # Default = 5

# OBSTACLES
obstacleSpeed = 3  # Default = 3           
obstacleSize = 10  # Default = 6
obstacleColor = [255,0,0] # Default = [255,0,0]
maxObstacles = 12  # Default = 12
obstacleBoundaries = "KILL" # Default = "KILL" (Can be updated by level)

# LEVELS

currentLevel = 1

levelTwo = [False,"KILL",2]
levelThree = [False,"KILL",3]
levelFour = [False,"KILL",4]
levelFive = [False,"KILL",5]
levelSix = [False,"KILL",6]
levelSeven = [False,"BOUNCE",7]
levelEight =[False,"KILL",8]

# ASSET LOADING
curDir = str(os.getcwd())

# SPACESHIP
spaceShip = pygame.image.load('spaceShip.png')
spaceShip.convert()

# BACKGROUND
bgList = []
bDir = os.path.join(curDir, 'Backgrounds')
for bg in os.listdir(bDir):
    if bg.endswith('.png'):
        path = os.path.join(bDir, bg)
        key = bg[:-4]
        bgList.append( pygame.image.load(path).convert_alpha() )
# METEORS

mDir = os.path.join(curDir, 'Meteors')
meteorDict = {}
meteorList = []
for filename in os.listdir(mDir):
    if filename.endswith('.png'):
        path = os.path.join(mDir, filename)
        key = filename[:-4]
        meteorDict[key] = pygame.image.load(path).convert_alpha()
        meteorList.append(meteorDict[key])

def main():
    
    def getPosition():
        X = random.randint(0, screenSize[0])
        Y = random.randint(0, screenSize[1])

        lowerX = random.randint(0, screenSize[0] * 0.1)
        upperX =  random.randint(screenSize[0] * 0.9, screenSize[0])
        lowerY  = random.randint(0, screenSize[1] * 0.1)
        upperY = random.randint(screenSize[1] * 0.9, screenSize[1])
        
        topDir = ["S", "E", "W", "SE", "SW"]
        leftDir = ["E", "S", "N", "NE", "SE"]
        bottomDir = ["N", "W", "E", "NE", "NW"]
        rightDir = ["W", "N", "S", "NW", "SW"]
        
        topDirection = topDir[random.randint(0, len(topDir) - 1)]
        leftDirection = leftDir[random.randint(0, len(leftDir) - 1)]
        bottomDirection = bottomDir[random.randint(0, len(bottomDir) - 1)]
        rightDirection = rightDir[random.randint(0, len(rightDir) - 1)]
        
        topBound = [X, lowerY, topDirection]
        leftBound = [lowerX, Y, leftDirection]
        bottomBound = [X, upperY, bottomDirection]
        rightBound = [upperX, Y, rightDirection]
     
        possible = [topBound, leftBound, rightBound, bottomBound]
        selected = possible[ random.randint(0, len(possible) - 1) ]
        
        return selected

    def getMovement():
        movement = getPosition()
        position = [movement[0], movement[1]]
        direction = movement[2]
        move = [position,direction]
        return move
                
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.color = playerColor 
            self.size = playerSize        
            self.pos = [screenSize[0] / 2 , screenSize[1] / 2]
            self.speed = playerSpeed                         
            
    class Obstacle(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.color = obstacleColor
            self.speed = obstacleSpeed
            self.size = obstacleSize
            self.movement = getMovement()
            self.pos = [self.movement[0][0], self.movement[0][1]]
            self.direction = self.movement[1]
            self.image = meteorList[currentLevel-1]
               
    # PLAYER 
    player = Player()
    
    # LIST OF ALL OBSTACLES SPAWNED
    obstacles = []
    
    # GAME CLOCK
    clk = pygame.time.Clock()
    gameClock = 0
    
    # TIMER DISPLAY
    timerFont = pygame.font.SysFont(None, timerSize)
    timerDisplay = timerFont.render(str(gameClock), True, timerColor)
    timerEvent = pygame.USEREVENT + 1
    pygame.time.set_timer(timerEvent, timerDelay)
    
    
    # PLAYER MOVEMENT
    def movement():
        
        key = pygame.key.get_pressed()
        
        if key[pygame.K_w] or key[pygame.K_UP]:
            player.pos[1] -= player.speed
            
        if key[pygame.K_s] or key[pygame.K_DOWN]:
            player.pos[1] += player.speed
            
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            player.pos[0] -= player.speed 
            
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            player.pos[0] += player.speed
    
    # PLAYER WRAPPING
    def wrapping():
        if player.pos[1]  > screenSize[1]:
            player.pos[1] = 0
        
        if player.pos[1] < 0:
            player.pos[1] = screenSize[1]
        
        if player.pos[0] > screenSize[0]:
            player.pos[0] = 0
        
        if player.pos[0] < 0:
            player.pos[0] = screenSize[0]
    
    # OBSTACLE SPAWNER
    def spawner():
        if len(obstacles) < maxObstacles:
            obstacle = Obstacle()
            obstacles.append(obstacle)
        
    # DRAW OBSTACLES
    def drawObstacles():
        for obs in obstacles:
            obs.image = pygame.transform.scale(obs.image, (obs.size * 4, obs.size * 4))
            height = (obs.image.get_height())
            width = (obs.image.get_height())
            blitPos = (obs.pos[0] - width/2, obs.pos[1] - height/2)
            pygame.draw.circle(screen, (obs.color), obs.pos, obs.size) # HITBOX TEST (CIRCLE)
            screen.blit(obs.image,blitPos)
            
    # MOVE OBSTACLES            
    def obstacleMove():
        for obs in obstacles:
            
            if "N" in obs.direction:
                obs.pos[1] -= obs.speed
                
            if "S" in obs.direction:
                obs.pos[1] += obs.speed
                
            if "E" in obs.direction:
                obs.pos[0] += obs.speed
                
            if "W" in obs.direction:
                obs.pos[0] -= obs.speed
    
    # REMOVE OBSTACLE
    def obstacleRemove():
        for obs in obstacles:
            position = obs.pos
            
            if obs.pos[0] > screenSize[0] or obs.pos[0] < 0:
                obstacles.remove(obs)
                obs.kill()

            elif obs.pos[1] > screenSize[1] or obs.pos[1] < 0:
                obs.kill()
                obstacles.remove(obs)
    
    def movementReverse(direction):
        if direction == "N":
            return "S"
        elif direction == "S":
            return "N"          
        elif direction == "E":
            return "W"
        elif direction == "W":
            return "E"
        elif direction == "NW":
            return "SE"
        elif direction == "NE":
            return "SW"
        elif direction == "SE":
            return "NW"
        elif direction == "SW":
            return "NE"
            
    def bounceObstacle():
        for obs in obstacles:
            direction = obs.direction
            
            if obs.pos[1]  > screenSize[1]:
                obs.direction = movementReverse(direction) 
                
            if obs.pos[1] < 0:
                obs.direction = movementReverse(direction)
                
            if obs.pos[0] > screenSize[0]:
                obs.direction = movementReverse(direction) 
                
            if obs.pos[0] < 0:
                obs.direction = movementReverse(direction)
                

    def wrapObstacle():
        for obs in obstacles:
            
            if obs.pos[1]  > screenSize[1]:
                obs.pos[1] = 0  
                
            if obs.pos[1] < 0:
                obs.pos[1] = screenSize[1]    
                
            if obs.pos[0] > screenSize[0]:
                obs.pos[0] = 0        
                
            if obs.pos[0] < 0:
                obs.pos[0] = screenSize[0]
    
    
    def levels():
        # Variables that get updated by levels are declared globally below
        global obstacleBoundaries,maxObstacles,obstacleSize,obstacleColor,obstacleSpeed
        
        # Level start initialized globally below
        global currentLevel,levelTwo,levelThree,levelFour,levelFive,levelSix,levelSeven,levelEight
        
        # STARTS ON LEVEL 1 
        
        # LEVEL 2
        if gameClock == 15 and levelTwo[0] == False:
            maxObstacles *= 1.5
            obstacleColor = [255,255,0]
            obstacleBoundaries = levelTwo[1]
            currentLevel +=1
            levelTwo[0] = True
        
        # LEVEL 3
        elif gameClock == 30 and levelThree[0] == False:
            obstacleSize *= 1.5
            obstacleColor = [0,0,255]
            currentLevel +=1
            obstacleBoundaries = levelThree[1]
            levelThree[0] = True
        
        # LEVEL 4
        elif gameClock == 45 and not levelFour[0]:
            obstacleSize *= 1.5
            obstacleColor = [0,255,0]
            currentLevel +=1
            obstacleBoundaries = levelFour[1]
            levelFour[0] = True
        
        # LEVEL 5
        elif gameClock == 60 and not levelFive[0]:
            obstacleSpeed *= 1.25
            obstacleColor = [0,255,255]
            currentLevel +=1
            obstacleBoundaries = levelFive[1]
            levelFive[0] = True
        
        # LEVEL 6
        elif gameClock == 75 and not levelSix[0]:
            obstacleSize *= 10
            obstacleSpeed /= 2
            maxObstacles /= 10
            obstacleColor = [255,0,255]
            currentLevel +=1
            obstacleBoundaries = levelSix[1]
            levelSix[0] = True
        
        # LEVEL 7
        elif gameClock == 90 and not levelSeven[0]:
            obstacleSize /= 10
            maxObstacles *= 1.5
            obstacleSpeed *= 1.25
            obstacleColor = [100, 0, 50]
            currentLevel +=1
            obstacleBoundaries = levelSeven[1]
            levelSeven[0] = True
            
        # LEVEL 8
        elif gameClock == 105 and not levelEight[0]:
            obstacleSize *= 1.5
            obstacleColor = [0,150,0]
            currentLevel +=1
            obstacleBoundaries = levelEight[1]
            levelEight[0] = True
        
                        
    def update():
        screen.blit(spaceShip, (player.pos[0] - 16,player.pos[1] - 16))
        #pygame.draw.circle(screen, (player.color), player.pos, player.size) # HITBOX TEST (CIRCLE)
        timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright)
        levelRect = levelDisplay.get_rect(topleft = screen.get_rect().topleft)
        screen.blit(timerDisplay, timerRect)
        screen.blit(levelDisplay, levelRect)
        pygame.display.flip()
        screen.fill(screenColor)
        clk.tick(fps)
        
    # LOOP CONDITION
    global running
    running = True  
    
    # GAME LOOP
    while running:
        
        try:
            screen.blit(bgList[round(currentLevel / 2)],(0,0))
        except:
            screen.blit(bgList[random.randint(0,len(bgList) - 1)],(0,0))
        
        for event in pygame.event.get():
            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
            
            elif event.type == timerEvent:
                gameClock +=1
                timerDisplay = timerFont.render(str(gameClock), True, (255,255,255))
                
        # LEVEL DISPLAY
        levelNum = "Level " + str(currentLevel)
        levelFont = pygame.font.SysFont(None, levelSize)
        levelDisplay = levelFont.render( str(levelNum), True, levelColor )
        
        # COLLISION DETECTION
        playerCenter = player.pos
        for obs in obstacles:
            obsCenter = obs.pos
            if ( (math.dist(playerCenter,obsCenter)) < (player.size + obs.size) ):
                running = False
                
                
        levels()    
        movement()
        wrapping()
        spawner()
        obstacleMove()
        
        if obstacleBoundaries == "KILL":
            obstacleRemove()
        
        if obstacleBoundaries == "BOUNCE":
            bounceObstacle()
        
        if obstacleBoundaries == "WRAP":
            wrapObstacle()
        
        drawObstacles()
        update()    
            
    pygame.quit()
    sys.exit()    
        
if __name__ == '__main__':
    main()
    
    
    



