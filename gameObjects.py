"""
Classes for different entities.

Used to create and update entity objects in game.
Contains functions for getting path to specified file
and for loading animations from files.
"""
import pygame
import os
import math
from random import randint


def get_path(*args):
    """
    Returns path to specified file.
    """
    return os.path.join(os.path.dirname(__file__), *args)


def load_animation(flip=False, *path):
    """
    Loads mulitples images from specified path.
    Returns list of loaded images

    Parameters
    ----------
    flip = bool (flips images horizontally)
    """
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
    """
    Base class for other classes
    to inherit from.
    """
    Entities = []

    def __init__(self, game, pos):
        """
        Initializes entity object.

        Parameters
        ----------
        game : Game()
        pos : (int, int)
        """
        self.game = game
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.x, self.y = pos
        self.speed = 1
        self.rect.topleft = (self.x, self.y)
        self.facing = 1  # right
        Entity.Entities.append(self)

    def move_by(self, value):
        """
        Changes entity position
        by given value.

        Parameters
        ----------
        value : (int, int)
        """
        self.x += value[0] * self.speed
        self.y += value[1] * self.speed
        self.rect.topleft = (self.x, self.y)

    def move_to(self, pos):
        """
        Changes entity position
        to new given position.

        Parameters
        ----------
        pos : (int, int)
        """
        self.x = pos[0]
        self.y = pos[1]
        self.rect.topleft = (self.x, self.y)

    @classmethod
    def drawAll(cls):
        """
        Draws all entities to game window.
        """
        for entity in Entity.Entities:
            entity.game.window.blit(entity.image, entity.rect)


class Player(Entity):
    """
    Used to create player object.
    Inherits from Entity class.
    """
    def __init__(self, game, pos):
        """
        Initializes player object.

        Parameters
        ----------
        game : Game()
        pos : (int, int)
        """
        Entity.__init__(self, game, pos)
        self.image_sets = [load_animation(True, 'images', 'playerRunning'),
                           load_animation(False, 'images', 'playerRunning')]
        self.images = self.image_sets[self.facing]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.guns = [Gun(self.game, self, 20, 10, 2, 'gunShot.wav'),
                     Gun(self.game, self, 8, 7, 1, 'machineGun.wav')]
        self.gun = self.guns[0]
        self.kills = 0

    def update(self):
        """
        Updates player position,
        gun object and spawns zombies.
        """
        self.spawn_zombie()
        self.run()
        self.gun.update()

    def spawn_zombie(self):
        """
        Spawns new zombie every 30 frames.
        """
        if Zombie.spawn_delay < 0:
            Zombie.spawn_delay = 30
            Zombie(self.game)
        Zombie.spawn_delay -= 1

    def run(self):
        """
        Handles control and logic
        behind moving player.
        """
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
    """
    Used to create gun object.
    """
    bullets = []

    def __init__(self, game, player, delay, bullet_speed, damage, sound):
        """
        Initializes gun object.

        Parameters
        ----------
        game : Game()
        player : Player()
        delay : int
        bullet_speed : int
        damage : int
        sound : str (file name)
        """
        self.game = game
        self.player = player
        self.delay_value = delay
        self.delay = delay
        self.bullet_speed = bullet_speed
        self.damage = damage
        self.sound = pygame.mixer.Sound(get_path('sounds', sound))

    def update(self):
        """
        Changes current weapon,
        shoots and updates bullets.
        """
        if pygame.K_1 in self.game.keys:
            self.player.gun = self.player.guns[0]
        if pygame.K_2 in self.game.keys:
            self.player.gun = self.player.guns[1]
        self.shoot()
        Bullet.update()

    def shoot(self):
        """
        Creates Bullet object relative to
        current delay and plays gun sound.
        """
        if self.game.mouse_buttons[0]:
            if self.delay < 0:
                pygame.mixer.Channel(1).play(self.sound)
                Bullet(self.game, self.player.rect.center,
                       self.game.mouse_pos, self.bullet_speed, self.damage)
                self.delay = self.delay_value
        self.delay -= 1


class Bullet():
    """
    Used to create bullet object.
    """
    bullets = []
    image = pygame.image.load(get_path("images", "bullet.png"))

    def __init__(self, game, pos, m_pos, speed, damage):
        """
        Initializes bullet object.

        Parameters
        ----------
        game : Game()
        pos : (int, int)
        m_pos : (int, int)
        speed : int
        damage : int
        """
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
        """
        Deletes all Bullet objects.
        """
        Bullet.bullets.clear()

    @classmethod
    def update(cls):
        """
        Updates position of bullets,
        deletes object if outside of the window.
        """
        for bullet in Bullet.bullets:

            bullet.x += bullet.x_speed
            bullet.y -= bullet.y_speed
            bullet.rect.topleft = (bullet.x, bullet.y)

            if 1500 < bullet.x or bullet.x < -10 or \
               1500 < bullet.y or bullet.y < -10:
                Bullet.bullets.remove(bullet)

        Zombie.update()
        Bullet.drawAll()

    @classmethod
    def drawAll(cls):
        """
        Draws all bullets to game window.
        """
        for bullet in Bullet.bullets:
            bullet.game.window.blit(Bullet.image, bullet.rect)


class Zombie(Entity):
    """
    Used to create zombie object.
    Inherits from Entity class.
    """
    spawns = ((240, 160), (240, 368), (784, 160), (784, 368))
    spawn_delay = 30
    zombies = []

    def __init__(self, game):
        """
        Initializes zombie object.

        Parameters
        ----------
        game : Game()
        """
        pos = (randint(0, 720), randint(0, 720))
        Entity.__init__(self, game, pos)
        self.image_sets = [load_animation(True, 'images', 'zombieWalk'),
                           load_animation(False, 'images', 'zombieWalk')]
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
        """
        Deletes all Zombie objects.
        """
        for z in Zombie.zombies:
            Entity.Entities.remove(z)
        Zombie.zombies.clear()

    @classmethod
    def update(cls):
        """
        Checks for collision with bullet,
        reduces HP and deletes the bullet.
        Moves every zombie.
        """
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
        """
        Changes position of every zombie
        relative to player position.
        """
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
