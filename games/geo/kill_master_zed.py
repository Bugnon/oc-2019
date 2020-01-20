import pygame
import sys
import random
import math
import time
from pygame import mixer
from pygame.locals import *

# initialize Pygame
pygame.init()
RED = (255, 0, 0)
debug = True
size = 1200, 600

# Create the screen
screen = pygame.display.set_mode(size)

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

class Player:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.img = img
        self.rect = Rect((x, y), self.img.get_size())

    def do_event(self, event):
        if event.type == KEYDOWN :
            if event.key == K_LEFT : 
                player.dx = -0.7
            elif event.key == K_RIGHT :
                player.dx = 0.35
            elif event.key == K_UP :
                player.dy = -0.5
            elif event.key == K_DOWN :
                player.dy = 0.5

        if event.type == KEYUP :
            if event.key in (K_LEFT, K_RIGHT) :
                player.dx = 0
            elif event.key in (K_UP, K_DOWN):
                player.dy = 0

    def update(self):
        self.x += self.dx
        self.x = min(1100, self.x)
        self.x = max(-200, self.x)

        self.y += self.dy
        self.y = max(0, self.y)
        self.y = min(500, self.y)

        self.rect.left = self.x
        self.rect.top = self.y     

    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        if debug:
            pygame.draw.rect(screen, RED, self.rect, 1)

# Player
playerImg = pygame.image.load('images/Captain.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg,(100,100))
player = Player(150, 250, playerImg)

class Enemy:
    def __init__(self, x, y, dx, dy, img):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.img = img
        self.rect = Rect((x, y), self.img.get_size())

    def update(self):
        self.x += self.dx
        self.x = min(1100, self.x)
        self.x = max(-200, self.x)

        self.y += self.dy
        self.y = max(0, self.y)
        self.y = min(500, self.y)

        if self.y <= 0:
            self.dy = 0.1
        elif self.y >= 500:
            self.dy = -0.1

        self.rect.left = self.x
        self.rect.top = self.y     

    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        if debug:
            pygame.draw.rect(screen, RED, self.rect, 1)


# Enemy
enemies = []
num_of_enemies = 5

enemy_img = pygame.image.load('images/enemy_big.png').convert_alpha()
for i in range(num_of_enemies) :
    x = random.randint(1200, 1300)
    y = random.randint(0,500)
    dx = -random.randint(2, 4)/10
    enemy = Enemy(x, y, dx, 0.1, enemy_img)
    enemies.append(enemy)
    
# Boss
bossImg = pygame.image.load('images/boss.png').convert_alpha()
bossImg = pygame.transform.scale(bossImg,(530,530))
bossX = 1200
bossY = 40
bossX_change = 0

class Laser(Enemy):
    def __init__(self, x, y, dx, dy, img):
        super().__init__(x, y, dx, dy, img)
        self.state = 'ready'
        self.sound = mixer.Sound('sounds/shot.wav')

    def do_event(self, event):
        global player
        if event.type == KEYDOWN:
            if event.key == K_SPACE :
                # if self.state == 'ready':
                    self.sound.play()
                    self.sound.set_volume(0.2)
                    self.x = player.x
                    self.y = player.y

# Laser1
laserImg = pygame.image.load('images/laser_big.png').convert_alpha()
laserImg = pygame.transform.scale(laserImg,(32,32))
laserImg = pygame.transform.rotate(laserImg,(90))
laser = Laser(150, 0, 6, 0, laserImg)

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
    
def boss(x,y) :    
    screen.blit(bossImg,(x,y))
    
def isCollision(enemyX, enemyY, laser1X, laser1Y):
    distance = math.sqrt((math.pow(enemyX - laser1X,2)) + (math.pow(enemyY - laser1Y,2)))
    if debug:
        pygame.draw.line(screen, RED, (enemyX, enemyY), (laser1X, laser1Y), 1)
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
        if event.type == QUIT:
            running = False
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_d:
                debug = not debug
    
        player.do_event(event)
        laser.do_event(event)

        # # Keys
        # if event.type == pygame.KEYDOWN :
                
        # #Laser Shoot
        #     if event.key == pygame.K_SPACE :
        #         if laser1_state and laser2_state is 'ready':
        #             laser_Sound = mixer.Sound('sounds/shot.wav')
        #             laser_Sound.play()
        #             laser_Sound.set_volume(0.2)
        #             laser1Y = player.y
        #             laser2Y = player.y
        #             fire_laser1(laser1X, player.y)
        #             fire_laser2(laser2X, player.y)

    player.update()
    laser.update()
    
    # for i in range(num_of_enemies) :
    for enemy in enemies :

        # Game Over
        if enemy.x < 0 :
            for e in enemies :
                e.x = -1000
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
        enemy.update()
            
        # Collision
        collision = isCollision(enemy.x, enemy.y, laser.x, laser.y)
        # collision2 = isCollision2(enemy.x, enemy.y, laser2.x, laser2.y)
        if collision :
            explosion_Sound = mixer.Sound('sounds/Explosion.wav')
            explosion_Sound.play()
            explosion_Sound.set_volume(0.2)
            laser.x = 150
            laser.state = 'ready'
            # laser2.x = 150
            # laser2.state = 'ready'
            score_value += 1
            enemy.x = random.randint(1200, 1300)
            enemy.y = random.randint(0,500)

            # Speed increases each time an enemy is killed
            enemy.dx -= 0.025
            
        # Spawn Boss if reach a certain score
        if score_value == 50 :
            bossX += bossX_change
            enemy.x = 3000 
            enemy.dx = 0
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
            collisionboss1 = isCollisionBoss1(bossX, bossY, laser1.x, laser1.y)
            collisionboss2 = isCollisionBoss2(bossX, bossY, laser2.x, laser2.y)
            if collisionboss1 or collisionboss2 :
                boss_sound = mixer.Sound('sounds/boss_sound.wav')
                boss_sound.play()
                laser.x = 150
                laser.state = 'ready'
                # laser2.x = 150
                # laser2.state = 'ready'
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

                       
        enemy.draw()
        
    # Laser movement
    if laser.x >= 1200 :
        laser.x = player.x
        # laser2.x = player.x
        laser.state = 'ready'
        # laser2.state = 'ready'
    
    
    # if laser1.state is 'fire' :
    #     laser1.fire()
    #     fire_laser1(laser1X, laser1Y)
    #     laser1X += laser1X_change
    # if laser2_state is 'fire' :
    #     fire_laser2(laser2X, laser2Y)
    #     laser2X += laser2X_change

    player.draw()
    laser.draw()
    boss(bossX, bossY)
    show_score(textX, textY)
    
    pygame.display.update()