"""
This is a game with a space theme (doc_string).
It uses object-oriented programming.

To play the game use the arrows to move around.
keep your distance from the asteroids, if you touch them you die.
You need to collect the stars to increase your score.
To restart the game, click on any key at the end of a play.
You can toggle Fullscreen mode whit escape.

Creative Commons Attribution license
Icons:  https://www.flaticon.com/free-icon/ufo_214358
        https://www.flaticon.com/free-icon/star_616655
        https://www.flaticon.com/free-icon/asteroid_433924
Music:  https://patrickdearteaga.com/arcade-music/
"""

import pygame
import sys
import random
from pygame.locals import *


class Player:
    """The player can be moved, he need to collect the stars and avoid the asteroids."""
    
    def __init__(self):
        print('create player')
        self.x = 100
        self.y = 100
        self.speed_x = 0
        self.speed_y = 0
        self.up = 0  # these 4 variable allows the player to have inertia and to use multiple arrow at the same time
        self.down = 0
        self.right = 0
        self.left = 0
        self.player = pygame.image.load('images/ship.png')
        self.player = pygame.transform.scale(self.player, (45, 45))
        
    def do_event(self, event):
        if event.type == KEYDOWN:  # look which key are currently being pressed
            if event.key == K_UP or event.key == K_w:
                self.up = 0.45

            elif event.key == K_DOWN or event.key == K_s:
                self.down = 0.45

            elif event.key == K_LEFT or event.key == K_a:
                self.left = 0.45

            elif event.key == K_RIGHT or event.key == K_d:
                self.right = 0.45

        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_w:
                self.up = 0

            elif event.key == K_DOWN or event.key == K_s:
                self.down = 0

            elif event.key == K_LEFT or event.key == K_a:
                self.left = 0

            elif event.key == K_RIGHT or event.key == K_d:
                self.right = 0

    def update(self):
        self.speed_x += self.right - self.left  # do the movement for the player
        self.speed_y += self.down - self.up
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x > 555:  # don't allow the player to exit the screen
            self.x = 555
        if self.x < 0:
            self.x = 0
        if self.y > 355:
            self.y = 355
        if self.y < 0:
            self.y = 0

        if self.speed_x > 5:  # don't allow the player to go to fast
            self.speed_x = 5
        if self.speed_x < -5:
            self.speed_x = -5
        if self.speed_y > 5:
            self.speed_y = 5
        if self.speed_y < -5:
            self.speed_y = -5

        if self.speed_x > 0.1:  # slow the player down
            self.speed_x -= 0.15
        if self.speed_x < -0.1:
            self.speed_x += 0.15
        if self.speed_y > 0.1:
            self.speed_y -= 0.15
        if self.speed_y < -0.1:
            self.speed_y += 0.15
        
        if -0.1 < self.speed_x < 0.1:  # ajust the speed to zero (there was a bug)
            self.speed_x = 0
        if -0.1 < self.speed_y < 0.1:
            self.speed_y = 0
    
    def draw(self):
        App.screen.blit(self.player, (self.x, self.y))

    def collision(self, star_x, star_y):  # detect the collision of the player whit the stars
        if self.x - 35 < star_x < self.x + 45:
            if self.y - 35 < star_y < self.y + 45:
                return True

    
class Asteroids:
    """The player must avoid the asteroids, when he touch them the game end."""
    
    def __init__(self, player_x, player_y):
        print('create an asteroid')
        create = True
        while create:  # avoid the asteroids to be created on the player
            self.x = random.randint(5, App.width - 40)
            self.y = random.randint(5, App.height - 40)
            if self.x - 120 < player_x < self.x + 110:
                if self.y - 120 < player_y < self.y + 110:
                    create = True
            else:
                create = False
        self.asteroid = pygame.image.load('images/asteroid.png')
        self.asteroid = pygame.transform.scale(self.asteroid, (35, 35))
        self.speed_x = random.randint(1, 3)  # give a random speed to the asteroids
        self.speed_y = random.randint(1, 3)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x < 1:  # make the asteroid bounce one the edge on the screen
            self.speed_x = -self.speed_x
        if self.x > 564:
            self.speed_x = -self.speed_x
        if self.y < 1:
            self.speed_y = -self.speed_y
        if self.y > 364:
            self.speed_y = -self.speed_y
    
    def draw(self):
        App.screen.blit(self.asteroid, (self.x, self.y))

    def collision(self, player_x, player_y):  # detect the collision of asteroids whit the player
        if self.x - 40 < player_x < self.x + 30:
            if self.y - 40 < player_y < self.y + 30:
                return True


