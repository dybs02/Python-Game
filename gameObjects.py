import pygame, os, sys
import math
from random import randint

def get_path(*args):
    return os.path.join(os.path.dirname(__file__), *args)

def load_animation(flip = False, *path):
    image_list = []
    full_path = get_path(*path)

    for file in os.listdir(full_path):
        if file.endswith(".png"):
            image = pygame.image.load(os.path.join(full_path, file))
            if flip:
                image = pygame.transform.flip(image, True, False)
            image_list.append(image)

    return image_list


class Entity():
    Entities = []

    def __init__(self, game, pos):
        self.game = game
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.x, self.y = pos
        self.speed = 1
        self.rect.topleft = (self.x, self.y)
        self.facing = 1 # right
        Entity.Entities.append(self)

    def move_by(self, value):
        self.x += value[0] * self.speed
        self.y += value[1] * self.speed
        self.rect.topleft = (self.x, self.y)

    def move_to(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect.topleft = (self.x, self.y)

    @classmethod
    def drawAll(cls):
        for entity in Entity.Entities:
            entity.game.window.blit(entity.image, entity.rect)

class Player(Entity):

    def __init__(self, game, pos):
        Entity.__init__(self, game, pos)
        self.image_sets = [load_animation(True, 'images', 'playerRunning'), load_animation(False, 'images', 'playerRunning')]
        self.images = self.image_sets[self.facing]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.guns = [Gun(self.game, self, 20, 10, 2, 'gunShot.wav'), Gun(self.game, self, 8, 7, 1, 'machineGun.wav')]
        self.gun = self.guns[0]
        self.kills = 0

    def update(self):
        self.spawn_zombie()
        self.run()
        self.gun.update()

    def spawn_zombie(self):
        if Zombie.spawn_delay < 0:
            Zombie.spawn_delay = 30
            Zombie(self.game)
        Zombie.spawn_delay -= 1

    def run(self):
        previous_facing = self.facing
        player_move_value = [0, 0]

        if pygame.K_w in self.game.keys:
            player_move_value[1] -= 1
        if pygame.K_s in self.game.keys:
            player_move_value[1] += 1
        if pygame.K_a in self.game.keys:
            if self.facing == 1:
                self.facing = 0
            player_move_value[0] -= 1
        if pygame.K_d in self.game.keys:
            if self.facing == 0:
                self.facing = 1
            player_move_value[0] += 1
        if pygame.K_LSHIFT in self.game.keys:
            self.speed = 2
        else:
            self.speed = 1

        if previous_facing != self.facing:
            self.images = self.image_sets[self.facing]

        if player_move_value != [0, 0]:
            if 0 > self.x:
                player_move_value[0] = 1
            if self.x > self.game.map_rect[2] - self.rect[2]:
                player_move_value[0] = -1
            if 0 > self.y:
                player_move_value[1] = 1
            if self.y > self.game.map_rect[3] - self.rect[3]:
                player_move_value[1] = -1

            self.current_image += 0.05 * self.speed
            if self.current_image >= len(self.images):
                self.current_image = 0
            self.image = self.images[int(self.current_image)]
            self.move_by(player_move_value)

class Gun():
    bullets = []

    def __init__(self, game, player, delay, bullet_speed, damage, sound):
        self.game = game
        self.player = player
        self.delay_value = delay
        self.delay = delay
        self.bullet_speed = bullet_speed
        self.damage = damage
        self.sound = pygame.mixer.Sound(get_path('sounds', sound))

    def update(self):
        if pygame.K_1 in self.game.keys:
            self.player.gun = self.player.guns[0]
        if pygame.K_2 in self.game.keys:
            self.player.gun = self.player.guns[1]
        self.shoot()
        Bullet.update()

    def shoot(self):
        if self.game.mouse_buttons[0]:
            if self.delay < 0:
                pygame.mixer.Channel(1).play(self.sound)
                Bullet(self.game, (self.player.x, self.player.y), self.game.mouse_pos, self.bullet_speed, self.damage)
                self.delay = self.delay_value
        self.delay -= 1

class Bullet():
    bullets = []
    image = pygame.image.load(get_path("images", "bullet.png"))

    def __init__(self, game, pos, m_pos, speed, damage):
        self.game = game
        self.rect = self.image.get_rect()
        self.x, self.y = pos
        self.rect.topleft = (self.x, self.y)
        dy, dx = pos[1]-m_pos[1], m_pos[0]-pos[0]
        r = math.hypot(dx, dy)
        self.x_speed = (dx/r) * speed
        self.y_speed = (dy/r) * speed
        self.damage = damage
        Bullet.bullets.append(self)

    @classmethod
    def reset(cls):
        Bullet.bullets.clear()

    @classmethod
    def update(cls):
        for bullet in Bullet.bullets:

            bullet.x += bullet.x_speed
            bullet.y -= bullet.y_speed
            bullet.rect.topleft = (bullet.x, bullet.y)

            if  1500 < bullet.x or bullet.x < -10 or 1500 < bullet.y or bullet.y < -10:
                Bullet.bullets.remove(bullet)

        Zombie.update()
        Bullet.drawAll()

    @classmethod
    def drawAll(cls):
        for bullet in Bullet.bullets:
            bullet.game.window.blit(Bullet.image, bullet.rect)

class Zombie(Entity):
    spawns = ((240, 160), (240, 368), (784, 160), (784, 368))
    spawn_delay = 30
    zombies = []

    def __init__(self, game):
        pos = (randint(0, 720), randint(0, 720))
        Entity.__init__(self, game, pos)
        self.image_sets = [load_animation(True, 'images', 'zombieWalk'), load_animation(False, 'images', 'zombieWalk')]
        self.images = self.image_sets[self.facing]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.midbottom = Zombie.spawns[randint(0, 3)]
        self.x, self.y = self.rect.topleft
        self.hp = 2
        Zombie.zombies.append(self)

    @classmethod
    def reset(cls):
        for z in Zombie.zombies:
            Entity.Entities.remove(z)
        Zombie.zombies.clear()


    @classmethod
    def update(cls):
        for z in Zombie.zombies:
            for b in Bullet.bullets:
                if z.rect.colliderect(b.rect):
                    z.hp -= b.damage
                    if z.hp <= 0:
                        Zombie.zombies.remove(z)
                        Entity.Entities.remove(z)
                        z.game.player.kills += 1
                    Bullet.bullets.remove(b)

        cls.move()

    @classmethod
    def move(cls):
        for z in Zombie.zombies:
            if z.rect.colliderect(z.game.player.rect):
                z.game.lost = True
                return

            dy, dx = z.game.player.y-z.y, z.game.player.x-z.x
            r = math.hypot(dx, dy)
            value = ((dx/r), (dy/r))

            if value[0] < 0:
                z.facing = 0
            else:
                z.facing = 1

            z.images = z.image_sets[z.facing]
            z.current_image += 0.05 * z.speed
            if z.current_image >= len(z.images):
                z.current_image = 0
            z.image = z.images[int(z.current_image)]

            z.move_by(value)
