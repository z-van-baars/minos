import pygame
import art
import utilities
import random

# Make constructs remember their choice for multiple choice sprites


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
                              "Copper": 0,
                              "Labor": 0}
        self.set_orbit(active_map, x, y)
        self.base_consumption_modifier = 1.0
        self.consumption_modifier = 1.0
        self.base_production_modifier = 1.0
        self.production_modifier = 1.0

    def __lt__(self, other):
        return False

    def set_orbit(self, active_map, x, y):
        self.orbit = utilities.get_nearby_tiles(active_map, (x, y), self.radius)

    def reset_modifiers(self):
        self.consumption_modifier = self.base_consumption_modifier
        self.production_modifier = self.base_production_modifier

    def set_image(self):
        self.sprite.rect = self.sprite.image.get_rect()

    def aura_bonus(self, active_map):
        pass

    def produce(self, active_map, resources):
        pass


class House(Construct):
    cost = {"Wood": 50,
            "Labor": 5}
    display_name = "House"
    radius = 0

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = random.choice(art.house_images)
        self.sprite.image = self.sprite.image.convert_alpha()

    def produce(self, active_map, resources):
        consumed_resources = {}
        produced_resources = {}
        if resources["Food"] < 5:
            return consumed_resources, produced_resources
        consumed_resources["Food"] = 5 * self.consumption_modifier
        produced_resources["Labor"] = 1 * self.production_modifier
        self.reset_modifiers()
        return consumed_resources, produced_resources


class Farm(Construct):
    cost = {"Wood": 30,
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
        consumed_resources = {}
        produced_resources = {}
        if resources["Labor"] < 1 or resources["Wood"] < 1:
            return consumed_resources, produced_resources
        consumed_resources["Labor"] = 1 * self.consumption_modifier
        produced_resources["Food"] = 6 * self.production_modifier
        self.reset_modifiers()
        return consumed_resources, produced_resources


class LumberCamp(Construct):
    cost = {"Labor": 5}
    display_name = "Lumber Camp"
    radius = 4

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.lumber_camp_image_1
        self.sprite.image = self.sprite.image.convert_alpha()

    def produce(self, active_map, resources):
        consumed_resources = {}
        produced_resources = {}
        if resources["Labor"] < 1:
            return consumed_resources, produced_resources
        total_extracted_wood = 0
        for tile in self.orbit:
            if tile.construct and tile.construct.raw_resources["Wood"] > 0:
                extracted_wood = min(1 * self.production_modifier, tile.construct.raw_resources["Wood"])
                tile.construct.raw_resources["Wood"] -= extracted_wood
                total_extracted_wood += extracted_wood
        if total_extracted_wood > 0:
            consumed_resources["Labor"] = 1 * self.consumption_modifier
        produced_resources["Wood"] = total_extracted_wood
        self.reset_modifiers()
        return consumed_resources, produced_resources


class StoneMine(Construct):
    cost = {"Wood": 100,
            "Labor": 5}
    display_name = "Stone Mine"
    radius = 4

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.stone_mine_image_1
        self.sprite.image = self.sprite.image.convert_alpha()

    def produce(self, active_map, resources):
        consumed_resources = {}
        produced_resources = {}
        if resources["Labor"] < 1 * self.consumption_modifier:
            return consumed_resources, produced_resources
        consumed_resources["Labor"] = 0
        produced_resources["Stone"] = 0
        for tile in self.orbit:
            if tile.construct and tile.construct.raw_resources["Stone"] > 0:
                extracted_stone = min(1 * self.production_modifier, tile.construct.raw_resources["Stone"])
                tile.construct.raw_resources["Stone"] -= extracted_stone
                if extracted_stone > 0:
                    consumed_resources["Labor"] = min(5, consumed_resources["Labor"] + 1 * self.consumption_modifier)
                produced_resources["Stone"] += extracted_stone
                if resources["Labor"] < 1 * self.consumption_modifier:
                    self.reset_modifiers()
                    return consumed_resources, produced_resources
        self.reset_modifiers()
        return consumed_resources, produced_resources


class Temple(Construct):
    cost = {"Wood": 200,
            "Stone": 0,
            "Labor": 50}
    display_name = "Temple"
    radius = 8

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.temple_image_1
        self.sprite.image = self.sprite.image.convert_alpha()

    def produce(self, active_map, resources):
        consumed_resources = {}
        produced_resources = {}
        if resources["Labor"] < 3 * self.consumption_modifier:
            return consumed_resources, produced_resources
        consumed_resources["Labor"] = 3 * self.consumption_modifier
        self.reset_modifiers()
        return consumed_resources, produced_resources

    def aura_bonus(self, active_map):
        for tile in self.orbit:
            if tile.construct and tile.construct.display_name == "House":
                tile.construct.production_modifier = 1.1


class Palace(Construct):
    cost = {"Wood": 10000,
            "Stone": 5000,
            "Labor": 1000}
    display_name = "Palace"
    radius = 6

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.palace_image_1
        self.sprite.image = self.sprite.image.convert_alpha()

    def produce(self, active_map, resources):
        consumed_resources = {}
        produced_resources = {}
        self.reset_modifiers()
        return consumed_resources, produced_resources

    def aura_bonus(self, active_map):
        for tile in self.orbit:
            if tile.construct and tile.construct.display_name == "House":
                tile.construct.consumption_modifier = 0.9
            if tile.construct and tile.construct.display_name == "Temple":
                tile.construct.consumption_modifier = 0.66


class CopperPile(Construct):
    display_name = "Copper"
    radius = 0

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()
        self.raw_resources["Copper"] = 800

    def set_image(self):
        self.sprite.image = art.copper_pile_image_1
        self.sprite.image = self.sprite.image.convert_alpha()


class StonePile(Construct):
    display_name = "Stone"
    radius = 0

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()
        self.raw_resources["Stone"] = 1000

    def set_image(self):
        self.sprite.image = art.stone_pile_image_1
        self.sprite.image = self.sprite.image.convert_alpha()


class Tree(Construct):
    display_name = "Tree"
    radius = 0

    def __init__(self, x, y, active_map):
        super().__init__(x, y, active_map)
        self.set_image()
        self.raw_resources["Wood"] = 250

    def set_image(self):
        self.sprite.image = art.tree_image_1
        self.sprite.image = self.sprite.image.convert_alpha()
