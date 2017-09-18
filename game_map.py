import pygame
from game_tile import GameTile
import utilities
from utilities import colors
import queue
import art
import math
import random
import construct
import queue


tile_width = 40
tile_height = 15


class DisplayLayer(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        layer_width = (width * math.floor(tile_width / 2)) + (height * math.floor(tile_width / 2))
        layer_height = (width * math.floor(tile_height / 2)) + (height * math.floor(tile_height / 2))
        self.image = pygame.Surface([layer_width, layer_height])
        self.image.fill(colors.key)
        self.rect = self.image.get_rect()


class Map(object):
    def __init__(self, map_dimensions, screen_dimensions):
        self.tile_display_layer = None
        self.terrain_display_layer = None
        self.building_display_layer = None
        self.screen_dimensions = screen_dimensions
        self.width = map_dimensions[0]
        self.height = map_dimensions[1]
        self.number_of_columns = map_dimensions[0]
        self.number_of_rows = map_dimensions[1]
        self.game_tile_rows = []
        self.constructs = []
        self.terrain = []
        self.buildings = []
        self.displayshift_x = 0
        self.displayshift_y = 0

    def generate_blank_grass_tiles(self):
        self.game_tile_rows = []
        for y_row in range(self.number_of_rows):
            this_row = []
            for x_column in range(self.number_of_columns):
                this_row.append(GameTile(x_column, y_row))
            self.game_tile_rows.append(this_row)

    def spread_contiguous_resource(self, seed, mine_tiles):
        seed_tile = self.game_tile_rows[seed[1]][seed[0]]
        mine_size = random.randint(4, 8)
        candidates = []
        new_mine_tiles = [seed_tile]
        candidates = utilities.get_adjacent_tiles(seed_tile, self)
        for ll in range(mine_size):
            mine_choice = None
            while not mine_choice:
                mine_choice = candidates.pop()
                if mine_choice.is_occupied():
                    mine_choice = None
            new_candidates = utilities.get_adjacent_tiles(mine_choice, self)
            for candidate in candidates:
                if candidate not in new_candidates:
                    new_candidates.append(candidate)
            candidates = new_candidates
            new_mine_tiles.append(mine_choice)
        return new_mine_tiles

    def generate_mines(self, width, height, mine_type, number_of_mines):
        mine_seeds = []
        for ii in range(number_of_mines):
            new_mine_seed = False
            while not new_mine_seed:
                new_mine_seed = utilities.get_random_coordinates(0, width - 1, 0, height - 1)
                for jj in mine_seeds:
                    if utilities.distance(new_mine_seed[0], new_mine_seed[1], jj[0], jj[1]) < 10:
                        new_mine_seed = False
                        break
                if new_mine_seed and self.game_tile_rows[new_mine_seed[1]][new_mine_seed[0]].is_occupied():
                    new_mine_seed = False

            mine_seeds.append(new_mine_seed)
        mine_tiles = []
        for kk in mine_seeds:
            mine_tiles += self.spread_contiguous_resource(kk, mine_tiles)

        for tile in mine_tiles:
            new_pile = mine_type(tile.column, tile.row, self)
            self.game_tile_rows[tile.row][tile.column].construct = new_pile
            self.terrain.append(new_pile)

    def generate_forests(self, width, height):
        number_of_forests = math.floor(math.sqrt(width * height))
        for ii in range(number_of_forests):
            new_forest_center = False
            while not new_forest_center:
                new_forest_center = utilities.get_random_coordinates(0, width - 1, 0, height - 1)
                if self.game_tile_rows[new_forest_center[1]][new_forest_center[0]].is_occupied():
                    new_forest_center = False
            forest_tiles = utilities.get_nearby_tiles(self, new_forest_center, math.floor(math.sqrt(number_of_forests) / 2))
            forest_size = random.randint(math.floor(math.sqrt(number_of_forests)), math.floor(math.sqrt(number_of_forests) * 2))
            for jj in range(forest_size):
                new_tree_xy = random.choice(forest_tiles)
                if self.game_tile_rows[new_tree_xy.row][new_tree_xy.column].is_occupied():
                    new_tree_xy = False
                if new_tree_xy:
                    new_tree = construct.Tree(new_tree_xy.column, new_tree_xy.row, self)
                    self.terrain.append(new_tree)
                    self.game_tile_rows[new_tree_xy.row][new_tree_xy.column].construct = new_tree

    def generate_resources(self, width, height):
        number_of_copper_mines = math.floor(math.sqrt((math.sqrt(width * height))))
        self.generate_mines(width, height, construct.CopperPile, number_of_copper_mines)
        number_of_stone_mines = math.floor(math.sqrt(width * height) / 2)
        self.generate_mines(width, height, construct.StonePile, number_of_stone_mines)
        self.generate_forests(width, height)

    def paint_resources(self):
        self.terrain_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.terrain_display_layer.image.get_width() / 2)
        for terrain_object in self.terrain:
            terrain_image = terrain_object.sprite.image
            x, y = utilities.get_screen_coords(terrain_object.tile_x, terrain_object.tile_y)
            self.terrain_display_layer.image.blit(terrain_image, [x + background_x_middle + (tile_width / 2), y - 25])
        self.terrain_display_layer.image.set_colorkey(colors.key)
        self.terrain_display_layer.image = self.terrain_display_layer.image.convert_alpha()

    def paint_buildings(self):
        self.building_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.building_display_layer.image.get_width() / 2)
        buildings_to_draw = queue.PriorityQueue()
        for building_object in self.buildings:
            x, y = utilities.get_screen_coords(building_object.tile_x, building_object.tile_y)
            buildings_to_draw.put((y, x, building_object.sprite.image))
        while not buildings_to_draw.empty():
            y, x, building_image = buildings_to_draw.get()
            self.building_display_layer.image.blit(building_image, [x + background_x_middle + (tile_width / 2), y - 25])
        self.building_display_layer.image.set_colorkey(colors.key)
        self.building_display_layer.image = self.building_display_layer.image.convert_alpha()

    def paint_background_tiles(self, game_tile_rows):
        tile_width = 40
        self.tile_display_layer = DisplayLayer(self.width, self.height)
        background_x_middle = (self.tile_display_layer.image.get_width() / 2)
        for y_row in game_tile_rows:
            for tile in y_row:
                new_tile_image = art.grass_tile_image_1
                x, y = utilities.get_screen_coords(tile.column, tile.row)
                self.tile_display_layer.image.blit(new_tile_image, [x + background_x_middle + (tile_width / 2), y])
        self.tile_display_layer.image.set_colorkey(colors.key)
        self.tile_display_layer.image = self.tile_display_layer.image.convert_alpha()

    def map_generation(self):
        self.generate_blank_grass_tiles()
        self.generate_resources(self.width, self.height)
        self.paint_background_tiles(self.game_tile_rows)
        self.paint_resources()
        self.paint_buildings()

    def world_scroll(self, shift_x, shift_y, screen_width, screen_height):
        background_width = self.tile_display_layer.image.get_width()
        background_height = self.tile_display_layer.image.get_height()
        self.x_shift += shift_x
        self.y_shift += shift_y
        if self.y_shift < -(background_height - 40):
            self.y_shift = -(background_height - 40)
        elif self.y_shift > screen_height + -40:
            self.y_shift = screen_height + -40
        if self.x_shift < -(background_width - 40):
            self.x_shift = -(background_width - 40)
        if self.x_shift > screen_width + -40:
            self.x_shift = screen_width + -40

    def draw_to_screen(self, screen):
        background_x_middle = self.tile_display_layer.rect.left + (self.tile_display_layer.image.get_width()) / 2
        objects_to_draw = queue.PriorityQueue()
        for each in self.constructs:
            screen_coordinates = utilities.get_screen_coords(each.tile_x,
                                                             each.tile_y,
                                                             self.x_shift,
                                                             self.y_shift,
                                                             self.tile_display_layer.rect.top,
                                                             background_x_middle)
            objects_to_draw.put((screen_coordinates[1], screen_coordinates[0], each))

        while not objects_to_draw.empty():
            y, x, construct = objects_to_draw.get()
            screen.blit(construct.sprite.image, [(x + self.x_shift),
                                                 (y + self.y_shift)])

