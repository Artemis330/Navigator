# NAVIGATOR

import random
import math
import sys
import os
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.display.init()
pygame.font.init()

pygame.mouse.set_visible(False)

#------------------GAME CONSTANTS--------------------------------------------------------------------------
# SCREEN                                                                                                                            
screenSize = [800,800] # Default = [800,800]                                                        
fps = 60 # Default = 60                                    
timerSize = 75 # Default = 75                            
timerColor = [255,255,255] # Default = [255,255,255] 
timerDelay = 1000 # Default = 1000

# LEVEL COUNTER
levelSize = 30 # Default = 30                                                                                                                                                                   
levelColor = [255,255,255] # Default = [255,255,255] 

# BACKGROUND CLOUD
cloudSpeed = 1 # Default = 1
cloudStart = -1000 # Default = -1000
cloudSpeedAdder = 0.5 # Default = 0.5

# GAME OVER SCREEN
gameOverColor = [255,0,0] # Default = [255,0,0]
gameOverSize = 100 # Default = 100
helpSize = 30 # Default = 30 
helpColor = [0,255,0] # Default = [0,255,0]
finalScoreSize = 40 # Default = 40
finalScoreColor = [0,255,0] # Default = [0,255,0]
pausedSize = 100 # Default = 100
pausedColor = [255,255,255] # Default = [255,255,255]
pauseMax = 5 # Default = 5

# START MENU
maxIcons = 5 # Default = 5
maxIconSpeed = 5 # Default = 5
maxIconRotationSpeed = 3 # Default = 3
startSize = 120 # Default = 120
startColor = [0,255,0] # Default = [0,255,0]
minIconSize = 30 # Default = 30
maxIconSize = 100 # Default = 100

# STAGE UP
stageUpColor = [0,255,0] # Default = [0,255,0]
stageUpSize = 90 # Default = 90
stageUpCloudStartPos = -900 # Default = -900
stageUpCloudSpeed = 8 # Default = 8

# CREDITS
creditsFontSize = 55 # Default = 55
creditsColor = [255,255,255] # Default = [255,255,255] 

# PLAYER           
playerSpeed = 5 # Default = 5
boostAdder = 1 # Default = 1 / Speed added per unit of fuel used
boostFuel = 10 # Default = 10
speedLimit = 10 # Default = 10
boostReplenishDelay = 50   # Default = 50
boostReplenishAmount = 0.05    # Default = 0.05
boostDrain = 0.5 # Default = 0.5
maxBoost = 20   # Default = 20

# OBSTACLES  (Can be updated by level)
obstacleSpeed = 4  # Default = 4           
obstacleSize = 30    # Default = 30
maxObstacles = 12  # Default = 12
obstacleBoundaries = "KILL" # Default = "KILL" 
aggro = True # Default = True / Determines if obstacles have ability to spawn in every direction / False = More difficult
spinSpeed = 1 # Default = 1
obstacleWipe = False # Default = False / Wipe before level

# LEVELS  
levelTimer = 15 # Default = 15 / Time (seconds) between levels
levelUpCloudSpeed = 25 # Default = 25

# ADD LEVELS HERE: [ hasStarted(T/F) , (levelNumber - 1) * levelTimer , BOUNDS , SPEED , SIZE , NUMBER, SPIN, AGGRO(T/F), WIPE(T/F) ]
levelTwo =           [ False,       levelTimer, "KILL", 5.5,  32,  16,  1, True,  False ]  
levelThree =         [ False,   2 * levelTimer, "KILL", 6,    34,  16,  2, True,  False ] 
levelFour =          [ False,   3 * levelTimer, "KILL", 6.5,  36,  18,  3, True,  False ] 
levelFive =          [ False,   4 * levelTimer, "KILL", 6,    38,  20,  4, True,  False ] 
levelSix =           [ False,   5 * levelTimer, "KILL", 6.5,  40,  18,  3, True,  False ] 
levelSeven =         [ False,   6 * levelTimer, "KILL", 2.2,  50,  65,  1, True,  False ] 
levelEight =         [ False,   7 * levelTimer, "KILL", 7,    44,  20,  4, True,  True  ] 
levelNine =          [ False,   8 * levelTimer, "KILL", 7,    46,  21,  5, True,  False ]
levelTen =           [ False,   9 * levelTimer, "KILL", 7.5,  48,  22,  5, True,  False ]
stageTwoLevelOne =   [ False,  10 * levelTimer, "KILL", 7.5,  50,  23,  0, False, False ]
stageTwoLevelTwo =   [ False,  11 * levelTimer, "KILL", 8,    52,  24,  0, False, False ]
stageTwoLevelThree = [ False,  12 * levelTimer, "KILL", 8,    54,  25,  3, False, False ]
stageTwoLevelFour =  [ False,  13 * levelTimer, "KILL", 8.5,  56,  26,  0, False, False ]

# DIVIDE INTO STAGES
stageOneLevels = [levelTwo,levelThree,levelFour,levelFive,levelSix,levelSeven,levelEight,levelNine,levelTen] # Stage 1
stageTwoLevels = [stageTwoLevelOne,stageTwoLevelTwo,stageTwoLevelThree,stageTwoLevelFour] # Stage 2

# STORE IN LIST
stageList = [stageOneLevels, stageTwoLevels] # List of stages

#----------------------------------------------------------------------------------------------------------------------
# STORE LEVEL DEFAULTS
screen = pygame.display.set_mode(screenSize) # Initialize screen
screenColor = [0,0,0] # Screen fill color 

# FOR EXE
def resource_path(relative_path):
    try: base_path = sys._MEIPASS    
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ASSET LOADING
curDir = resource_path('Assets')
obsDir = os.path.join(curDir, 'Obstacles') # Obstacle asset directory
mDir = os.path.join(obsDir, 'Meteors') # Meteor asset directory
uDir = os.path.join(obsDir, 'UFOs') # UFO asset directory
sDir = os.path.join(curDir, 'Spaceships') # Spaceship asset directory
bDir = os.path.join(curDir, 'Backgrounds') # Background asset directory
menuDir = os.path.join(curDir, 'MainMenu') # Start menu asset directory
rDir = os.path.join(os.getcwd(), 'Records') # Game records directory

