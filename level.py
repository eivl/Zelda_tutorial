import operator
import random

import pygame
from settings import *
from support import import_csv_layout, import_folder
from tile import Tile
from player import Player
from debug import debug
from weapon import Weapon


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player = None

        # Attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

    def create_attack(self):
        self.current_attack = Weapon(self.player, (self.visible_sprites,))

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), (self.obstacle_sprites,), 'invisible')
                        if style == 'grass':
                            Tile(
                                (x, y),
                                (self.visible_sprites, self.obstacle_sprites,),
                                'grass',
                                random.choice(graphics['grass']),
                            )
                        if style == 'object':
                            Tile(
                                (x, y),
                                (self.visible_sprites, self.obstacle_sprites,),
                                'object',
                                graphics['objects'][int(col)],
                            )

        self.player = Player(
            (2000, 1430),
            (self.visible_sprites,),
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack,
        )

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

        # Create the floor.
        self.floor_surface = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = self.half_width - player.rect.centerx
        self.offset.y = self.half_height - player.rect.centery

        self.display_surface.blit(self.floor_surface, (self.offset.x, self.offset.y))

        for sprite in sorted(self.sprites(), key=operator.attrgetter("rect.y")):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)
