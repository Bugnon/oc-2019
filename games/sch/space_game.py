"""
This is a game with a space theme (doc_string).
It uses oriented-object programming.

To play the game, you have to dodge the squares with the spaceship.

spaceship image: "Ship concept Sketches"
by Tano Bonfanti, licensed under CC BY-NC-ND 4.0
space image: https://www.flaticon.com/authors/freepik

"""

import pygame
import sys
from pygame.locals import *
import random
import math
# imports all needed modules

  mainClock = pygame.time.Clock()

class Player:
    """The player can move up and down."""
    def __init__(self):
        self.dy = 0 #player speed
        self.img0 = pygame.image.load('images/spaceship1.png')
        self.img = self.img0.copy()
        self.rect = self.img.get_rect()
        self.rect.center = (100, App.size/2)
        self.y = self.rect.center [1]
        #initializes vars, gets image and rect
        
    def do_event(self, event): #how player reacts to key presses
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.dy += 3
            elif event.key == K_UP:
                self.dy -= 3
        elif event.type == KEYUP:
            self.dy = 0
        
        center = self.rect.center
        self.rect = self.img.get_rect()
        self.rect.center = center
                
    def update(self): #updates player's position
        self.rect.move_ip(0, self.dy)
        self.rect.centery = self.rect.centery % App.size
    
    def draw(self): #draws the player
        App.screen.blit(self.img, self.rect)
        
    
class Enemy:
    """The player must avoid the enemies."""
    
    def __init__(self): #create initial vars
        self.x = random.randint(App.width/2, App.width)
        self.y = random.randint(0, App.size)
        self.w = 15
        self.h = 15
        self.dx = -1
        self.dy = 0
        self.color = Color('blue')
        #position (x and y), width and height, speed and color)
        
    def update(self): #updates enemy's position
        self.x += self.dx
        self.y += self.dy
        
        #enemies respawn
        if self.x <= 0:
            self.x = App.width
            self.y = random.randint(0, 2*App.width/4)
            
    def draw(self): #draws the enemy
        pygame.draw.rect(App.screen, self.color, Rect(self.x, self.y, self.w, self.h))
        
        
class App:
    width = 800
    size = 400
    caption = 'space game'
    screen = None
    """width and size of window and its caption.
    the variable screen enables us to re-use it simplier"""
    
    def __init__(self): #create initial vars
        print('initalize app')
        pygame.init()
        App.screen = pygame.display.set_mode((App.width, App.size))
        pygame.display.set_caption(App.caption)
        #opens screen and display message
        
        self.img = pygame.image.load('images/space.jpg')
        self.player = Player()
        self.enemies = []
        for i in range(3):
            self.enemies.append(Enemy())
        #creates background, player and 3 ennemies
        
        self.running = True

    def collide(self):
        for enemy in self.enemies:
            if player.colliderect(enemy) == True:
                enemies.remove(enemy)
    #defines collisions between player and enemies

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
            
        self.player.do_event(event)
        #game's event loop
            
    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        #updates the enemies and the player
            
    def draw(self):
        App.screen.blit(self.img, (0, 0))
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
        #draws background, player and enemies
         
        
if __name__ == '__main__':
    app = App() 
    app.run()
    #code to run the app