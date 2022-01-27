import pygame
import sys
from menu import *
from gameObjects import *

class Game():
    WINDOW_SIZE = (720, 720)
    FONT_NAME = pygame.font.get_default_font()

    def __init__(self):
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        self.playing = False
        self.keys = []
        self.mouse_buttons = [None, None, None, None, None]
        self.mouse_pos = (0, 0)
        self.window = pygame.display.set_mode(Game.WINDOW_SIZE)
        self.menu_list = [MainMenu(self), OptionsMenu(self), CreditsMenu(self)]
        self.menu = self.menu_list[0]
        self.player = Player(self, (360, 360))

    def game_loop(self):
        self.fpsClock.tick(120)
        self.check_events()

        if not self.playing:
            self.menu.display_menu()
        else:
            self.check_controls()

            self.player.update()

            self.window.fill((50, 150, 50))
            Entity.drawAll()
            pygame.display.flip()

    def check_controls(self):
        if pygame.K_ESCAPE in self.keys:
            self.playing = False
            self.keys.remove(pygame.K_ESCAPE)

    def check_events(self):
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

    def draw_text(self, text : str, size : int, position : tuple[int, int], color : tuple[int, int, int] = (255, 255, 255)):
        font = pygame.font.Font(Game.FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = position
        self.window.blit(text_surface,text_rect)