# FONT
gameFont = ''
for filename in os.listdir(curDir):
    if filename.endswith('.ttf'):
        path = os.path.join(curDir, filename)
        gameFont = path
        break

# STAGE WIPE CLOUD
stageCloudImg = pygame.image.load( resource_path(os.path.join(curDir,'StageCloud.png') ) ).convert_alpha()

# METEOR ASSETS
meteorList = []
for filename in os.listdir(mDir):
    if filename.endswith('.png'):
        path = os.path.join(mDir, filename)
        meteorList.append(pygame.image.load(resource_path(path)).convert_alpha())

# UFO ASSETS
ufoList = []
for filename in os.listdir(uDir):
    if filename.endswith('.png'):
        path = os.path.join(uDir, filename)
        ufoList.append(pygame.image.load(resource_path(path)).convert_alpha())

# BACKGROUND ASSETS
bgList = []
for filename in os.listdir(bDir):
    bgPath = os.path.join(bDir,filename)
    for nextBg in os.listdir(bgPath):
        
        stageBgPath = os.path.join(bgPath,'Background.png')
        stageCloudPath = os.path.join(bgPath,'Cloud.png')

        bg = pygame.image.load(resource_path(stageBgPath)).convert_alpha()
        cloud = pygame.image.load(resource_path(stageCloudPath)).convert_alpha()
        
        bgList.append([bg,cloud])
        break

# SPACESHIP ASSETS
spaceShipList = []
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'spaceShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'yellowShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'blackAndGoldShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'blackAndRedShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'blueShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'purpleShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'taxiShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'greyAndRedShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'greenShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'orangeShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'rastaShip.png'))).convert_alpha())
spaceShipList.append(pygame.image.load(resource_path(os.path.join(sDir, 'ogreShip.png'))).convert_alpha())

# ALL OBSTACLE ASSETS
obstacleImages = [meteorList,ufoList]

# MAIN MENU ASSETS
menuList = []
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'A.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'O.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'big.png'))).convert_alpha()) 
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'left.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'right.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'dblue.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'lblue.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'lgreen.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'dgreen.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'orange.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'red.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'white.png'))).convert_alpha())
menuList.append(pygame.image.load(resource_path(os.path.join(menuDir,'yellow.png'))).convert_alpha())

# WINDOW
pygame.display.set_caption('Navigator')
pygame.display.set_icon(menuList[0])

# LOAD GAME RECORDS
overallHighScorePath = os.path.join(rDir,'OverallHighScore.txt')
totalAttemptsPath = os.path.join(rDir,'TotalAttempts.txt')

if not os.path.exists(rDir):
    os.mkdir('Records')
    newFile = open(overallHighScorePath,'w')
    newFile.write('0')
    newFile.close()
    newFile = open(totalAttemptsPath,'w')
    newFile.write('0')
    newFile.close()

highScoreFile = open(overallHighScorePath,'r') # Open saved high score
attemptFile = open(totalAttemptsPath,'r')  # Open saved attempts count

overallHighScore = int( highScoreFile.readline() ) # Loads high score
totalAttempts = int ( attemptFile.readline() ) # Loads number of game attempts

highScoreFile.close()
attemptFile.close()

timerFont = pygame.font.Font(gameFont, timerSize)

# FOR RANDOM MOVEMENT    
topDir = ["S", "E", "W", "SE", "SW"]
leftDir = ["E", "S", "N", "NE", "SE"]
bottomDir = ["N", "W", "E", "NE", "NW"]
rightDir = ["W", "N", "S", "NW", "SW"]

restrictedTopDir = ["SE", "SW", "S"]
restrictedLeftDir = ["E", "NE", "SE"]
restrictedBottomDir = ["N", "NE", "NW"]
restrictedRightDir = ["NW", "SW", "W"]