class Stars:
    """The player need to collect the stars to increase his score."""

    def __init__(self):
        print('create a star')
        self.x = random.randint(0, App.width - 35)
        self.y = random.randint(0, App.height - 35)
        self.star = pygame.image.load('images/star.png')
        self.star = pygame.transform.scale(self.star, (35, 35))

    def draw(self):
        App.screen.blit(self.star, (self.x, self.y))


class Text:
    """Create a text object to show the score."""

    def __init__(self, text, pos):
        self.font = pygame.font.SysFont(None, 32)
        self.rect = Rect(pos, (0, 0))
        self.set(text)

    def set(self, text):
        self.text = text
        self.img = self.font.render(self.text, True, Color('white'))
        self.rect.size = self.img.get_size()

    def draw(self):
        App.screen.blit(self.img, self.rect)


class App:
    """Create the main application that run the game"""

    width = 600
    height = 400
    screen = None  # this allows to use the class variable App.screen from everywhere
    caption = 'Space Game'
    
    def __init__(self):
        print('start the game')
        pygame.init()
        App.screen = pygame.display.set_mode((App.width, App.height))
        pygame.display.set_caption(App.caption)

        self.fullscreen = False
        self.background = pygame.image.load('images/space.jpg')

        self.sound = pygame.mixer.Sound('sounds/Interplanetary Odyssey.ogg')
        self.sound.set_volume(0.1)
        self.sound.play(-1)

        self.player = Player()
        self.score = 0
        self.text = Text(f'Stars : {self.score}', (260, 10))
  
        self.asteroids = []
        self.asteroids.append(Asteroids(self.player.x, self.player.y))

        self.star = Stars()
  
        self.running = True
        self.replay = False
        
    def run(self):
        print('run game')
        timer = pygame.time.Clock()  # timer to define the speed of the game
        while self.running:
            for event in pygame.event.get():
                self.do_event(event)

            self.collision()
            self.update()
            self.draw()
            timer.tick(60)
            
        pygame.quit()
        sys.exit()

    def do_event(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN:  # to toggle on and of the Fullscreen mode
            if event.key == K_ESCAPE:
                if self.fullscreen:
                    App.screen = pygame.display.set_mode((App.width, App.height))
                    self.fullscreen = False
                else:
                    App.screen = pygame.display.set_mode((App.width, App.height), pygame.FULLSCREEN)
                    self.fullscreen = True
            
        self.player.do_event(event)

    def collision(self):  # what the game need to do when a collision occur
        col = self.player.collision(self.star.x, self.star.y)
        if col:
            self.star = Stars()
            self.score += 1
            self.asteroids.append(Asteroids(self.player.x, self.player.y))
        for i in self.asteroids:
            col = i.collision(self.player.x, self.player.y)
            if col:
                self.replay = True  # end of the game

    def update(self):  # update the position of all moving object
        self.player.update()
        for stone in self.asteroids:
            stone.update()
            
    def draw(self):  # draw everything on the screen
        App.screen.blit(self.background, (0, 0))

        for i in self.asteroids:
            i.draw()
        self.star.draw()
        self.player.draw()

        if not self.replay:
            self.text.set(f'Stars : {self.score}')
            self.text.draw()

        if self.replay:
            self.text = Text(f'You lose, your score was : {self.score}', (150, 160))  # show your score
            self.text.draw()
            pygame.display.update()
            while self.replay:  # ask if you want to play again
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        self.sound.stop()
                        app = App()
                        app.run()
                    if event.type == QUIT:
                        self.replay = False
                        self.running = False

        pygame.display.update()


if __name__ == '__main__':
    app = App()
    app.run()
