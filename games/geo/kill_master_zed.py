import pygame
import sys
import random
import math
import time
from pygame import mixer
from pygame.locals import *

# initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((1200, 600))

# Title and Icon
pygame.display.set_caption('Kill Master Zed')
icon = pygame.image.load('images/icon.png')
icon = pygame.transform.scale(icon,(64,64))
pygame.display.set_icon(icon)

# Background
backgroundImg = pygame.image.load('images/Space Background.png').convert_alpha()
backgroundImg = pygame.transform.scale(backgroundImg,(1200,620))

# Background Music
# music = mixer.music.load('SPACE GAME SONG.mp3')
# music = mixer.music.play(-1)
# music = mixer.music.set_volume(0.4)

# Other Musics
play_boss = True

play_winmusic = True

#Sounds
no = mixer.Sound('sounds/no.wav')
no.set_volume(0.3)
play_no = True

laugh = mixer.Sound('sounds/boss_laugh.wav')
laugh.set_volume(0.3)
play_laugh = True

win = mixer.Sound('sounds/win_sound.wav')
win.set_volume(0.6)
play_win = True


# Player
playerImg = pygame.image.load('images/Captain.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg,(100,100))
playerX = 150
playerY = 250
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies) :
    enemyImg.append(pygame.image.load('images/enemy_big.png').convert_alpha())
    enemyX.append(random.randint(1200, 1300))
    enemyY.append(random.randint(0,500))
    enemyX_change.append(-0.3)
    enemyY_change.append(0.1)
    
# Boss
bossImg = pygame.image.load('images/boss.png').convert_alpha()
bossImg = pygame.transform.scale(bossImg,(530,530))
bossX = 1200
bossY = 40
bossX_change = 0

# Laser1
laser1Img = pygame.image.load('images/laser_big.png').convert_alpha()
laser1Img = pygame.transform.scale(laser1Img,(32,32))
laser1Img = pygame.transform.rotate(laser1Img,(90))
laser1X = 150
laser1Y = 0
laser1X_change = 6
laser1Y_change = 0
laser1_state = 'ready'

# Laser2
laser2Img = pygame.image.load('images/laser_big.png').convert_alpha()
laser2Img = pygame.transform.scale(laser2Img,(32,32))
laser2Img = pygame.transform.rotate(laser2Img,(90))
laser2X = 150
laser2Y = 0
laser2X_change = 6
laser2Y_change = 0
laser2_state = 'ready'

# Score
score_value = 0
font = pygame.font.SysFont('magneto', 32)
textX = 10
textY = 10

# Boss Health
bosshealth = 50
bosshealth_change = -1
text2X = 250
text2Y = 2
boss_font = pygame.font.SysFont('BankGothic', 50)
health = True

# Game Over
over_font = pygame.font.SysFont('Elephant', 100)

#Boss Message
mess_font = pygame.font.SysFont('Tahoma', 30)
message = True

# Functions
def boss_mess() :
    mess = mess_font.render('The Boss has appeared ! Aim for the forehead!!!', True, (205,205,50))
    screen.blit(mess,(10,550))

def show_score(x, y):
    score = font.render('Score = ' + str(score_value), True, (40, 113, 134))
    screen.blit(score,(x,y))
    
def show_bosshealth() :
    health = boss_font.render('BOSS HEALTH = ' + str(bosshealth), True, (255,0,0))
    screen.blit(health,(300,10))
    
def game_over_text():
    over_text = over_font.render('GAME OVER', True, (175,0,42))
    screen.blit(over_text,(250,200))
    
def win_text() :
    over_text = over_font.render('YOU WIN', True, (255,215,0))
    screen.blit(over_text,(300,200))

def player(x,y):
    screen.blit(playerImg,(x,y))
    
def enemy(x,y, i):
    screen.blit(enemyImg[i],(x,y))
    
def boss(x,y) :    
    screen.blit(bossImg,(x,y))
    
def fire_laser1(x,y):
    global laser1_state
    laser1_state = 'fire'
    screen.blit(laser1Img,(x + 80 ,y - 5))
    
def fire_laser2(x,y):
    global laser2_state
    laser2_state = 'fire'
    screen.blit(laser2Img,(x + 80 ,y + 75))
    
def isCollision1(enemyX, enemyY, laser1X, laser1Y):
    distance = math.sqrt((math.pow(enemyX - laser1X,2)) + (math.pow(enemyY - laser1Y,2)))
    if distance <= 40 :
        return True
    else :
        return False
    
def isCollision2(enemyX, enemyY, laser2X, laser2Y):
    distance = math.sqrt((math.pow(enemyX - laser2X,2)) + (math.pow(enemyY - laser2Y,2)))
    if distance <= 40 :
        return True
    else :
        return False
    
def isCollisionBoss1(bossX, bossY, laser1X, laser1Y):
    distance = math.sqrt((math.pow(bossX - laser1X,2)) + (math.pow(bossY - laser1Y,2)))
    if distance <= 40 :
        return True
    else :
        return False
    
