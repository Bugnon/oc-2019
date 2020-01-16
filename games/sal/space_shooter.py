from __future__ import division
import pygame
import random
from os import path

'''
All variable related to the working of the game.
end_game: If game is over
WIDTH,HEIGHT: dimensions of the window
FPS: Frames per second.
Color Definations
'''
end_game=False
img_dir = path.join(path.dirname(__file__), 'images')
sound_folder = path.join(path.dirname(__file__), 'sounds')
WIDTH = 480
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
pygame.init() # initializing the game
pygame.mixer.init()  # For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # defining screen size
pygame.display.set_caption("Space Shooter") # caption of window
clock = pygame.time.Clock()     #For syncing the FPS
font_name = pygame.font.match_font('arial') # font for text


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
'''
Main Menu.
'''
def main_menu():
    global screen
    screen.fill(BLACK)
    pygame.display.update()
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN: # if down key is pressed
            if ev.key == pygame.K_RETURN: # if enter key is pressed
                break
            elif ev.key == pygame.K_q:#If q key is pressed.
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT: 
                pygame.quit()
                quit() 
        else:
            if end_game == True: #If game was over rather than a new game
                draw_text(screen, "GAME OVER", 30, WIDTH/2, (HEIGHT/2)-70)
            draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH/2, HEIGHT/2)
            draw_text(screen, "or [Q] To Quit", 30, WIDTH/2, (HEIGHT/2)+40)
            pygame.display.update()

    ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg')) #Ready music
    ready.play()
    screen.fill(BLACK)#Blank the screen with black color
    draw_text(screen, "GET READY!", 30, WIDTH/2, HEIGHT/2)
    pygame.display.update()
'''
This method create new enemies on the screen after they have got destroyed or initializing them.
'''
def newEnemy():
    Enemy_element = Enemy()
    all_sprites.add(Enemy_element)
    Enemys.add(Enemy_element)

'''
Defining the Explosion class
'''
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size #Size of explosion
        self.image = explosion_anim[self.size][0] #Image to show when explosion occur.
        self.rect = self.image.get_rect() # Explosion rectangle to draw.
        self.rect.center = center 
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate: # Syncing frame rate and then killing the objects.
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

'''
Player class.
'''
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))# scale the player img down
        self.image.set_colorkey(BLACK)#setting image color background as black
        self.rect = self.image.get_rect() # rect to draw
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 #speed on x_axis
        self.speedy = 0 # speed on y_axis
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3 #lives
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0 # speed x
        self.speedy = 0
        '''
        Checking which key was pressed and act accordingly 
        '''
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx += -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx += 5
        if keystate[pygame.K_DOWN]:
            self.speedy += 5
        elif keystate[pygame.K_UP]:
            self.speedy += -5
        #Fire weapons by holding spacebar
        if keystate[pygame.K_SPACE]:
            self.shoot()
        
        # check for the borders at the left and right and up , down
        if self.rect.right > WIDTH:
            self.rect.right = self.rect.right-WIDTH
        if self.rect.left < 0:
            self.rect.left = self.rect.left + WIDTH
        if self.rect.top > HEIGHT:
            self.rect.top = 0
        if self.rect.bottom < 0:
            self.rect.bottom = HEIGHT
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        # to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)



# defines the enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
    
        pygame.sprite.Sprite.__init__(self)
        self.image = ufo_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = 5 
        self.speedx = 0



    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)        ## vitesse des ennemis aléatoire 


# defines the sprite for bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

'''
Background image
'''
background = pygame.image.load(path.join(img_dir, 'space.jpg')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()

'''
Spaceship initializing
'''
player_img = pygame.image.load(path.join(img_dir, 'spaceship.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (40, 30))
player_mini_img.set_colorkey(BLACK)

'''
Bullet object initializing
UFO object initializing
'''
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
ufo_image =pygame.image.load(path.join(img_dir, 'ufo.png')).convert()
ufo_image.set_colorkey(BLACK)
# UFO explosion
explosion_anim = {}
explosion_anim['sm'] = [] # UFO explosions
explosion_anim['player'] = [] #player explosion
filename = 'regularExplosion00.png' #explosion image
img = pygame.image.load(path.join(img_dir, filename)).convert()
img.set_colorkey(BLACK)
img_sm = pygame.transform.scale(img, (32, 32)) #explosion size
explosion_anim['sm'].append(img_sm) #explosion to animate
filename = 'sonicExplosion00.png' # explosion when player is destroyed
img = pygame.image.load(path.join(img_dir, filename)).convert() #loading player explosion image
img.set_colorkey(BLACK)
explosion_anim['player'].append(img)


pygame.mixer.music.set_volume(0.2)      # simmered the sound down a little
running = True #variable to check whether game is running or not.
menu_display = True
while running:
    if menu_display:
        main_menu()
        pygame.time.wait(3000)

        pygame.mixer.music.stop()
        pygame.mixer.music.load(path.join(sound_folder, 'Intergalactic Odyssey.ogg'))
        pygame.mixer.music.play(-1)     ## makes the gameplay sound in an endless loop
        
        menu_display = False
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        Enemys = pygame.sprite.Group()
        for i in range(10):
            newEnemy()

        # group for bullets
        bullets = pygame.sprite.Group()

        # Score board variable
        score = 0
        

    clock.tick(FPS)     # will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        # listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

      

    #2 Update
    all_sprites.update()
    #Checking when  UFO and bullets collide ,  which means UFO object is destroyed
    hits = pygame.sprite.groupcollide(Enemys, bullets, True, True)
    for hit in hits:
        score += 10
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newEnemy()
    #Checking when  Player and UFO collide ,  which means PLayer object is destroyed
    hits = pygame.sprite.spritecollide(player, Enemys, True, pygame.sprite.collide_circle)        ## gives back a list, True makes the Enemy element disappear
    for hit in hits:
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newEnemy() 
        death_explosion = Explosion(player.rect.center, 'player')
        all_sprites.add(death_explosion)
        player.lives -= 1


    # if player died and the explosion has finished, end game
    if player.lives == 0:
        menu_display = True
        end_game=True
        pygame.display.update()

    #3 Draw/render
    screen.fill(BLACK)
    # draw the stargaze.png image
    screen.blit(background, background_rect)

    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)     # 10px down from the screen

    pygame.display.flip()       

pygame.quit()
