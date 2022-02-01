"""
Game class.

Allows creation of game object.
"""
import pygame
import sys
from menu import *
from gameObjects import *


class Game():
    """
    Allows creation of game object.

    Contains functions for running main loop,
    updating in-game objects.
    """
    WINDOW_SIZE = (1024, 512)
    FONT_NAME = 'font.ttf'

    def __init__(self):
        """
        Initializes game object.
        """
        pygame.init()
        pygame.mixer.init()
        self.music = pygame.mixer.Sound(get_path('sounds', 'music.wav'))
        self.lost_sound = pygame.mixer.Sound(get_path('sounds', 'lost.wav'))
        self.music.set_volume(0.5)
        pygame.mixer.Channel(0).play(self.music, -1)
        pygame.mixer.Channel(0).pause()
        self.fpsClock = pygame.time.Clock()
        self.playing = False
        self.lost = False
        self.keys = []
        self.mouse_buttons = [None, None, None, None, None]
        self.mouse_pos = (0, 0)
        self.window = pygame.display.set_mode(Game.WINDOW_SIZE)
        self.map = pygame.image.load(get_path('images', 'map.jpg'))
        self.map_rect = self.map.get_rect()
        self.menu_list = [MainMenu(self), HelpMenu(self),
                          CreditsMenu(self), DeathScreen(self)]
        self.menu = self.menu_list[0]
        self.player = Player(self, (360, 360))

    def game_loop(self):
        """
        Function for running game, starts the main loop.
        """
        self.fpsClock.tick(120)
        self.check_events()

        if not self.playing:
            pygame.mixer.Channel(0).pause()
            self.menu.display_menu()
        else:
            pygame.mixer.Channel(0).unpause()
            self.check_controls()
            self.window.blit(self.map, self.map_rect)

            self.player.update()
            Entity.drawAll()
            pygame.display.flip()

            if self.lost:
                pygame.mixer.Channel(0).pause()
                pygame.mixer.Channel(3).play(self.lost_sound)
                self.menu = self.menu_list[3]
                self.playing = False

    def check_controls(self):
        """
        Checks if ESC is pressed,
        switches between game and menu.
        """
        if pygame.K_ESCAPE in self.keys:
            self.playing = False
            self.keys.remove(pygame.K_ESCAPE)

    def check_events(self):
        """
        Registers pressed keys,
        mouse buttons and mouse position.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.keys.append(event.key)
            if event.type == pygame.KEYUP:
                if event.key in self.keys:
                    self.keys.remove(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button <= 5:
                    self.mouse_buttons[event.button - 1] = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button <= 5:
                    self.mouse_buttons[event.button - 1] = None
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

    def draw_text(self, text: str, size: int, position: tuple[int, int],
                  color: tuple[int, int, int] = (255, 255, 255)):
        """
        Draws text to the game window.

        Parameters
        ----------
        text : str
        size : int
        position : (int, int)
        color : (int, int, int) = (255, 255, 255)
        """
        font = pygame.font.Font(Game.FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = position
        self.window.blit(text_surface, text_rect)

    def reset(self):
        """
        Sets game variables to default.
        """
        self.lost = False
        self.playing = False
        self.keys.clear()
        self.mouse_buttons = [None, None, None, None, None]
        Zombie.reset()
        Bullet.reset()
        self.player.__init__(self, (360, 360))
        self.menu = self.menu_list[0]
        self.menu.options[0] = 'Start Game'
