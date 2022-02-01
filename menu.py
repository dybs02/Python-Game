"""
Menu classes.

Used to create different menu screens in game.
"""
import pygame
import sys


class Menu:
    """
    Base class for other menu classes
    to inherit from.
    """
    def __init__(self, game):
        """
        Initializes menu object.

        Parameters
        ----------
        game : Game()
        """
        self.game = game
        self.show = True
        self.mid_x = self.game.WINDOW_SIZE[0] / 2
        self.mid_y = self.game.WINDOW_SIZE[1] / 2

    def draw(self):
        """
        Draws menu to the game window.
        """
        self.game.window.blit(self.game.window, (0, 0))
        pygame.display.flip()


class MainMenu(Menu):
    """
    Used to create main menu object.
    Inherits from menu class.
    """
    def __init__(self, game):
        """
        Initializes main menu object.

        Parameters
        ----------
        game : Game()
        """
        Menu.__init__(self, game)
        self.choice = 0
        self.options = ['Start Game', 'Help', 'Credits', 'Quit']

    def check_events(self):
        """
        Handles controls in while
        main menu is displayed.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show = False
                if event.key in [pygame.K_UP, pygame.K_w]:
                    if self.choice == 0:
                        self.choice = len(self.options)-1
                    else:
                        self.choice -= 1
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    if self.choice == len(self.options)-1:
                        self.choice = 0
                    else:
                        self.choice += 1
                if event.key == pygame.K_RETURN:
                    if self.choice == 0:
                        self.options[0] = 'Resume'
                        self.show = False
                        self.game.playing = True
                    if self.choice == 3:
                        sys.exit()
                    self.game.menu = self.game.menu_list[self.choice]
                    self.show = False

    def display_menu(self):
        """
        Displays main menu
        using menu loop.
        """
        self.show = True

        while self.show:
            self.check_events()

            self.game.window.fill((50, 50, 50))
            self.game.draw_text('Main Menu', 40,
                                (self.mid_x, self.mid_y - 100), (50, 50, 255))

            offset = -50
            for i, option in enumerate(self.options):
                color = (255, 0, 0) if i == self.choice else (255, 255, 255)

                self.game.draw_text(option, 20,
                                    (self.mid_x, self.mid_y + offset), color)
                offset += 30

            self.draw()


class CreditsMenu(Menu):
    """
    Used to create credits menu object.
    Inherits from menu class.
    """
    def __init__(self, game):
        """
        Initializes credits menu object.

        Parameters
        ----------
        game : Game()
        """
        Menu.__init__(self, game)

    def check_events(self):
        """
        Handles controls in while
        credits menu is displayed.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show = False
                    self.game.menu = self.game.menu_list[0]

    def display_menu(self):
        """
        Displays credits menu
        using menu loop.
        """
        self.show = True

        while self.show:
            self.check_events()
            self.game.window.fill((50, 50, 50))

            self.game.draw_text('Credits', 40,
                                (self.mid_x, self.mid_y - 100), (50, 50, 255))
            self.game.draw_text('Made by: Mateusz Dybala', 20,
                                (self.mid_x, self.mid_y - 50), (250, 250, 255))
            self.game.draw_text('Art by: RgsDev', 20,
                                (self.mid_x, self.mid_y - 20), (250, 250, 255))
            self.game.draw_text('Sound from: freesound.org', 20,
                                (self.mid_x, self.mid_y + 10), (250, 250, 255))

            self.draw()


class HelpMenu(Menu):
    """
    Used to create help menu object.
    Inherits from menu class.
    """
    def __init__(self, game):
        """
        Initializes help menu object.

        Parameters
        ----------
        game : Game()
        """
        Menu.__init__(self, game)

    def check_events(self):
        """
        Handles controls in while
        help menu is displayed.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show = False
                    self.game.menu = self.game.menu_list[0]

    def display_menu(self):
        """
        Displays help menu
        using menu loop.
        """
        self.show = True

        while self.show:
            self.check_events()
            self.game.window.fill((50, 50, 50))

            self.game.draw_text('Help', 40, (self.mid_x, self.mid_y - 100),
                                (50, 255, 50))
            self.game.draw_text('Kill as many zombies as you can', 20,
                                (self.mid_x, self.mid_y - 50))
            self.game.draw_text('Switch between weapon using 1 & 2 keys', 20,
                                (self.mid_x, self.mid_y - 20))
            self.game.draw_text('Press ESC to pause game', 20,
                                (self.mid_x, self.mid_y + 10))

            self.draw()


class DeathScreen(Menu):
    """
    Used to create death screen object.
    Inherits from menu class.
    """
    def __init__(self, game):
        Menu.__init__(self, game)

    def check_events(self):
        """
        Handles controls in while
        death screen is displayed.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.reset()
                    self.show = False

    def display_menu(self):
        """
        Displays death screen
        using menu loop.
        """
        self.show = True

        while self.show:
            self.check_events()

            self.game.draw_text('You Lost !', 40,
                                (self.mid_x, self.mid_y - 100), (255, 0, 0))
            self.game.draw_text(f'Score: {self.game.player.kills} kills',
                                30, (self.mid_x, self.mid_y), (150, 0, 0))

            self.draw()