# GAME 
class Game:
    def __init__(self):
        self.currentLevel = 1
        self.currentStage = 1
        self.gameClock = 1
        self.pauseCount = 0
        self.clk = pygame.time.Clock()
        self.savedOverallHighScore = overallHighScore
        self.savedTotalAttempts = totalAttempts
        self.obstacleSpeed = obstacleSpeed         
        self.obstacleSize = obstacleSize  
        self.maxObstacles = maxObstacles
        self.aggro = aggro
        self.obstacleBoundaries = obstacleBoundaries 
        self.cloudSpeed = cloudSpeed
        self.attemptNumber = 1
        self.mainMenu = True # Assures start menu only runs when called
        self.sessionHighScore = 0
        self.gameConstants = []
        self.savedShipNum = 0
        self.spinSpeed = spinSpeed
        self.cloudPos = cloudStart
        self.wipe = obstacleWipe
        contantList = []
        for stage in stageList:
            stageConstants = []
            for settings in stage:
                levelDict = {
                                "START" : settings[0], 
                                "TIME" : settings[1],
                                "bound" : settings[2],  
                                "speedMult" : settings[3],
                                "obsSizeMult" : settings[4],
                                "maxObsMult" : settings[5],
                                "spinSpeed" : settings[6],
                                "aggro" : settings[7],
                                "wipe" : settings[8]
                    }
                stageConstants.append(levelDict)
            contantList.append(stageConstants)
        self.gameConstants = contantList 
        
        # LOAD GAME CONSTANTS
        self.savedConstants = {
                "obstacleSpeed" : self.obstacleSpeed, 
                "obstacleSize" : self.obstacleSize, 
                "maxObstacles" : self.maxObstacles, 
                "obstacleBoundaries" : self.obstacleBoundaries,
                "cloudSpeed" : self.cloudSpeed,
                "spinSpeed" : self.spinSpeed,
                "aggro" : self.aggro,
                "wipe" : self.wipe
                }

    
    # MAIN GAME LOOP
    def update(self,player,obstacles,menu,events):
        for event in pygame.event.get():
            
            # EXIT
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            # INCREMENT TIMER
            if event.type == events.timerEvent:
                self.gameClock +=1
            
            # PAUSE GAME
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game.pauseCount < pauseMax :
                game.pauseCount += 1
                menu.pause(game,player,obstacles)
            
            # BOOST REPLENISH
            if event.type == events.boostReplenish and player.boostFuel < player.maxBoost: player.boostFuel += boostReplenishAmount

        # BACKGROUND ANIMATION
        screen.blit(bgList[self.currentStage - 1][0], (0,0) )
        screen.blit(bgList[self.currentStage - 1][1], (0,self.cloudPos) )
        if self.cloudPos < screenSize[1]: self.cloudPos += self.cloudSpeed  
        else: self.cloudPos = cloudStart 
        
        # HUD
        self.showHUD(player)
        
        # COLLISION DETECTION
        if pygame.sprite.spritecollide(player,obstacles,True,pygame.sprite.collide_mask): menu.gameOver(self,player,obstacles)
        
        # DRAW AND MOVE SPRITES
        player.movement()
        player.boost()
        player.wrapping()
        self.spawner(obstacles)
        obstacleMove(obstacles)

        # UPDATE HIGH SCORE
        if self.gameClock > self.sessionHighScore: self.sessionHighScore = self.gameClock
        
        # OBSTACLE HANDLING
        if self.obstacleBoundaries == "KILL": obstacleRemove(obstacles)
        if self.obstacleBoundaries == "BOUNCE": bounceObstacle(obstacles)
        if self.obstacleBoundaries == "WRAP": wrapObstacle(obstacles)
        
        # LEVEL UP 
        self.levelUpdater(player,obstacles,events)   
        
        # DRAW SPRITES
        newBlit = rotateImage(player.image,player.rect,player.angle) # Player rotation
        screen.blit(newBlit[0],newBlit[1]) # Draw player
        
        # DRAW OBSTACLES
        for obs in obstacles:
            newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
            screen.blit(newBlit[0],newBlit[1])
            obs.angle += (obs.spinSpeed * obs.spinDirection) # Update angle 
        
        # UPDATE SCREEN
        player.lastAngle = player.angle
        player.angle = 0 # Reset player orientation
        pygame.display.flip()
        self.tick()
    
    
    def tick(self): self.clk.tick(fps)


    # SET GAME CONSTANTS TO DEFAULT
    def resetGameConstants(self):
        self.obstacleSpeed = self.savedConstants["obstacleSpeed"]
        self.obstacleSize = self.savedConstants["obstacleSize"]
        self.maxObstacles = self.savedConstants["maxObstacles"]
        self.obstacleBoundaries = self.savedConstants["obstacleBoundaries"]
        self.cloudSpeed = self.savedConstants["cloudSpeed"]
        self.spinSpeed = self.savedConstants["spinSpeed"]
        self.aggro = self.savedConstants["aggro"]
        self.wipe = self.savedConstants["wipe"]
        self.cloudPos = cloudStart
    
    
    def alternateUpdate(self,player,obstacles,events):
        
        player.alternateMovement()
        player.movement()
        player.wrapping()
        screen.fill(screenColor)
        screen.blit(bgList[self.currentStage-1][0],(0,0)) # Draw background
        screen.blit(bgList[self.currentStage-1][1],(0,self.cloudPos)) # Draw background cloud
        self.cloudPos += self.cloudSpeed
        obstacleMove(obstacles)
        
        for obs in obstacles:
            newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
            screen.blit(newBlit[0],newBlit[1])
            obs.angle += (obs.spinSpeed * obs.spinDirection) # Update angle 


    # UPDATE GAME CONSTANTS
    def levelUpdater(self,player,obstacles,events):
        
        # UPDATES STAGE
        if self.currentStage < len(self.gameConstants):
            if self.gameConstants[self.currentStage][0]["TIME"] == self.gameClock and not self.gameConstants[self.currentStage][0]["START"]:
                self.gameConstants[self.currentStage][0]["START"] = True
                stageUpCloud = stageCloudImg
                stageUpFont = pygame.font.Font(gameFont, stageUpSize)
                stageUpDisplay = stageUpFont.render("STAGE UP", True, stageUpColor)
                stageUpRect = stageUpCloud.get_rect()
                stageUpRect.center = (screenSize[0]/2, stageUpCloudStartPos)
                stageUp , stageWipe = True , True
                
                # STAGE UP ANIMATION / Removes old obstacles
                while stageUp:
                    
                    img, imgRect = rotateImage(player.image, player.rect, player.angle)
                    self.alternateUpdate(player,obstacles,events)
                    
                    for obs in obstacles:
                        if obs.rect.centery <= stageUpRect.centery: obs.kill()

                    screen.blit(stageUpCloud,stageUpRect) # Draw cloud
                    screen.blit(stageUpDisplay,(stageUpRect.centerx - screenSize[0]/5, stageUpRect.centery)) # Draw "STAGE UP" text
                    game.showHUD(player)
                    screen.blit(img,imgRect) # Draw player
                    pygame.display.flip()
                    stageUpRect.centery += stageUpCloudSpeed
                    self.tick()
                    
                    if stageUpRect.centery >= screenSize[1]/2 and stageWipe: 
                        self.currentStage += 1
                        self.currentLevel = 1
                        stageWipe = False
        
                    elif stageUpRect.centery >= screenSize[1] * 2: stageUp = False

        # UPDATES LEVEL
        for levelDict in self.gameConstants[self.currentStage-1]:
            if levelDict["TIME"] == self.gameClock:
                if not levelDict["START"]:
                    
                    if self.gameConstants[self.currentStage-1][self.currentLevel-1]["wipe"]:
                        # REMOVE OLD OBSTACLES
                        levelUpCloud = stageCloudImg
                        levelUpRect = levelUpCloud.get_rect()
                        levelUpRect.center = (screenSize[0]/2, stageUpCloudStartPos)
                        levelUp = True  
                        
                        # LEVEL UP ANIMATION / Removes old obstacles
                        while levelUp:
                            
                            img, imgRect = rotateImage(player.image, player.rect, player.angle)                        
                            self.alternateUpdate(player,obstacles,events)
                            for obs in obstacles:
                                if obs.rect.centery <= levelUpRect.centery: obs.kill()

                            screen.blit(levelUpCloud,levelUpRect) # Draw cloud
                            game.showHUD(player)
                            screen.blit(img,imgRect) # Draw player
                            pygame.display.flip()
                            levelUpRect.centery += levelUpCloudSpeed

                            if levelUpRect.top >= screenSize[1]: levelUp = False
 
                            self.tick()
                     
                    levelDict["START"] = True
                    self.obstacleBoundaries = levelDict["bound"]
                    self.obstacleSpeed = levelDict["speedMult"]
                    self.maxObstacles = levelDict["maxObsMult"]
                    self.obstacleSize = levelDict["obsSizeMult"]
                    self.spinSpeed = levelDict["spinSpeed"]
                    self.aggro = levelDict["aggro"]
                    self.wipe = levelDict["wipe"]
                    self.cloudSpeed += cloudSpeedAdder
                    self.currentLevel += 1
    

    # RESET LEVEL PROGRESS
    def resetAllLevels(self):
        for stage in self.gameConstants:
            for levels in stage:
                levels["START"] = False


    # REMOVE ALL OBSTACLES
    def killAllObstacles(self,obstacles):
        for obstacle in obstacles: obstacle.kill()


    # HUD
    def showHUD(self,player):
        
        # TIMER DISPLAY
        timerDisplay = timerFont.render(str(self.gameClock), True, timerColor)
        
        # STAGE DISPLAY
        stageNum = "Stage " + str(self.currentStage)
        stageFont = pygame.font.Font(gameFont, levelSize)
        stageDisplay = stageFont.render( str(stageNum), True, levelColor )
        stageRect = stageDisplay.get_rect(topleft = screen.get_rect().topleft)
        
        # LEVEL DISPLAY
        levelNum = "-  Level " + str(self.currentLevel)
        levelFont = pygame.font.Font(gameFont, levelSize)
        levelDisplay = levelFont.render( str(levelNum), True, levelColor )
        levelRect = levelDisplay.get_rect() 
        levelRect.center = (stageRect.right + levelRect.width*0.65, stageRect.centery)

        timerRect = timerDisplay.get_rect(topright = screen.get_rect().topright) 
        
        screen.blit(timerDisplay, timerRect)
        screen.blit(stageDisplay, stageRect)
        screen.blit(levelDisplay, levelRect)
        pygame.draw.rect(screen, [255,0,0],[screenSize[0]/3, 0, player.boostFuel * 20, 10]) # BOOST METER
    
    
    # SPAWN OBSTACLES
    def spawner(self,obstacles):
            if len(obstacles) < self.maxObstacles:
                obstacle = Obstacle(self.aggro)
                obstacles.add(obstacle)
    
    
    def resetClock(self): self.gameClock = 0


