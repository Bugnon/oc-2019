"""
A little game in space. Demonstration of OOP
The player must avoid the asteroids as long as he can. The asteroids' spawn rate increase with time.

Resources:
Music: White Bat - Neon Dreams https://whitebataudio.com/downloads/neon-dreams/ (copyright free)
Everything else: Valentin Porchet

Note:   - Try to activate the App.debug cls var, the collisions aren't fixed yet ("game over" cames very soon)
        - The game speed and difficulty may increase with a slow computer (closer asteroids)
"""

import pygame
from pygame.locals import *
import time
import sys
import random

class Player:
    """playable character. Moves with arrow keys"""
    def __init__(self):
        print('player created')
        self.img = pygame.image.load('images/player.png')
        self.rect = self.img.get_rect()
        self.pos = (60, 150)
        self.rect.center = self.pos
        self.xspeed = 0
        self.yspeed = 0
 
    def do_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT: 
                self.xspeed = -2
            if event.key == K_RIGHT:
                self.xspeed = 2
            if event.key == K_DOWN: 
                self.yspeed = 2
            if event.key == K_UP:
                self.yspeed = -2


        elif event.type == KEYUP:
            if event.key == K_LEFT:
                self.xspeed = 0
            if event.key == K_RIGHT:
                self.xspeed = 0
            if event.key == K_DOWN:
                self.yspeed = 0
            if event.key == K_UP:
                self.yspeed = 0
        
    def update(self):
        self.rect.move_ip(self.xspeed,self.yspeed)

    def draw(self):
        App.screen.blit(self.img, self.rect)
        if App.debug:
            pygame.draw.rect(App.screen, Color('red'), self.rect, 1)


class Asteroid:
    """asteroid objects, can hit the player"""

    def __init__(self):
        self.img = pygame.image.load('images/asteroid.png')
        self.rect = self.img.get_rect()
        self.x = App.size[0] + 100
        self.y = random.randint(10, App.size[1]-10)
        self.rect.center = (self.x, self.y)
        self.speed = -1


    def update(self):
        self.rect.move_ip(self.speed, 0)
    
    def draw(self):
        App.screen.blit(self.img, self.rect)
        if App.debug:
            pygame.draw.rect(App.screen, Color('red'), self.rect, 1)

    def __del__(self): # makes the game run faster
        pass

class Text:
    """Create a text object."""
    
    def __init__(self, text, pos):
        self.font = pygame.font.SysFont('consolas', 36)
        self.rect = Rect(pos, (0, 0))
        self.set(text)
        
    def set(self, text):
        self.text = text
        self.img = self.font.render(self.text, True, Color('white'))
        self.rect.size = self.img.get_size()
        
    def draw(self):
        App.screen.blit(self.img, self.rect)


class App:
    """Main class of the game"""
    size = None
    screen = None
    debug = False

    def __init__(self):
        pygame.init()
        print('create app')
        pygame.display.set_caption('Space game Valentin')
        self.bg = pygame.image.load('images/bg.png')
        App.size = self.bg.get_size()
        App.screen = pygame.display.set_mode(App.size)
        self.running = True
        self.asteroids = []
        self.time = None
        self.start = None
        self.game_over = False

        self.music = pygame.mixer.music.load('sounds/music1.mp3')
        pygame.mixer.music.play(0,0)

        self.last_score = 0
        self.score = 0
        self.text = Text(f'Score: {self.score}', (20, 20))
        self.player = Player()

    def add_asteroid(self):
        now = time.time()
        delay = 2.5 - self.score/450 #increase difficulty
        if now - self.time >= delay:
            self.asteroids.append(Asteroid())
            self.time = time.time()

    def run(self):
        print('app launched')
        self.time = time.time()
        self.start = time.time()
        while self.running:
            self.add_asteroid()
            for event in pygame.event.get():
                self.do_event(event)
            self.update()
            self.draw()
            if self.game_over:
                time.sleep(3)
                self.running = False

        sys.exit()

    def do_event(self, event):
        if event.type == QUIT:
            self.running = False
        self.player.do_event(event)

    def update(self):
        self.check_collision()
        for ast in self.asteroids:
            if ast.rect.center[0] <= -50:
                del ast # for a faster programm
        for ast in self.asteroids:
            ast.update()
        self.player.update()
        t = time.time()
        score = t - self.start
        self.score = int(score*10)

    
    def draw(self):
        App.screen.blit(self.bg, (0, 0))

        self.player.draw()
        for ast in self.asteroids:
            ast.draw()

        if self.game_over:
            self.text.set(f'Game Over! Score: {self.last_score}')
        else:
            self.text.set(f'Score: {self.score}')
        
        self.text.draw()

        pygame.display.update()

    def check_collision(self): # the player rect is too wide, needs an update
        for ast in self.asteroids:
            if ast.rect.colliderect(self.player.rect):
                self.last_score = self.score
                self.game_over = True


if __name__ == '__main__':
    app = App()
    app.run()