def isCollisionBoss2(bossX, bossY, laser2X, laser2Y):
    distance = math.sqrt((math.pow(bossX - laser2X,2)) + (math.pow(bossY - laser2Y,2)))
    if distance <= 40 :
        return True
    else :
        return False
    
# Game Loop
running = True
while running:
    
    # Background (bottom)
    screen.blit(backgroundImg, [0,0])
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    
        # Keys
        if event.type == pygame.KEYDOWN :
        # Player Control
            #Forward and backwards
            if event.key == pygame.K_LEFT : 
                playerX_change = -0.7
            if event.key == pygame.K_RIGHT :
                playerX_change = 0.35
            #Up and down
            if event.key == pygame.K_UP :
                playerY_change = -0.5
            if event.key == pygame.K_DOWN :
                playerY_change = 0.5
                
        #Laser Shoot
            if event.key == pygame.K_SPACE :
                if laser1_state and laser2_state is 'ready':
                    laser_Sound = mixer.Sound('sounds/shot.wav')
                    laser_Sound.play()
                    laser_Sound.set_volume(0.2)
                    laser1Y = playerY
                    laser2Y = playerY
                    fire_laser1(laser1X, playerY)
                    fire_laser2(laser2X, playerY)
                          
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                playerY_change = 0
                
            

    
    # Player Boundaries
    playerX += playerX_change
    if playerX >= 1100 :
        playerX = 1100
    elif playerX <= -200 :
        playerX = -200
        
    playerY += playerY_change
    if playerY <= 0 :
        playerY = 0
    elif playerY >= 500 :
        playerY = 500
    
    for i in range(num_of_enemies) :
        
        # Game Over
        if enemyX[i] < 0 :
            for j in range (num_of_enemies) :
                enemyX[j] = -1000
            mixer.music.stop()
            if play_no :
                play_no = False
                no.play(0)
            game_over_text()
            break

        if bossX < 0 :
            bossX_change = -1
            mixer.music.stop()
            if play_no :
                play_no = False
                no.play(0)
            game_over_text()
            
        
        #Enemy Movement and Boundaries
        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0 :
            enemyY_change[i] = 0.1
        elif enemyY[i] >= 500 :
            enemyY_change[i] = -0.1
            
        # Collision
        collision1 = isCollision1(enemyX[i], enemyY[i], laser1X, laser1Y)
        collision2 = isCollision2(enemyX[i], enemyY[i], laser2X, laser2Y)
        if collision1 or collision2 :
            explosion_Sound = mixer.Sound('sounds/Explosion.wav')
            explosion_Sound.play()
            explosion_Sound.set_volume(0.2)
            laser1X = 150
            laser1_state = 'ready'
            laser2X = 150
            laser2_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(1200, 1300)
            enemyY[i] = random.randint(0,500)

            # Speed increases each time an enemy is killed
            enemyX_change[i] -= 0.025
            
        # Spawn Boss if reach a certain score
        if score_value == 50 :
            bossX += bossX_change
            enemyX[i] = 3000 
            enemyX_change[i] = 0
            bossX_change = -0.045
            if health :
                show_bosshealth()
            if message :
                boss_mess()
            if play_laugh :
                play_laugh = False
                laugh.play(0)
            if play_boss :
                play_boss = False
                # boss_music = mixer.music.load('boss_song2.mp3')
                # boss_music = mixer.music.play()

            #Boss Collision
            collisionboss1 = isCollisionBoss1(bossX, bossY, laser1X, laser1Y)
            collisionboss2 = isCollisionBoss2(bossX, bossY, laser2X, laser2Y)
            if collisionboss1 or collisionboss2 :
                boss_sound = mixer.Sound('sounds/boss_sound.wav')
                boss_sound.play()
                laser1X = 150
                laser1_state = 'ready'
                laser2X = 150
                laser2_state = 'ready'
                bosshealth -= bosshealth_change
                bosshealth_change = 1
                
        #Dispawn Boss if Health < 0        
        if bosshealth < 0 :
            bossX = 4000
            win_text()
            message = False
            health = False
            if play_win :
                play_win = False
                win.play(0)
            if play_winmusic :
                play_winmusic = False

                       
        enemy(enemyX[i],enemyY[i], i)
        
    # Laser movement
    if laser1X and laser2X >=1200 :
        laser1X = playerX
        laser2X = playerX
        laser1_state = 'ready'
        laser2_state = 'ready'
    
    
    if laser1_state is 'fire' :
        fire_laser1(laser1X, laser1Y)
        laser1X += laser1X_change
    if laser2_state is 'fire' :
        fire_laser2(laser2X, laser2Y)
        laser2X += laser2X_change
        

    player(playerX,playerY)
    boss(bossX, bossY)
    show_score(textX, textY)
    
    pygame.display.update()