# GAME EVENTS
class Event:
    def __init__(self):
        
        # GAMECLOCK
        self.timerEvent = pygame.USEREVENT
        
        # BOOST
        self.boostReplenish = pygame.USEREVENT + 1

    # SETS EVENTS
    def set(self):
        pygame.time.set_timer(self.timerEvent, timerDelay)
        pygame.time.set_timer(self.boostReplenish, boostReplenishDelay)

    
# MENUS
class Menu:
    # START MENU
    def home(self,game,player):
        
        icons = []
        for icon in range(maxIcons): icons.append(Icon())
     
        startFont = pygame.font.Font(gameFont, startSize)
        startDisplay = startFont.render("N  VIGAT  R", True, startColor)
        startRect = startDisplay.get_rect()
        startRect.center = (screenSize[0]/2,screenSize[1]/2)
        
        startHelpFont = pygame.font.Font(gameFont, helpSize)
        startHelpDisplay = startHelpFont.render("ESCAPE = QUIT     SPACE = START     C = CREDITS", True, helpColor)   
        startHelpRect = startHelpDisplay.get_rect()
        startHelpRect.center = (screenSize[0]/2,screenSize[1]-screenSize[1]/7)
        
        shipHelpFont = pygame.font.Font(gameFont, round(helpSize * .8))
        shipHelpDisplay = shipHelpFont.render("A/LEFT = PREV SHIP     D/RIGHT = NEXT SHIP", True, helpColor)
        shipHelpRect = shipHelpDisplay.get_rect(center = (screenSize[0]/2, screenSize[1]-screenSize[1]/7 + 40))
        
        leftRect = menuList[3].get_rect(center = (screenSize[0] * 0.2 , screenSize[1]/3) )
        rightRect = menuList[4].get_rect(center = (screenSize[0] * 0.8 , screenSize[1]/3) )
        
        bounceDelay = 5
        bounceCount = 0
        
        # SHIP UNLOCKS   
        unlockNumber = 0
        if game.savedOverallHighScore >= 330: unlockNumber = len(spaceShipList)
        elif game.savedOverallHighScore >= 300: unlockNumber = len(spaceShipList) - 1
        elif game.savedOverallHighScore >= 270: unlockNumber = len(spaceShipList) - 2
        elif game.savedOverallHighScore >= 240: unlockNumber = len(spaceShipList) - 3
        elif game.savedOverallHighScore >= 210: unlockNumber = len(spaceShipList) - 4
        elif game.savedOverallHighScore >= 180: unlockNumber = len(spaceShipList) - 5    
        elif game.savedOverallHighScore >= 150: unlockNumber = len(spaceShipList) - 6 
        elif game.savedOverallHighScore >= 120: unlockNumber = len(spaceShipList) - 7   
        elif game.savedOverallHighScore >= 90: unlockNumber = len(spaceShipList) - 8    
        elif game.savedOverallHighScore >= 60: unlockNumber = len(spaceShipList) - 9
        elif game.savedOverallHighScore >= 30: unlockNumber = len(spaceShipList) - 10

        for imageNum in range(unlockNumber-1):
            player.nextSpaceShip()
        
        startOffset = 100
        startDelay = 1
        iconPosition, startDelayCounter = startOffset, 0
        
        while game.mainMenu:
                
            if bounceCount >= bounceDelay: bounceCount = 0
            else: bounceCount +=1
                
            for event in pygame.event.get():
                # START
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    
                    game.savedShipNum = player.currentImageNum
                    
                    while iconPosition > 0:
                        
                        if startDelayCounter >= startDelay:  startDelayCounter = 0
                        else: startDelayCounter +=1
                             
                        # Start animation
                        screen.fill(screenColor)
                        screen.blit(bgList[game.currentStage - 1][0],(0,0))
                        screen.blit(player.image, (player.rect.x,player.rect.y + iconPosition)) # Current spaceship
                        
                        pygame.display.update()
                        
                        if startDelayCounter >= startDelay: iconPosition-=1

                    game.mainMenu = False    
                    return
                
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                    if unlockNumber > player.currentImageNum + 1: player.nextSpaceShip()
                    
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_LEFT):
                    player.lastSpaceShip()
                
                # CREDITS
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c: menu.creditScreen()
                
                # QUIT
                elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and  event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage - 1][0],(0,0))
            
            for icon in icons:
                if bounceCount == bounceDelay: icon.move()    
                icon.draw()

            screen.blit(startDisplay,startRect)
            screen.blit(startHelpDisplay, startHelpRect)
            if game.savedOverallHighScore >= 30: screen.blit(shipHelpDisplay,shipHelpRect)
            screen.blit(player.image, (player.rect.x,player.rect.y + startOffset)) # Current spaceship
            screen.blit(menuList[0],(-14 + startRect.left + menuList[0].get_width() - menuList[0].get_width()/8,screenSize[1]/2 - 42)) # "A" symbol
            screen.blit(menuList[1],(-42 + screenSize[0] - startRect.centerx + menuList[1].get_width() * 2,screenSize[1]/2 - 42)) # "O" symbol
            
            # UFO icons
            screen.blit(menuList[2],(screenSize[0]/2 - menuList[2].get_width()/2,screenSize[1]/8)) # Big icon
            screen.blit(menuList[3],leftRect) # Left UFO
            screen.blit(menuList[4],rightRect) # Right UFO
            
            pygame.display.update()
        
        
    def pause(self,game,player,obstacles):
        
        playerBlit = rotateImage(player.image,player.rect,player.lastAngle)
        paused = True
        pausedFont = pygame.font.Font(gameFont, pausedSize)
        pausedDisplay = pausedFont.render("Paused", True, pausedColor)
        pausedRect = pausedDisplay.get_rect()
        pausedRect.center = (screenSize[0]/2, screenSize[1]/2)
        
        # REMAINING PAUSES
        pauseCountSize = 40
        pauseNum = str(pauseMax - game.pauseCount) + " Pauses left"
        
        if game.pauseCount >= pauseMax:
            pauseNum = "Out of pauses"

        pauseCountFont = pygame.font.Font(gameFont,pauseCountSize)
        pauseDisplay = pauseCountFont.render( pauseNum , True, levelColor )
        pauseRect = pauseDisplay.get_rect() 
        pauseRect.center = (screenSize[0] * .5 , screenSize[1] -16)
        
        while paused:
            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage-1][0],(0,0))
            screen.blit(cloud,(0,game.cloudPos))
            game.showHUD(player)
            
            screen.blit(playerBlit[0],playerBlit[1])
            
            for obs in obstacles: # Draw obstacles
                newBlit = rotateImage(obs.image,obs.rect,obs.angle) # Obstacle rotation
                screen.blit(newBlit[0],newBlit[1])

            screen.blit(pauseDisplay, pauseRect)
            screen.blit(pausedDisplay,pausedRect)
            pygame.display.flip()
            for event in pygame.event.get():
                # EXIT
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE): paused = False
     

    # GAME OVER SCREEN 
    def gameOver(self,game,player,obstacles):
        
        gameOver = True
        newHighScore = False
        
        if game.sessionHighScore > game.savedOverallHighScore:
            updatedHighScoreFile = open(overallHighScorePath,'w')
            updatedHighScoreFile.write(str(game.sessionHighScore))
            updatedHighScoreFile.close()
            game.savedOverallHighScore = game.sessionHighScore
            newHighScore = True

        game.savedTotalAttempts += 1
        statsSpacingY = screenSize[1]/16
        
        # "GAME OVER" text
        gameOverFont = pygame.font.Font(gameFont, gameOverSize)
        gameOverDisplay = gameOverFont.render("Game Over", True, gameOverColor)
        gameOverRect = gameOverDisplay.get_rect()
        gameOverRect.center = (screenSize[0]/2, screenSize[1]/3)
        
        # Stats display
        statLineFontSize = round(finalScoreSize * 0.75)
        statFont = pygame.font.Font(gameFont, statLineFontSize)
        exitFont = pygame.font.Font(gameFont, helpSize)
        
        # Text
        attemptLine = str(game.attemptNumber) + " attempts this session, " + str(game.savedTotalAttempts) + " overall"
        survivedLine = "Survived for " + str(game.gameClock) + " seconds"
        levelLine = "Died at stage " + str(game.currentStage) + "  -  level " + str(game.currentLevel)
        overallHighScoreLine = "High score  =  " + str(game.savedOverallHighScore) + " seconds"
        newHighScoreLine = "New high score! " + str(game.sessionHighScore) + " seconds"
        
        # Display
        recordDisplay = statFont.render(overallHighScoreLine, True, finalScoreColor)
        attemptDisplay = statFont.render(attemptLine, True, finalScoreColor)
        survivedDisplay = statFont.render(survivedLine, True, finalScoreColor)
        levelDisplay = statFont.render(levelLine, True, finalScoreColor)
        newHighScoreDisplay = statFont.render(newHighScoreLine, True, finalScoreColor)
        exitDisplay = exitFont.render("TAB = MENU     SPACE = RESTART    ESCAPE = QUIT    C = CREDITS", True, helpColor)
        
        # Rects
        attemptRect = attemptDisplay.get_rect()
        survivedRect = survivedDisplay.get_rect()
        levelRect = levelDisplay.get_rect()
        recordRect = recordDisplay.get_rect()
        exitRect = exitDisplay.get_rect()
        
        # Rect position
        survivedRect.center = (screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 3)
        recordRect.center = (screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 4)
        levelRect.center = (screenSize[0]/2, screenSize[1]/3 +statsSpacingY * 5)
        attemptRect.center = (screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 6)
        exitRect.center = (screenSize[0]/2, screenSize[1]/3 + statsSpacingY * 8)
        
        # Updated game records
        updatedAttemptFile = open(totalAttemptsPath,'w')
        updatedAttemptFile.write(str(game.savedTotalAttempts))
        updatedAttemptFile.close()
        updatedRecords = True
        
        while gameOver:
        
            # Background
            screen.fill(screenColor)
            screen.blit(bgList[game.currentStage - 1][0],(0,0))
            if newHighScore: screen.blit(newHighScoreDisplay,recordRect)   
            else: screen.blit(recordDisplay,recordRect)
            screen.blit(gameOverDisplay,gameOverRect)
            screen.blit(attemptDisplay,attemptRect)
            screen.blit(survivedDisplay,survivedRect)
            screen.blit(levelDisplay,levelRect)
            screen.blit(exitDisplay,exitRect)
            pygame.display.flip()
           
            for event in pygame.event.get():
                
                # EXIT
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # CREDITS
                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_c): menu.creditScreen()

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_TAB): 
                    # SET DEFAULTS AND GO BACK TO MENU
                    game.gameClock = 0
                    game.currentLevel = 1
                    game.currentStage = 1
                    player.kill()
                    game.killAllObstacles(obstacles)
                    game.resetAllLevels()
                    game.attemptNumber += 1
                    game.mainMenu = True
                    gameLoop()

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    # SET DEFAULTS AND RESTART GAME
                    game.gameClock = 0
                    game.currentLevel = 1
                    game.currentStage = 1
                    player.kill()
                    game.killAllObstacles(obstacles)
                    game.resetAllLevels()
                    game.attemptNumber += 1
                    running = True
                    gameLoop()


    def creditScreen(self):
        
            rollCredits = True 
            posX = screenSize[0]/2
            posY = screenSize[1]/2
            creditsFont = pygame.font.Font(gameFont, creditsFontSize)
            
            createdByLine = "Created by Mike Pistolesi"
            creditsLine = "Art by Collin Guetta"
            
            createdByDisplay = creditsFont.render(createdByLine, True, creditsColor)
            creditsDisplay = creditsFont.render(creditsLine, True, creditsColor)
            
            creditsRect = creditsDisplay.get_rect()
            createdByRect = createdByDisplay.get_rect()
            
            creditsRect.center = (posX,posY)
            createdByRect.center = (posX, posY - screenSize[1]/15) 
            
            bounceCount = 0
            direction = randomEightDirection()
            
            while rollCredits:
                
                for event in pygame.event.get():
                    # EXIT
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # RETURN TO GAME
                    elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_c or event.key == pygame.K_SPACE):
                        rollCredits = False
                
                screen.fill(screenColor)
                screen.blit(bgList[game.currentStage - 1][0],(0,0))
                screen.blit(createdByDisplay,createdByRect)
                screen.blit(creditsDisplay,creditsRect)
                pygame.display.flip()

                # BOUNCE OFF EDGES
                if createdByRect.right > screenSize[0]: direction = rightDir[random.randint(0, len(rightDir) - 1)]
                if createdByRect.left < 0: direction = leftDir[random.randint(0, len(leftDir) - 1)]  
                if creditsRect.bottom > screenSize[1]: direction = bottomDir[random.randint(0, len(bottomDir) - 1)]
                if createdByRect.top < 0 : direction = topDir[random.randint(0, len(topDir) - 1)]

                if bounceCount == 0:
                    if "N" in direction:
                        creditsRect.centery-= 1
                        createdByRect.centery-= 1
                        
                    if "S" in direction: 
                        creditsRect.centery+= 1
                        createdByRect.centery+= 1
                        
                    if "E" in direction:
                        creditsRect.centerx+= 1
                        createdByRect.centerx+= 1
                        
                    if "W" in direction:
                        creditsRect.centerx-= 1
                        createdByRect.centerx-= 1

                bounceCount +=1
                if bounceCount >= 10: bounceCount = 0


