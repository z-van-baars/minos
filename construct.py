import pygame
import art
import utilities
import random


class Construct(object):
    display_name = "N/A"
    radius = 0

    def __init__(self, x, y, active_map):
        self.active_map = active_map
        self.tile_x = x
        self.tile_y = y
        self.sprite = pygame.sprite.Sprite()
        self.orbit = []
        self.raw_resources = {"Wood": 0,
                              "Food": 0,
                              "Stone": 0,
                              "Labor": 0}
        self.set_orbit(active_map, x, y)

    def __lt__(self, other):
        return False

    def set_orbit(self, active_map, x, y):
        self.orbit = utilities.get_nearby_tiles(active_map, (x, y), self.radius)

    def set_image(self):
        self.sprite.rect = self.sprite.image.get_rect()

    def produce(self, active_map, resources):
        pass


class House(Construct):
    cost = {"Wood": 25,
            "Stone": 0,
            "Food": 0,
            "Labor": 5}
    display_name = "House"
    radius = 0

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.house_image_1
        self.sprite.image = self.sprite.image.convert_alpha()

    def produce(self, active_map, resources):
        consumed_resources = {"Wood": 0,
                              "Food": 0,
                              "Stone": 0,
                              "Labor": 0}
        produced_resources = {"Wood": 0,
                              "Food": 0,
                              "Stone": 0,
                              "Labor": 0}
        if resources["Food"] < 5:
            return consumed_resources, produced_resources
        consumed_resources["Food"] += 5
        produced_resources["Labor"] += 1
        return consumed_resources, produced_resources


class Farm(Construct):
    cost = {"Wood": 10,
            "Stone": 0,
            "Food": 0,
            "Labor": 2}
    display_name = "Farm"
    radius = 0

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = random.choice([art.farm_image_1, art.farm_image_2])
        self.sprite.image = self.sprite.image.convert_alpha()

    def produce(self, active_map, resources):
        consumed_resources = {"Wood": 0,
                              "Food": 0,
                              "Stone": 0,
                              "Labor": 0}
        produced_resources = {"Wood": 0,
                              "Food": 0,
                              "Stone": 0,
                              "Labor": 0}
        if resources["Labor"] < 1 or resources["Wood"] < 1:
            return consumed_resources, produced_resources
        consumed_resources["Labor"] += 1
        consumed_resources["Wood"] += 1
        produced_resources["Food"] += 6
        return consumed_resources, produced_resources


class LumberCamp(Construct):
    cost = {"Wood": 10,
            "Stone": 0,
            "Food": 0,
            "Labor": 2}
    display_name = "Lumber Camp"
    radius = 4

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.lumber_camp_image_1
        self.sprite.image = self.sprite.image.convert_alpha()

    def produce(self, active_map, resources):
        consumed_resources = {"Wood": 0,
                              "Food": 0,
                              "Stone": 0,
                              "Labor": 0}
        produced_resources = {"Wood": 0,
                              "Food": 0,
                              "Stone": 0,
                              "Labor": 0}
        if resources["Labor"] < 1:
            return consumed_resources, produced_resources
        total_extracted_wood = 0
        for tile in self.orbit:
            if tile.construct and tile.construct.raw_resources["Wood"] > 0:
                extracted_wood = min(1, tile.construct.raw_resources["Wood"])
                tile.construct.raw_resources["Wood"] -= extracted_wood
                total_extracted_wood += extracted_wood
        if total_extracted_wood > 0:
            consumed_resources["Labor"] += 1
        produced_resources["Wood"] += total_extracted_wood
        return consumed_resources, produced_resources


class Palace(Construct):
    cost = {"Wood": 10000,
            "Stone": 5000,
            "Food": 0,
            "Labor": 1000}
    display_name = "Palace"
    radius = 10

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.palace_image_1
        self.sprite.image = self.sprite.image.convert_alpha()

    def produce(self, active_map, resources):
        consumed_resources = {"Wood": 0,
                              "Food": 0,
                              "Stone": 0,
                              "Labor": 0}
        produced_resources = {"Wood": 0,
                              "Food": 0,
                              "Stone": 0,
                              "Labor": 0}
        return consumed_resources, produced_resources


class Tree(Construct):
    display_name = "Tree"
    radius = 0

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()
        self.raw_resources["Wood"] = 100

    def set_image(self):
        self.sprite.image = art.tree_image_1
        self.sprite.image = self.sprite.image.convert_alpha()
