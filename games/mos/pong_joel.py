"""
This is a game with a space theme (doc_string).
It uses object-oriented programming.
It's a Pong BO11
"""

import pygame
import sys
import random
from pygame.locals import *
        

class Player:
    
    def __init__(self, x, y):
        print('create player object')
        self.score = 0
        self.x = x
        self.y = y
        self.w = 15
        self.h = 150
        self.dy = 0
        self.color = Color('red')
        
    """The player can move"""
    def do_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_d:
                self.dy = 4
            elif event.key == K_a:
                self.dy = -4


    """The player cannot move outside the field"""
    def update(self):
        self.y += self.dy
        if self.y < 0:
            self.dy = 0
            self.y = 0
        
        if self.y > App.height-self.h:
            self.dy = 0
            self.y = 250
        
        
    """Creating the players shape"""
    def draw(self):
        pygame.draw.rect(App.screen, self.color, Rect(self.x, self.y, self.w, self.h))
        
        
class Player1(Player):
    def __init__(self):
        super().__init__(0, 200)
        
        
class Player2(Player):
    def __init__(self):
        super().__init__(585, 100)
        
    def do_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.dy = 4
            elif event.key == K_RIGHT:
                self.dy = -4

    
class Ball:
    """The ball must know the 2 players in order to calculate the collision."""
    def __init__(self, player1, player2): 
        print('create ball object')
        self.p1 = player1
        self.p2 = player2
        self.w = 30
        self.h = 30
        self.color = Color('blue')
        self.reset()
        
        
        """Reset the ball in his initial position"""
    def reset(self):
        self.x = 300
        self.y = 200
        self.dx = 3
        self.dy = 3
        
        
        """Stop the game when one player has 5 points """
        if self.p1.score > 4:
            print("player 1 has won")
            self.dx = 0
            self.dy = 0
        
        if self.p2.score > 4:
            print("player 2 has won")
            self.dx = 0
            self.dy = 0
        
        
        """Interaction between the ball and the player """
        """If the ball hits the player, it bounces away, if the ball doesnt hit the player it inceases the score"""
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
        if self.x < 15:
            if not (self.p1.y < self.y < self.p1.y+self.p1.h):
                self.p2.score += 1
                self.reset()
            else:
                self.dx = -self.dx
                
        if self.x > 555:
            if not (self.p2.y < self.y < self.p2.y+self.p2.h):
                self.p1.score += 1
                self.reset()
            else:
                self.dx = -self.dx
                
        if not (0 < self.y < App.height-self.h):
            self.dy = -self.dy
            
    
    
    def draw(self):
        pygame.draw.rect(App.screen, self.color, Rect(self.x, self.y, self.w, self.h))
    
    
class Text:
    """Create a text object"""
    def __init__(self, text, pos):
        print('create text object')
        self.font = pygame.font.Font(None, 36)
        self.rect = Rect(pos, (0, 0))
        self.set(text)
    """Create setings for the text object.""" 
    def set(self, text):
        self.text = text
        self.img = self.font.render(self.text, True, Color('white'))
        self.rect.size = self.img.get_size()
        
    def draw(self):
        App.screen.blit(self.img, self.rect)
    
    
class App:
    width = 600
    height = 400
    caption = 'Space Pong'
    screen = None
    
    """Intitialize the app"""
    def __init__(self):
        print('initalize app')
        pygame.init()
        App.screen = pygame.display.set_mode((App.width, App.height))
        pygame.display.set_caption(App.caption)
        
##fond d'écran
##        self.img = pygame.image.load('images/space.jpg')
##        App.size = self.img.get_size()
##        App.screen = pygame.display.set_mode(App.size)

        self.player1 = Player1()
        self.player2 = Player2()

        self.text1 = Text(f'Points: {self.player1.score}', (20, 20))
        self.text2 = Text(f'Points: {self.player2.score}', (480, 20))
        
        self.ball = Ball(self.player1, self.player2)

        self.running = True
    
    
    """Runs the app"""        
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
            
        self.player1.do_event(event)
        self.player2.do_event(event)
            
    def update(self):
        self.player1.update()
        self.player2.update()
        self.ball.update()
        self.text1.set(f'Points: {self.player1.score}')
        self.text2.set(f'Points: {self.player2.score}')
            
    def draw(self):
        App.screen.fill(Color('black'))

        self.player1.draw()
        self.player2.draw()
        self.ball.draw()
        self.text1.draw()
        self.text2.draw()

        pygame.display.update()
        

"""Maintance the app running"""
if __name__ == '__main__':
    app = App()
    app.run()