# PLAYER
class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.currentImageNum = 0         
            self.speed,self.baseSpeed = playerSpeed, playerSpeed
            self.image = spaceShipList[self.currentImageNum]
            self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
            self.mask = pygame.mask.from_surface(self.image)
            self.angle = 0
            self.boostFuel = boostFuel
            self.maxBoost = maxBoost
            self.lastAngle = 0

        # PLAYER MOVEMENT
        def movement(self):
            key = pygame.key.get_pressed()
            
            if key[pygame.K_w] or key[pygame.K_UP]: 
                self.rect.centery -= self.speed
                self.angle = 0
                
            if key[pygame.K_s] or key[pygame.K_DOWN]: 
                self.rect.centery += self.speed
                self.angle = 180
            
            if key[pygame.K_a] or key[pygame.K_LEFT]: 
                self.rect.centerx -= self.speed
                self.angle = 90
            
            if key[pygame.K_d] or key[pygame.K_RIGHT]:
                self.rect.centerx += self.speed
                self.angle = -90
            
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_w] or key[pygame.K_UP]):
                self.angle = 45
                
            if (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_w] or key[pygame.K_UP]):
                self.angle = 0
                
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_d] or key[pygame.K_RIGHT]):
                self.angle = 0
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (key[pygame.K_w] or key[pygame.K_UP]):
                self.angle = -45
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and (key[pygame.K_s] or key[pygame.K_DOWN]):
                self.angle = -120
                
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_s] or key[pygame.K_DOWN]):
                self.angle = 120
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and ( key[pygame.K_a] or key[pygame.K_LEFT]): 
                self.angle = 0
            
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_w] or key[pygame.K_UP]):
                self.angle = 90

            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and ( key[pygame.K_a] or key[pygame.K_LEFT]) and (key[pygame.K_s] or key[pygame.K_DOWN]): 
                self.angle = 180
            
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and ( key[pygame.K_w] or key[pygame.K_UP]) and (key[pygame.K_s] or key[pygame.K_DOWN]): 
                self.angle = -90
            
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and ( key[pygame.K_w] or key[pygame.K_UP]) and (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_d] or key[pygame.K_RIGHT]): 
                self.angle = 0
            
        
        def boost(self):
            key = pygame.key.get_pressed()
            
            if (key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]) and self.boostFuel - boostDrain > 0 and self.speed + boostAdder < speedLimit and  ( (key[pygame.K_a] or key[pygame.K_LEFT]) and ( key[pygame.K_w] or key[pygame.K_UP]) and (key[pygame.K_s] or key[pygame.K_DOWN]) and (key[pygame.K_d] or key[pygame.K_RIGHT]) ):
                pass
                
            elif (key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT]) and self.boostFuel - boostDrain > 0 and self.speed + boostAdder < speedLimit and  ( (key[pygame.K_a] or key[pygame.K_LEFT]) or ( key[pygame.K_w] or key[pygame.K_UP]) or (key[pygame.K_s] or key[pygame.K_DOWN]) or (key[pygame.K_d] or key[pygame.K_RIGHT]) ):
                self.speed += (boostAdder)
                self.boostFuel -= (boostDrain)

            else: self.speed = self.baseSpeed

    
        # MOVEMENT DURING STAGE UP
        def alternateMovement(self):    
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_UP): 
                    self.rect.centery -=1
                    self.angle = 0

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_LEFT): 
                    self.rect.centerx -=1
                    self.angle = 90

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN): 
                    self.rect.centery +=1
                    self.angle = 180  

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT): 
                    self.rect.centerx +=1
                    self.angle = -90 

                if event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (event.key == pygame.K_w or event.key == pygame.K_UP): self.angle = -45
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (event.key == pygame.K_w or event.key == pygame.K_UP): self.angle = -45  
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_a or event.key == pygame.K_LEFT): self.angle = 120   
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_d or event.key == pygame.K_RIGHT): self.angle = -120  
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (event.key == pygame.K_a or event.key == pygame.K_LEFT): self.angle = 0
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (event.key == pygame.K_d or event.key == pygame.K_RIGHT): self.angle = 180
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (event.key == pygame.K_w or event.key == pygame.K_UP): self.angle = -90
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (event.key == pygame.K_w or event.key == pygame.K_UP): self.angle = 90
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (event.key == pygame.K_w or event.key == pygame.K_UP): self.angle = 0
                else: self.angle = 0

 
        # WRAP AROUND SCREEN
        def wrapping(self):
            if self.rect.centery  > screenSize[1]: self.rect.centery = 0
            if self.rect.centery < 0: self.rect.centery = screenSize[1]
            if self.rect.centerx > screenSize[0]: self.rect.centerx = 0
            if self.rect.centerx < 0: self.rect.centerx = screenSize[0]


        # GET NEXT SPACESHIP IMAGE
        def nextSpaceShip(self):
            if self.currentImageNum < len(spaceShipList)-1:
                self.image = spaceShipList[self.currentImageNum + 1]
                self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
                self.mask = pygame.mask.from_surface(self.image)
                self.currentImageNum+=1


        # GET PREVIOUS SPACESHIP IMAGE
        def lastSpaceShip(self):
            if self.currentImageNum >= 1: 
                self.image = spaceShipList[self.currentImageNum - 1]
                self.rect = self.image.get_rect(center = (screenSize[0]/2,screenSize[1]/2))
                self.mask = pygame.mask.from_surface(self.image)
                self.currentImageNum-=1
  

