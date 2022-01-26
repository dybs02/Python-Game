import pygame, sys

class Menu:

    def __init__(self, game):
        self.game = game
        self.show = True
        self.mid_x, self.mid_y = self.game.WINDOW_SIZE[0] / 2, self.game.WINDOW_SIZE[1] / 2

    def draw(self):
        self.game.window.blit(self.game.window, (0, 0))
        pygame.display.flip()

class MainMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        self.choice = 0
        self.options = ['Start Game', 'Options', 'Credits', 'Quit']

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show = False
                    # self.game.playing = True
                if event.key == pygame.K_UP:
                    if self.choice == 0:
                        self.choice = len(self.options)-1
                    else:
                        self.choice -= 1
                if event.key == pygame.K_DOWN:
                    if self.choice == len(self.options)-1:
                        self.choice = 0
                    else:
                        self.choice += 1
                if event.key == pygame.K_RETURN:
                    if self.choice == 3:
                        sys.exit()
                    self.game.menu = self.game.menu_list[self.choice]
                    self.show = False

    def display_menu(self):
        self.show = True

        while self.show:
            self.check_events()

            self.game.window.fill((50, 50, 50))
            self.game.draw_text('Main Menu', 40, (self.mid_x, self.mid_y - 100), (50, 50, 255))

            offset = -50
            for i, option in enumerate(self.options):
                color = (255, 0, 0) if i == self.choice else (255, 255, 255)

                self.game.draw_text(option, 20, (self.mid_x, self.mid_y + offset), color)
                offset += 30

            self.draw()

class CreditsMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show = False
                    self.game.menu = self.game.menu_list[0]

    def display_menu(self):
        self.show = True

        while self.show:
            self.check_events()
            self.game.window.fill((50, 50, 50))

            self.game.draw_text('Game made by', 40, (self.mid_x, self.mid_y - 100), (50, 50, 255))
            self.game.draw_text('Mateusz Dybala', 20, (self.mid_x, self.mid_y - 50), (250, 250, 255))

            self.draw()

class OptionsMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show = False
                    self.game.menu = self.game.menu_list[0]

    def display_menu(self):
        self.show = True

        while self.show:
            self.check_events()
            self.game.window.fill((50, 50, 50))

            self.game.draw_text('Options', 40, (self.mid_x, self.mid_y - 100), (255, 255, 255))
            self.game.draw_text('Volume: =====--------', 20, (self.mid_x, self.mid_y - 50), (50, 255, 50))

            self.draw()