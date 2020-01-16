import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates
from game import Spacegame
import math
import random
from pygame import mixer

BLACK = (0, 0, 0,)
RED = (255, 0, 0,)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

img =pygame.image.load("images/spacebackground.jpg")
imgrect = img.get_rect()

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            bg_rgb (background colour) - tuple (r, g, b)
            text_rgb (text colour) - tuple (r, g, b)
            action - the gamestate change associated with this button
        """
        self.mouse_over = False

        default_image = create_surface_with_text(text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb)

        highlighted_image = create_surface_with_text(text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb)

        self.images = [default_image, highlighted_image]

        self.rects = [default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ Updates the mouse_over variable and returns the button's
            action value when clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)


class Player:
    """ Stores information about a player """

    def __init__(self, score=0, lives=3, current_level=1):
        self.score = score
        self.lives = lives
        self.current_level = current_level


def main():
    pygame.init()
    # mixer.music.load("sounds/background1.wav")
    # mixer.music.play(-1)

    screen = pygame.display.set_mode((700, 600))
    game_state = GameState.TITLE

    while True:       
        if game_state == GameState.TITLE:

            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = play_level(screen, player)

        if game_state == GameState.NEXT_LEVEL:
            player.current_level == 1
            game_state = play_level(screen, player)
            mixer.music.pause()
            Spacegame()
            mixer.music.load("sounds/background1.wav")
            mixer.music.play(-1)
            game_state = play_level(screen, player)

            
        if game_state == GameState.QUIT:
            pygame.quit()
            return

def title_screen(screen):
    title_btn = UIElement(center_position=(350, 250),
        font_size=50,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Earth invaders")
    start_btn = UIElement(center_position=(350, 350),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,)
    quit_btn = UIElement(
        center_position=(350, 450),
        font_size=30,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,)

    buttons = RenderUpdates(title_btn, start_btn, quit_btn)

    return game_loop(screen, buttons)


def play_level(screen, player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,)

    nextlevel_btn = UIElement(
        center_position=(350, 300),
        font_size=50,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="New Game",
        action=GameState.NEXT_LEVEL,)
    
    quit_btn = UIElement(
        center_position=(540, 570),
        font_size=20,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,)
    
    info_btn = UIElement(
        center_position=(350, 350),
        font_size=20,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        text="(double click to start)")
    buttons = RenderUpdates(quit_btn, return_btn, info_btn, nextlevel_btn)

    return game_loop(screen, buttons)


def game_loop(screen, buttons):
    """ Handles game loop until an action is return by a button in the
        buttons sprite renderer.
    """
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
                
        screen.fill(BLACK)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
        screen.blit(img, imgrect)
        buttons.draw(screen)
        pygame.display.flip()


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    NEXT_LEVEL = 2


if __name__ == "__main__":
    main()