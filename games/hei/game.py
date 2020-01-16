import pygame
import math

import random
from pygame import mixer

def Spacegame():
    #initialize pygame
    pygame.init()

    #create the screen
    screen = pygame.display.set_mode((700, 600))

    #Background
    background = pygame.image.load("images/spacebackground.jpg")

    #background sound
    # mixer.music.load("sounds/background.wav")
    # mixer.music.play(-1)

    #Title and Icon
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load("images/spaceship.png")
    pygame.display.set_icon(icon)

    #player
    playerImg = pygame.image.load("images/player.png")
    playerx = 330
    playery = 480
    playerx_change = 0

    #Enemy
    enemyImg = []
    enemyy = []
    enemyx = []
    enemyx_change = []
    enemyy_change = []
    num_of_enemies = 10

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load("images/enemy.png"))
        enemyx.append(random.randint(0, 636))
        enemyy.append(random.randint(50, 150))
        enemyx_change.append(random.randint(1, 4))
        enemyy_change.append(40)

    #Bullet

    #Ready means you cant see the bullet on the screen
    #fire - the bullet is currently moving

    bulletImg = pygame.image.load("images/bullet.png")
    bulletx = 0
    bullety = 480
    bulletx_change = 0
    bullety_change = 30
    bullet_state = "ready"

    #score
    score_value = 0
    font = pygame.font.Font("minecraft.ttf", 32)
    textx = 10
    texty = 10

    #game over Text
    over_font = pygame.font.Font("minecraft.ttf", 64)
    enemy_font = pygame.font.Font("minecraft.ttf", 32)
    win_font = pygame.font.Font("minecraft.ttf", 64)

    def show_score(x, y):
        score = font.render("Score: " + str(score_value) + " /50", True, (255, 255, 255))

        screen.blit(score, (x, y))

        
    def win_game():
        mixer.music.stop()
        win_Sound = mixer.Sound("sounds/win.wav")
        win_Sound.play()
        win_text = win_font.render("YOU WIN", True, (255, 255, 255))
        screen.blit(win_text, (200, 250))
        
        

        
    def game_over_text():
        mixer.music.stop()
        game_over_Sound = mixer.Sound("sounds/game_over.wav")
        game_over_Sound.play()
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        enemy_text = enemy_font.render("The aliens got too close to the Spaceship!" , True, (255, 255, 255))
        screen.blit(over_text, (175, 250))
        screen.blit(enemy_text, (75, 300))
        
        
        
    def player(x, y):
        screen.blit(playerImg, (x, y))
      
      
    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))


    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))

       
    def Collision(enemyx, enemyy, bulletx, bullety):
        distance = math.sqrt((math.pow(enemyx-bulletx,2))+ (math.pow(enemyy - bullety,2)))
        if distance < 27:
            return True
        else:
            return False
  
    #Game loop
    print('instantiate SpaceGame')
    running = True
    while running:
        
        #rgb background
        screen.fill((0, 0, 255))
        #background image
        screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.music.stop()
                running = False
        
            #if keystroke is pressed check whether it is right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    playerx_change = -6
                if event.key == pygame.K_d:
                    playerx_change = 6
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bullet_Sound = mixer.Sound("sounds/laser.wav")
                        bullet_Sound.play()
                        bullet_state = "fire"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound("sounds/laser.wav")
                    bullet_Sound.play()
                    bullet_state = "fire"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    playerx_change = 0

        
        #change the position of the spacecraft
        #checking for boundaries so that it doesnt go out of bounds
        playerx += playerx_change
        
        if playerx <= 0:
            playerx = 0
        elif playerx >= 637:
            playerx = 636
            
        #Enemy movement    
        for i in range (num_of_enemies):
            
            #Win text
            if score_value >= 50:
                for k in range(num_of_enemies):
                    enemyy[k] = 2000
                    
                win_game()
                
               
                break
            
            #Game Over
            if enemyy[i] > 440:
                for j in range (num_of_enemies):
                    enemyy[j] = 2000
                        
                game_over_text()
                
                break
            
            enemyx[i] += enemyx_change[i]
            if enemyx[i] <= 0:
                enemyx_change[i] = random.randint(1, 6)
                enemyy[i] += enemyy_change[i]
            elif enemyx[i] >= 636:
                enemyx_change[i] = -random.randint(1, 6)
                enemyy[i] += enemyy_change[i]
                
            #collision
            collision = Collision(enemyx[i], enemyy[i], bulletx, bullety)
            if collision:
                explosion_Sound = mixer.Sound("sounds/explosion.wav")
                explosion_Sound.play()
                bullety = 480
                bullet_state = "ready"
                score_value += 1
                enemyx[i] = random.randint(0, 636)
                enemyy[i] = random.randint(50, 150)
                
            enemy(enemyx[i], enemyy[i], i)
        #Bullet movemement
        if bullety <= 0:
            bullety = 480
            bullet_state = "ready"
           
            
           
        if bullet_state is "fire":
            if bulletx == 0:
                bulletx = playerx
            fire_bullet(bulletx, bullety )
            
            bullety -= bullety_change
        else:
            bulletx = 0
         
        player(playerx, playery)
        show_score(textx, texty)
        pygame.display.update()
     
    return
 
    pygame.quit()
    