# OBSTACLES
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,aggro):
        super().__init__()
        self.aggro = aggro
        self.speed = game.obstacleSpeed
        self.size = game.obstacleSize
        self.spinSpeed = game.spinSpeed
        self.movement = getMovement(self.aggro)
        self.direction = self.movement[1]
        try: self.image = obstacleImages[game.currentStage - 1][game.currentLevel-1].convert_alpha()
        except: self.image = meteorList[random.randint(0,len(meteorList)-1)]
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = 0
        spins = [-1,1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]


# START MENU METEOR GENERATION
class Icon(pygame.sprite.Sprite):
    def __init__(self):
        spins = [-1,1]
        self.speed = random.randint(1,maxIconSpeed)
        self.movement = getMovement(False)
        self.direction = self.movement[1]
        self.spinDirection = spins[random.randint(0,len(spins)-1)]
        self.image = menuList[random.randint(5,len(menuList)-1)]
        size = random.randint(minIconSize,maxIconSize)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
        self.angle = 0

 
    def move(self): 
        if "N" in self.direction: self.rect.centery -= self.speed                       
        if "S" in self.direction: self.rect.centery += self.speed                        
        if "E" in self.direction: self.rect.centerx += self.speed               
        if "W" in self.direction: self.rect.centerx -= self.speed  
        
        if self.angle >= 360 or self.angle <= -360: self.angle = 0
            
        self.angle += self.spinDirection * random.uniform(0, maxIconRotationSpeed)
        
        randomTimerUX = random.randint(screenSize[0] * 2,screenSize[0] * 4)
        randomTimerUY = random.randint(screenSize[1] * 2,screenSize[1] * 4)
        randomTimerLX = -1 * random.randint(screenSize[0], screenSize[0] * 3)
        randomTimerLY = -1 * random.randint(screenSize[0], screenSize[1] * 3)
        
        if (self.rect.centery > randomTimerUY) or (self.rect.centery < randomTimerLY) or (self.rect.centerx> randomTimerUX) or (self.rect.centerx < randomTimerLX):
            self.movement = getMovement(False)
            self.direction = self.movement[1]
            self.image = menuList[random.randint(5,len(menuList)-1)]
            self.speed = random.randint(1,maxIconSpeed)
            self.rect = self.image.get_rect(center = (self.movement[0][0],self.movement[0][1]))
            size = random.randint(minIconSize,maxIconSize)
            self.image = pygame.transform.scale(self.image, (size, size))


    def draw(self):
        drawing, drawee = rotateImage(self.image,self.rect,self.angle)
        screen.blit(drawing,drawee)


