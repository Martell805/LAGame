import pygame
import sys
import os
from LAGClasses import *


tile_width = tile_height = 50

pygame.init()


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
    try:
        level_map = [line.strip() for line in open(filename, 'r')]
    except Exception:
        print('Указанного уровня не существует.')
        print('Забота программы завершена.')
        terminate()

    max_width = max(map(len, level_map))
    level_map = list(map(lambda x: '#' + x.ljust(max_width, '.') + '#', level_map))
    max_width += 2
    level_map = ['#' * max_width] + level_map + ['#' * max_width]
    return level_map


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level_map, tile_images, player_image):
    px, py = None, None
    all_sprites = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    gates_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '.':
                Tile('empty', x, y, tile_images, all_sprites)
            elif level_map[y][x] == '#':
                Tile('wall', x, y, tile_images, all_sprites, walls_group)
            elif level_map[y][x] == '@':
                Tile('empty', x, y, tile_images, all_sprites)
                px = x
                py = y
            elif level_map[y][x] == 'G':
                Tile('gate_c', x, y, all_sprites, gates_group)
    players_group = pygame.sprite.Group()
    s = {'player': Player(px, py, 100, player_image, players_group, all_sprites), 'walls': walls_group,
         'bullets': pygame.sprite.Group(), 'enemy': enemy_group, 'all': all_sprites, 'players': players_group,
         'gates': gates_group}
    return s

