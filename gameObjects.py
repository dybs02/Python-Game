import pygame, os

class Entity():
    Entities = []

    def __init__(self, game, pos):
        self.game = game
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.x, self.y = pos
        self.speed = 1
        self.rect.topleft = (self.x, self.y)
        Entity.Entities.append(self)

    @classmethod
    def drawAll(cls):
        for entity in Entity.Entities:
            entity.game.window.blit(entity.image, entity.rect)

class Player(Entity):

    def __init__(self, game, pos):
        Entity.__init__(self, game, pos)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "images", "player.png"))
        self.rect = self.image.get_rect()

    def move_by(self, value):
        print(self.rect.topleft)
        self.x += value[0] * self.speed
        self.y += value[1] * self.speed
        self.rect.topleft = (self.x, self.y)

    def update(self):
        player_move_value = [0, 0]

        if pygame.K_w in self.game.keys:
            player_move_value[1] -= 1
        if pygame.K_s in self.game.keys:
            player_move_value[1] += 1
        if pygame.K_a in self.game.keys:
            player_move_value[0] -= 1
        if pygame.K_d in self.game.keys:
            player_move_value[0] += 1
        if pygame.K_LSHIFT in self.game.keys:
            self.speed = 2.5
        else:
            self.speed = 1

        self.move_by(player_move_value)