# ROTATE IMAGE
def rotateImage(image, rect, angle):
    rotated = pygame.transform.rotate(image, angle)
    rotatedRect = rotated.get_rect(center=rect.center)
    return rotated,rotatedRect


# REVERSE OBSTACLE MOVEMENT DIRECTION
def movementReverse(direction):
    if direction == "N": return "S"           
    elif direction == "S": return "N"                     
    elif direction == "E": return "W"           
    elif direction == "W": return "E"          
    elif direction == "NW": return "SE"         
    elif direction == "NE": return "SW"          
    elif direction == "SE": return "NW"
    elif direction == "SW": return "NE"


def randomEightDirection():
    directions = ["N","S","E","W","NW","SW","NE","SE"]
    direction = directions[random.randint(0, len(directions)-1)]
    return direction
    
    
# OBSTACLE POSITION GENERATION
def getMovement(eightDirections):
    top,bottom,left,right = [],[],[],[]
    
    if eightDirections: top, bottom, left, right = topDir, bottomDir, leftDir, rightDir
    else: top, bottom, left, right, = restrictedTopDir, restrictedBottomDir, restrictedLeftDir, restrictedRightDir
    X = random.randint(0, screenSize[0])
    Y = random.randint(0, screenSize[1])
    
    lowerX = random.randint(0, screenSize[0] * 0.05)
    upperX =  random.randint(screenSize[0] * 0.95, screenSize[0])
    lowerY  = random.randint(0, screenSize[1] * 0.05)
    upperY = random.randint(screenSize[1] * 0.95, screenSize[1])
    
    topDirection = top[random.randint(0, len(top) - 1)]
    leftDirection = left[random.randint(0, len(left) - 1)]
    bottomDirection = bottom[random.randint(0, len(bottom) - 1)]
    rightDirection = right[random.randint(0, len(right) - 1)]
    
    topBound = [X, lowerY, topDirection]
    leftBound = [lowerX, Y, leftDirection]
    bottomBound = [X, upperY, bottomDirection]
    rightBound = [upperX, Y, rightDirection]
 
    possible = [topBound, leftBound, rightBound, bottomBound]
    movement = possible[ random.randint(0, len(possible) - 1) ]
    
    position = [movement[0], movement[1]]
    direction = movement[2]
    move = [position,direction]
    return move 


