"""
This is a game with a space theme (doc_string).
It uses object-oriented programming.
Marc PORTA
"""

import pygame
import sys
import random
from pygame.locals import *


class Player:
    """The player can move."""
    SPEED = 0.5
    def __init__(self):
        
        self.x = 100
        self.y = 100
        self.w = 50
        self.h = 50
        self.dx = 0
        self.dy = 0
        self.color = Color("green")
        self.time = 0
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.life = 10
        
    def do_event(self, event):
        pass
    
    
    def update(self):
        self.move()
        self.rect = Rect(self.x, self.y, self.w, self.h)
        if self.time > 0:
            self.time -= 1 * app.clock.get_time()/1000
    
    def draw(self):
        app.camera.draw_rect_player(self)
        
    def move(self):
        self.x += self.dx * Player.SPEED * app.clock.get_time()
        self.y += self.dy * Player.SPEED * app.clock.get_time()
        if self.y < 0:
            self.y = 0
        elif self.y > App.HEIGHT:
            self.y = App.HEIGHT
            
    def do_input(self, input):
            if input[K_RIGHT] == input[K_LEFT]:
                self.dx = 0
            elif input[K_RIGHT] :
                self.dx = 1
            elif input[K_LEFT]:
                self.dx = -1
            if input[K_DOWN] == input[K_UP]:
                self.dy = 0
            elif input[K_DOWN]:
                self.dy = 1
            elif input [K_UP]:
                self.dy = -1
            if input [K_SPACE]:
                self.shot()
    
    def shot(self):
        if self.time <= 0:
            Bullet.shot(self, 1)
            self.time = 0.2
            
    def damage(self):
        self.life -= 1
        if self.life <= 0:
            app.end_game(False)
  
class Enemy:
    """The player must avoid the enemies."""
    ENEMY_ZONE = 10000
    def __init__(self):
        self.x = random.randint(0, self.ENEMY_ZONE)
        self.y = random.randint(0 , App.HEIGHT)
        self.w = 30
        self.h = 30
        self.color = Color("blue")
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.life = 1
        
    def update(self):
        self.rect = Rect(self.x, self.y, self.w, self.h)
        
    
    def draw(self):
        app.camera.draw_rect(self)
    

    
    def remove(self):
        app.score += 1 * self.w
        app.enemies.remove(self)
    
    def damage(self):
        self.life -= 1
        if self.life <= 0:
            self.remove()
            
            
class Bullet:
    """
    Bullet to shot
    """
    def __init__(self, x, y, dx=1):
        self.x = x
        self.y = y
        self.w = 30
        self.h = 5
        self.dx = dx
        self.dy = 0
        self.color = Color("red")
        self.time = 1
        self.rect = Rect(self.x, self.y, self.w, self.h)
        
    def update(self):
        self.x += self.dx * app.clock.get_time()
        self.y += self.dy
        self.time -= 1 * app.clock.get_time()/1000
        if self.time < 0:
            self.remove()
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.collide()
            
        
    
    def draw(self):
        app.camera.draw_rect(self)
    
    @staticmethod   
    def shot(other, dx):
        app.bullets.append(Bullet(other.x, other.y + 0.5 * other.h, dx))
      
        
        
    
    def remove(self):
        try:
            app.bullets.remove(self)
        except:
            pass

    def collide(self):
        for enemy in app.enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.damage()
                self.remove()


class BulletBoss(Bullet):
    """
    Bullet of the boss
    """
    def __init__(self, x, y, dx=1):
        super().__init__(x, y, dx)
        self.h = 10
    
    @staticmethod   
    def shot(other, dx):
        app.bullets.append(BulletBoss(other.x, other.y + 0.25 * other.h,
         dx))
        app.bullets.append(BulletBoss(other.x, other.y + 0.5 * other.h,
         dx))
        app.bullets.append(BulletBoss(other.x, other.y + 0.75 * other.h,
         dx))
    
    def collide(self):
        if self.rect.colliderect(app.player.rect):
            app.player.damage()
            self.remove()
        
        
        
        
    
