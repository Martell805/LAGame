import os
import pygame
import sys
from random import randint, choice

FPS = 100


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    level_s = []
    try:
        level_s = [line.strip() for line in open(filename, 'r')]
    except Exception:
        print('Указанного уровня не существует.')
        print("Забота программы завершена.")
        terminate()

    max_width = max(map(len, level_s))
    level_s = list(map(lambda x: 'G' + x.ljust(max_width, '.') + 'G', level_s))
    max_width += 2
    level_s = ['G' * max_width] + level_s + ['G' * max_width]
    return level_s


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level_map):
    px, py = None, None
    all_sprites = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    gates_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    s_enemy_cords = []
    m_enemy_cords = []
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '.':
                Tile('empty', x, y, all_sprites)
            elif level_map[y][x] == '#':
                Tile('wall', x, y, all_sprites, walls_group)
            elif level_map[y][x] == '@':
                Tile('empty', x, y, all_sprites)
                px = x
                py = y
            elif level_map[y][x] == 'G':
                Tile('gate_c', x, y, all_sprites, gates_group)
            elif level_map[y][x] == 'S':
                Tile('empty', x, y, all_sprites)
                s_enemy_cords.append((x, y))
            elif level_map[y][x] == 'M':
                Tile('empty', x, y, all_sprites)
                m_enemy_cords.append((x, y))
    for x, y in s_enemy_cords:
        Enemy(x, y, 100, 'S', enemy_group, all_sprites)
    for x, y in m_enemy_cords:
        Enemy(x, y, 100, 'M', enemy_group, all_sprites)
    players_group = pygame.sprite.Group()
    s = {'player': Player(px, py, 100, players_group, all_sprites),
         'level': pygame.Surface((len(level_map[0]) * tile_width, len(level_map) * tile_height)),
         'walls': walls_group,
         'bullets': pygame.sprite.Group(),
         'enemy': enemy_group,
         'all': all_sprites,
         'players': players_group,
         'gates': gates_group,
         'particles': pygame.sprite.Group()}
    return s


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self, enemy_group):
        can_tp = True
        for _ in enemy_group:
            can_tp = False
            break

        if can_tp:
            self.image = tile_images['gate_o']


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, v, *groups):
        super().__init__(groups)
        self.shoot_rate = 300
        self.last_bullet = self.shoot_rate
        self.image = player_image
        self.clock = pygame.time.Clock()
        self.new = True
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)
        self.mr = self.ml = self.md = self.mu = False
        self.v = v
        self.x = tile_width * pos_x + 10
        self.y = tile_height * pos_y + 10
        self.god = False

    def right(self):
        self.mr = not self.mr

    def left(self):
        self.ml = not self.ml

    def up(self):
        self.mu = not self.mu

    def down(self):
        self.md = not self.md

    def update(self, walls_group, gate_group, enemy_group):
        tick = self.clock.tick()

        self.last_bullet -= 1
        if self.last_bullet < 0:
            self.last_bullet = 0

        can_tp = True
        for _ in enemy_group:
            can_tp = False
            break

        if pygame.sprite.spritecollideany(self, gate_group) and can_tp:
            loaded_levels.append(generate_level(load_level(f'levels/rand_lvl/{randint(1, 7)}.lvl')))

        if self.new:
            self.mr = False
            self.ml = False
            self.mu = False
            self.md = False
            self.new = False

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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, v, typ, *groups):
        super().__init__(groups)
        self.shoot_rate = 500
        self.type = typ
        self.last_bullet = self.shoot_rate
        if self.type == 'S':
            self.image = s_enemy_image
        elif self.type == 'M':
            self.image = m_enemy_image
        self.clock = pygame.time.Clock()
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)
        self.v = v
        self.x = tile_width * pos_x + 10
        self.y = tile_height * pos_y + 10
        self.flying = False

    def update(self, player_group, walls_group, particle_group, all_sprites):
        tick = self.clock.tick()

        self.last_bullet -= 1
        if self.last_bullet < 0:
            self.last_bullet = 0

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if self.type == 'S':
            self.ui_s(player_group, walls_group, particle_group, all_sprites, tick)
        elif self.type == 'M':
            self.ui_m(player_group, walls_group, particle_group, all_sprites, tick)

    def ui_s(self, player_group, walls_group, particle_group, all_sprites, tick):
        v = 75
        player_cords = None
        player = None
        for p in player_group:
            player = p
            player_cords = player.rect.x, player.rect.y
        if player_cords:

            dirs = [(player.rect.x, player.rect.y - 100),
                    (player.rect.x + 100, player.rect.y),
                    (player.rect.x, player.rect.y + 100),
                    (player.rect.x - 100, player.rect.y)]

            dir = dirs[min([(0, abs((self.rect.x ** 2 + self.rect.y ** 2) ** 0.5 -
                            (player.rect.x ** 2 + (player.rect.y - 100) ** 2) ** 0.5)),
                       (1, abs((self.rect.x ** 2 + self.rect.y ** 2) ** 0.5 -
                               ((player.rect.x + 100) ** 2 + player.rect.y ** 2) ** 0.5)),
                       (2, abs((self.rect.x ** 2 + self.rect.y ** 2) ** 0.5 -
                               (player.rect.x ** 2 + (player.rect.y + 100) ** 2) ** 0.5)),
                       (3, abs((self.rect.x ** 2 + self.rect.y ** 2) ** 0.5 -
                               ((player.rect.x - 100) ** 2 + player.rect.y ** 2) ** 0.5))],
                      key=lambda x: x[1])[0]]

            if abs((self.rect.x ** 2 + self.rect.y ** 2) ** 0.5 - (dir[0] ** 2 + dir[1] ** 2) ** 0.5) <= 250:
                if dir[0] < self.rect.x:
                    if dir[1] < self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x != wall.rect.x + tile_width or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x -= min(v * tick / 1000, abs(self.x - dir[0]))
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y != wall.rect.y + tile_height or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y -= min(v * tick / 1000, abs(self.y - dir[1]))
                    elif dir[1] == self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x != wall.rect.x + tile_width or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x -= min(v * tick / 1000, abs(self.x - dir[0]))
                    elif dir[1] > self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x != wall.rect.x + tile_width or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x -= min(v * tick / 1000, abs(self.x - dir[0]))
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y + 30 != wall.rect.y or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y += min(v * tick / 1000, abs(self.y - dir[1]))
                elif dir[0] == self.rect.x:
                    if dir[1] < self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y != wall.rect.y + tile_height or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y -= min(v * tick / 1000, abs(self.y - dir[1]))
                    elif dir[1] == self.rect.y:
                        pass
                    elif dir[1] > self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y + 30 != wall.rect.y or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y += min(v * tick / 1000, abs(self.y - dir[1]))
                elif dir[0] > self.rect.x:
                    if dir[1] < self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x + 30 != wall.rect.x or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x += min(v * tick / 1000, abs(self.x - dir[0]))
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y != wall.rect.y + tile_height or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y -= min(v * tick / 1000, abs(self.y - dir[1]))
                    elif dir[1] == self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x + 30 != wall.rect.x or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x += min(v * tick / 1000, abs(self.x - dir[0]))
                    elif dir[1] > self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x + 30 != wall.rect.x or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x += min(v * tick / 1000, abs(self.x - dir[0]))
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y + 30 != wall.rect.y or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y += min(v * tick / 1000, abs(self.y - dir[1]))

            if not self.last_bullet:
                if self.rect.x - 200 < player_cords[0] + 15 < self.rect.x and\
                        self.rect.y - 200 < player_cords[1] + 15 < self.rect.y:
                    if player.mr:
                        Bullet(self.rect.x + 10, self.rect.y + 10, 0, False,
                               loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                        self.last_bullet = self.shoot_rate
                    elif player.md:
                        Bullet(self.rect.x + 10, self.rect.y + 10, 3, False,
                               loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                        self.last_bullet = self.shoot_rate
                elif self.rect.x < player_cords[0] < self.rect.x + 30 and \
                        self.rect.y < player_cords[1] < self.rect.y + 200:
                    Bullet(self.rect.x + 10, self.rect.y + 10, 0, False,
                           loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                    self.last_bullet = self.shoot_rate
                elif self.rect.x + 30 < player_cords[0] + 15 < self.rect.x + 230 and\
                        self.rect.y - 200 < player_cords[1] + 15 < self.rect.y:
                    if player.ml:
                        Bullet(self.rect.x + 10, self.rect.y + 10, 0, False,
                               loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                        self.last_bullet = self.shoot_rate
                    elif player.md:
                        Bullet(self.rect.x + 10, self.rect.y + 10, 1, False,
                               loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                        self.last_bullet = self.shoot_rate
                elif self.rect.x + 30 < player_cords[0] < self.rect.x + 200 and \
                        self.rect.y < player_cords[1] - 15 < self.rect.y:
                    Bullet(self.rect.x + 10, self.rect.y + 10, 1, False,
                           loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                    self.last_bullet = self.shoot_rate
                elif self.rect.x + 30 < player_cords[0] + 15 < self.rect.x + 230 and\
                        self.rect.y + 20 < player_cords[1] + 15 < self.rect.y + 230:
                    if player.ml:
                        Bullet(self.rect.x + 10, self.rect.y + 10, 2, False,
                               loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                        self.last_bullet = self.shoot_rate
                    elif player.mu:
                        Bullet(self.rect.x + 10, self.rect.y + 10, 1, False,
                               loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                        self.last_bullet = self.shoot_rate
                elif self.rect.x < player_cords[0] + 15 < self.rect.x + 30 and \
                        self.rect.y < player_cords[1] < self.rect.y + 230:
                    Bullet(self.rect.x + 10, self.rect.y + 10, 2, False,
                           loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                    self.last_bullet = self.shoot_rate
                elif self.rect.x - 200 < player_cords[0] + 15 < self.rect.x and\
                        self.rect.y + 20 < player_cords[1] + 15 < self.rect.y + 230:
                    if player.mr:
                        Bullet(self.rect.x + 10, self.rect.y + 10, 2, False,
                               loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                        self.last_bullet = self.shoot_rate
                    elif player.mu:
                        Bullet(self.rect.x + 10, self.rect.y + 10, 3, False,
                               loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                        self.last_bullet = self.shoot_rate
                elif self.rect.x - 200 < player_cords[0] < self.rect.x + 30 and \
                        self.rect.y < player_cords[1] < self.rect.y + 30:
                    Bullet(self.rect.x + 10, self.rect.y + 10, 3, False,
                           loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                    self.last_bullet = self.shoot_rate
        else:
            self.x += randint(-100, 100) * tick / 1000
            self.y += randint(-100, 100) * tick / 1000

    def ui_m(self, player_group, walls_group, particle_group, all_sprites, tick):
        v = 100
        player_cords = None
        for p in player_group:
            player = p
            player_cords = player.rect.x, player.rect.y
        if player_cords:
            dir = player_cords

            if abs((self.rect.x ** 2 + self.rect.y ** 2) ** 0.5 - (dir[0] ** 2 + dir[1] ** 2) ** 0.5) <= 250:
                if dir[0] < self.rect.x:
                    if dir[1] < self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x != wall.rect.x + tile_width or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x -= min(v * tick / 1000, abs(self.x - dir[0]))
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y != wall.rect.y + tile_height or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y -= min(v * tick / 1000, abs(self.y - dir[1]))
                    elif dir[1] == self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x != wall.rect.x + tile_width or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x -= min(v * tick / 1000, abs(self.x - dir[0]))
                    elif dir[1] > self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x != wall.rect.x + tile_width or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x -= min(v * tick / 1000, abs(self.x - dir[0]))
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y + 30 != wall.rect.y or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y += min(v * tick / 1000, abs(self.y - dir[1]))
                elif dir[0] == self.rect.x:
                    if dir[1] < self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y != wall.rect.y + tile_height or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y -= min(v * tick / 1000, abs(self.y - dir[1]))
                    elif dir[1] == self.rect.y:
                        pass
                    elif dir[1] > self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y + 30 != wall.rect.y or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y += min(v * tick / 1000, abs(self.y - dir[1]))
                elif dir[0] > self.rect.x:
                    if dir[1] < self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x + 30 != wall.rect.x or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x += min(v * tick / 1000, abs(self.x - dir[0]))
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y != wall.rect.y + tile_height or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y -= min(v * tick / 1000, abs(self.y - dir[1]))
                    elif dir[1] == self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x + 30 != wall.rect.x or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x += min(v * tick / 1000, abs(self.x - dir[0]))
                    elif dir[1] > self.rect.y:
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.x + 30 != wall.rect.x or self.rect.y
                                                     not in range(wall.rect.y - 29, wall.rect.y + tile_height))
                        if can_move:
                            self.x += min(v * tick / 1000, abs(self.x - dir[0]))
                        can_move = True
                        for wall in walls_group:
                            can_move = can_move and (self.rect.y + 30 != wall.rect.y or self.rect.x
                                                     not in range(wall.rect.x - 29, wall.rect.x + tile_width))
                        if can_move:
                            self.y += min(v * tick / 1000, abs(self.y - dir[1]))
        else:
            self.x += randint(-100, 100) * tick / 1000
            self.y += randint(-100, 100) * tick / 1000

        s = pygame.sprite.spritecollide(self, player_group, True)
        if s:
            for q in s:
                for _ in range(100):
                    Particle((q.rect.x + 15, q.rect.y + 15), particle_group, all_sprites)
            print('YOU DEAD')


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direct, f_or_e, *groups):
        super().__init__(groups)
        if f_or_e:
            self.image = f_bullet_image
        else:
            self.image = e_bullet_image
        self.clock = pygame.time.Clock()
        self.friendly = f_or_e
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.dir = direct
        self.x = pos_x
        self.y = pos_y

    def update(self, walls_group, enemy_group, player_group, particle_group, all_sprites):
        if pygame.sprite.spritecollideany(self, walls_group):
            self.dir = -1
        elif pygame.sprite.spritecollideany(self, player_group) and not self.friendly:
            s = pygame.sprite.spritecollide(self, player_group, True)
            if s:
                self.kill()
                for q in s:
                    for _ in range(100):
                        Particle((q.rect.x + 15, q.rect.y + 15), particle_group, all_sprites)
            print('YOU DEAD')
        elif pygame.sprite.spritecollideany(self, enemy_group) and self.friendly:
            s = pygame.sprite.spritecollide(self, enemy_group, False)
            if s:
                self.kill()
                for q in s:
                    q.kill()
                    for _ in range(randint(10, 30)):
                        Particle((q.rect.x + 15, q.rect.y + 15), particle_group, all_sprites)
                    break

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


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        self.image = load_image("blood.png")
        fire = []
        for scale in (2, 3, 4, 5):
            fire += [pygame.transform.scale(self.image, (scale, scale))]

        super().__init__(*groups)

        self.image = choice(fire)
        self.rect = self.image.get_rect()
        self.lifetime = 1000

        self.velocity = [randint(-50, 50), randint(-50, 50)]
        self.rect.x, self.rect.y = pos
        self.x, self.y = pos
        self.clock = pygame.time.Clock()

    def update(self, walls_group):
        tick = self.clock.tick()
        self.lifetime -= tick
        self.x += self.velocity[0] * tick / 1000
        self.y += self.velocity[1] * tick / 1000
        if pygame.sprite.spritecollideany(self, walls_group):
            self.velocity = [0, 0]
        self.rect.x = self.x
        self.rect.y = self.y
        if self.lifetime < 1:
            self.velocity = [0, 0]


tile_width = tile_height = 50

level_name = list(open('lvlname.data', 'r'))[0]
# open('lvlname.data', 'w').close()
print(level_name)

pygame.init()

level = load_level(level_name)
print(*level, sep='\n')

ysize = len(level)
xsize = len(level[0])
width = WIDTH = xsize * tile_width
height = HEIGHT = ysize * tile_height

print(xsize, ysize)

screen = pygame.display.set_mode((500, 500))
# pygame.mouse.set_visible(False)
pygame.display.set_caption('LAGame')

tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png'),
               'gate_c': load_image('gate_o.png'), 'gate_o': load_image('gate_o.png')}
player_image = load_image('mar.png', -1)
s_enemy_image = load_image('s_ene.png', -1)
m_enemy_image = load_image('m_ene.png', -1)
f_bullet_image = load_image('fb.png', -1)
e_bullet_image = load_image('eb.png', -1)

loaded_levels = [generate_level(level)]
now = -1

running = True

while running:
    loaded_levels[now]['players'].update(loaded_levels[now]['walls'], loaded_levels[now]['gates'],
                                         loaded_levels[now]['enemy'])
    loaded_levels[now]['enemy'].update(loaded_levels[now]['players'], loaded_levels[now]['walls'],
                                       loaded_levels[now]['particles'], loaded_levels[now]['all'])
    loaded_levels[now]['particles'].update(loaded_levels[now]['walls'])
    loaded_levels[now]['bullets'].update(loaded_levels[now]['walls'], loaded_levels[now]['enemy'],
                                         loaded_levels[now]['players'], loaded_levels[now]['particles'],
                                         loaded_levels[now]['all'])
    loaded_levels[now]['level'].fill((0, 0, 0))
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                pass
            elif event.button == 1:
                pass

        if event.type == pygame.KEYUP:
            if event.key == 100:
                loaded_levels[now]['player'].mr = False
            elif event.key == 97:
                loaded_levels[now]['player'].ml = False
            elif event.key == 119:
                loaded_levels[now]['player'].mu = False
            elif event.key == 115:
                loaded_levels[now]['player'].md = False
            if event.key == 103:
                loaded_levels[now]['player'].god = False
            if event.key == 27:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if not loaded_levels[now]['player'].last_bullet:
                    Bullet(loaded_levels[now]['player'].rect.x + 10,
                           loaded_levels[now]['player'].rect.y + 10, 1, True,
                           loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                    loaded_levels[now]['player'].last_bullet = loaded_levels[now]['player'].shoot_rate
            elif event.key == pygame.K_LEFT:
                if not loaded_levels[now]['player'].last_bullet:
                    Bullet(loaded_levels[now]['player'].rect.x + 10,
                           loaded_levels[now]['player'].rect.y + 10, 3, True,
                           loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                    loaded_levels[now]['player'].last_bullet = loaded_levels[now]['player'].shoot_rate
            elif event.key == pygame.K_UP:
                if not loaded_levels[now]['player'].last_bullet:
                    Bullet(loaded_levels[now]['player'].rect.x + 10,
                           loaded_levels[now]['player'].rect.y + 10, 0, True,
                           loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                    loaded_levels[now]['player'].last_bullet = loaded_levels[now]['player'].shoot_rate
            elif event.key == pygame.K_DOWN:
                if not loaded_levels[now]['player'].last_bullet:
                    Bullet(loaded_levels[now]['player'].rect.x + 10,
                           loaded_levels[now]['player'].rect.y + 10, 2, True,
                           loaded_levels[now]['bullets'], loaded_levels[now]['all'])
                    loaded_levels[now]['player'].last_bullet = loaded_levels[now]['player'].shoot_rate
            if event.key == 100:
                loaded_levels[now]['player'].mr = True
            elif event.key == 97:
                loaded_levels[now]['player'].ml = True
            elif event.key == 119:
                loaded_levels[now]['player'].mu = True
            elif event.key == 115:
                loaded_levels[now]['player'].md = True
            if event.key == 103:
                loaded_levels[now]['player'].god = True
            if event.key == 27:
                running = False

    loaded_levels[now]['all'].draw(loaded_levels[now]['level'])
    screen.blit(loaded_levels[now]['level'], (
        -(loaded_levels[now]['player'].rect.x + loaded_levels[now]['player'].rect.w // 2 - 250),
        -(loaded_levels[now]['player'].rect.y + loaded_levels[now]['player'].rect.h // 2 - 250)
    ))
    pygame.display.flip()

print('Работа завершена...')
terminate()