# OBSTACLE MOVEMENT
def obstacleMove(obstacles):
    for obs in obstacles:
        position = obs.rect.center 
        if "N" in obs.direction: obs.rect.centery -= obs.speed    
        if "S" in obs.direction: obs.rect.centery += obs.speed      
        if "E" in obs.direction: obs.rect.centerx += obs.speed 
        if "W" in obs.direction: obs.rect.centerx -= obs.speed


# OFF SCREEN OBSTACLE REMOVAL
def obstacleRemove(obstacles):
    for obs in obstacles:
   
        if obs.rect.centerx > screenSize[0] or obs.rect.centerx < 0:
            obstacles.remove(obs)
            obs.kill()

        elif obs.rect.centery > screenSize[1] or obs.rect.centery < 0:
            obs.kill()
            obstacles.remove(obs)


# OBSTACLE BOUNCING
def bounceObstacle(obstacles):
    for obs in obstacles:
        direction = obs.direction
        if obs.rect.centery  > screenSize[1]: obs.direction = movementReverse(direction)    
        if obs.rect.centery < 0: obs.direction = movementReverse(direction) 
        if obs.rect.centerx > screenSize[0]: obs.direction = movementReverse(direction)   
        if obs.rect.centerx < 0: obs.direction = movementReverse(direction)
 
 
# OBSTACLE WRAPPING
def wrapObstacle(obstacles):
    for obs in obstacles:
        if obs.rect.centery  > screenSize[1]: obs.rect.centery = 0  
        if obs.rect.centery < 0: obs.rect.centery = screenSize[1]                      
        if obs.rect.centerx > screenSize[0]: obs.rect.centerx = 0      
        if obs.rect.centerx < 0: obs.rect.centerx = screenSize[0]


game = Game()
menu = Menu()


def gameLoop():
    
    game.resetGameConstants()
    game.pauseCount = 0
    game.resetClock()
    player = Player()
    events = Event()
    events.set()    

    if game.mainMenu: menu.home(game,player)
    else:
        for i in range(game.savedShipNum): player.nextSpaceShip()

    obstacles = pygame.sprite.Group()
    running = True
    
    # GAME LOOP
    while running: game.update(player,obstacles,menu,events)


if __name__ == '__main__': gameLoop()
    
    
    
    



