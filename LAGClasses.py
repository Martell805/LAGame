import pygame
import sys
import os
from random import randint
from LAGDefs import *


pygame.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tile_images, *groupes):
        super().__init__(*groupes)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, v, player_image, *groups):
        super().__init__(groups)
        self.image = player_image
        self.clock = pygame.time.Clock()
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)
        self.mr = self.ml = self.md = self.mu = False
        self.v = v
        self.x = tile_width * pos_x + 10 - tile_width
        self.y = tile_height * pos_y + 10 - tile_height
        self.god = False

    def right(self):
        self.mr = not self.mr

    def left(self):
        self.ml = not self.ml

    def up(self):
        self.mu = not self.mu

    def down(self):
        self.md = not self.md

    def update(self, walls_group, gate_group):
        tick = self.clock.tick()

        can_move = True
        for wall in walls_group:
            can_move = can_move and (self.rect.x + 30 != wall.rect.x or self.rect.y
                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
        if self.mr and (can_move or self.god):
            self.x += self.v * tick / 1000

        can_move = True
        for wall in walls_group:
            can_move = can_move and (self.rect.x != wall.rect.x + tile_width or self.rect.y
                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
        if self.ml and (can_move or self.god):
            self.x -= self.v * tick / 1000

        can_move = True
        for wall in walls_group:
            can_move = can_move and (self.rect.y != wall.rect.y + tile_height or self.rect.x
                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
        if self.mu and (can_move or self.god):
            self.y -= self.v * tick / 1000

        can_move = True
        for wall in walls_group:
            can_move = can_move and (self.rect.y + 30 != wall.rect.y or self.rect.x
                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
        if self.md and (can_move or self.god):
            self.y += self.v * tick / 1000

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.sprite.spritecollideany(self, gate_group):
            return generate_level(load_level(f'levels/rand_lvl/{randint(1, 7)}.lvl'))
        else:
            return False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direct, f_or_e, bullet_image,  *groups):
        super().__init__(groups)
        self.image = bullet_image
        self.clock = pygame.time.Clock()
        self.friendly = f_or_e
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.dir = direct
        self.x = pos_x
        self.y = pos_y

    def update(self, walls_group, enemy_group, player_group):
        if pygame.sprite.spritecollideany(self, walls_group):
            self.dir = -1
        elif pygame.sprite.spritecollideany(self, player_group) and not self.friendly:
            self.dir = -1
            print('YOU DEAD')
            terminate()
        elif pygame.sprite.spritecollideany(self, enemy_group) and self.friendly:
            self.dir = -1
            for enemy in enemy_group:
                if pygame.sprite.spritecollideany(self, enemy):
                    enemy.kill()

        tick = self.clock.tick()
        if self.dir == 0:
            self.y -= 400 * tick / 1000
        elif self.dir == 1:
            self.x += 400 * tick / 1000
        elif self.dir == 2:
            self.y += 400 * tick / 1000
        elif self.dir == 3:
            self.x -= 400 * tick / 1000

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