class App:
    WIDTH = 1280
    HEIGHT = 600
    CAPTION = 'Space Game'
    sreen = None
    
    def __init__(self):
        print('initalize app')
        pygame.init()
        App.screen = pygame.display.set_mode((App.WIDTH, App.HEIGHT))
        pygame.display.set_caption(App.CAPTION)


        self.player = Player()
        self.enemies = []
        self.__bullets = []
        self.clock = pygame.time.Clock()
        for i in range(100):
            self.enemies.append(Enemy())
        self.enemies.append(Boss())
        self.running = True
        self.score = 0
        self.text = Text(f'Score: {self.score}', (20, 20))
        self.input = Input()
        self.camera = Camera()
        
        
        
    def run(self):
        print('run app')
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)

            self.update()
            self.draw()
            
        pygame.quit()
        sys.exit()
            
            
    def do_event(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN or KEYUP:
            self.input.do_event(event)
            self.do_input()
    
    def do_input(self):
        self.player.do_input(self.input.input)
            
    def update(self):
        self.clock.tick()
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        for bullet in self.bullets:
            bullet.update()
            
    def draw(self):
        App.screen.fill(Color('black'))
        for enemy in self.enemies:
            enemy.draw()
        
        for bullet in self.bullets:
            bullet.draw()
        self.player.draw()
        self.text.set(f'Score: {self.score}')
        self.text.draw()
        pygame.display.update()
     
    @property
    def bullets(self):
        return self.__bullets
     
     
    @bullets.setter 
    def bullets(self, bullets):
        self.__bullets = bullets
        
    def end_game(self, win):
        if win:
            print("You win")
        else:
            print("You lose")
        
        self.running = False
        
    
    #def bullets(self, bullet):
    #   self.__bullets.append(bullet)
    

class Text:
    """Create a text object."""
    
    def __init__(self, text, pos):
        self.font = pygame.font.SysFont(None, 36)
        self.rect = Rect(pos, (0, 0))
        self.set(text)
        
    def set(self, text):
        self.text = text
        self.img = self.font.render(self.text, True, Color('white'))
        self.rect.size = self.img.get_size()
        
    def draw(self):
        App.screen.blit(self.img, self.rect)
        

class Input():
    """
    Keep in memory the keys press
    """
    def __init__ (self):
        self.__input = {
            K_RIGHT : False, K_LEFT : False, K_DOWN : False,
             K_UP : False, K_SPACE : False,
                       }
        
    def do_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT :
                self.input[K_RIGHT] = True 
            elif event.key == K_LEFT:
                self.input[K_LEFT] = True
            elif event.key == K_DOWN:
                self.input[K_DOWN] = True
            elif event.key == K_UP:
                self.input[K_UP] = True
            elif event.key == K_SPACE:
                self.input[K_SPACE] = True
        elif event.type == KEYUP:
            if event.key == K_RIGHT :
                self.input[K_RIGHT] = False
            elif event.key == K_LEFT:
                self.input[K_LEFT] = False
            elif event.key == K_DOWN:
                self.input[K_DOWN] = False
            elif event.key == K_UP:
                self.input[K_UP] = False
            elif event.key == K_SPACE:
                self.input[K_SPACE] = False
                
    @property
    def input(self):
        return self.__input
    
class Camera():
    """
    to do a scrolling
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        
    def update(self):
        pass
    
    def draw_rect(self, other):
        r = other.rect
        rect_s = Rect(r.left - self.x, r.top - self.y, r.width,
         r.height) 
        pygame.draw.rect(App.screen, other.color, rect_s)
    
    def draw_rect_player(self, other):
        r = other.rect
        #if r.left > App.WIDTH/2:
        self.x = r.left-App.WIDTH/4
        rect_s = Rect(r.left - self.x, r.top - self.y, r.width,
         r.height) 
        pygame.draw.rect(App.screen, other.color, rect_s)
        

class Boss(Enemy):
    """ 
        Big enemy
    """
    def __init__(self):
        super().__init__()
        self.x = 10100
        self.h = 300
        self.y = App.HEIGHT/2 - self.h/2
        self.w = 300
        self.dx = 0
        self.dy = 0
        self.color = Color("blue")
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.life = 12
        self._attack = False
        self.time = 0
        self.speed = 0.2
        self.time_dy = 0
        
    def update(self):
        self.rect = Rect(self.x, self.y, self.w, self.h)
        if self._attack:
            self.shot()
            self.move()
        if self.time > 0:
            self.time -= 1 * app.clock.get_time()/1000
        if self.time_dy > 0:
            self.time_dy -= 1 * app.clock.get_time()/1000
        
        
    def damage(self):
        self.life -= 1
        if self.life <= 0:
            app.end_game(True)
           # self.remove()
        self._attack = True
    
    def shot(self):
        if self.time <= 0:
            BulletBoss.shot(self, -1)
            self.time = 0.2
            
    def move(self):
        if self.time_dy <= 0:
            self.dy = random.randint(-1, 1)
            self.time_dy = 1
        self.y += self.dy * self.speed * app.clock.get_time()
        self.y = self.y%App.HEIGHT    
        

        

            
        
if __name__ == '__main__':
    app = App()
    app.run()
