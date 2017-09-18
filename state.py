import pygame
import construct
import utilities


build_list = ["Palace",
              "Lumber Camp",
              "Stone Mine",
              "House",
              "Temple",
              "Farm"]

build_dict = {"Palace": construct.Palace,
              "House": construct.House,
              "Lumber Camp": construct.LumberCamp,
              "Stone Mine": construct.StoneMine,
              "Temple": construct.Temple,
              "Farm": construct.Farm}


class GameState(object):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = pygame.time.Clock()
        self.calendar = utilities.Calendar()
        self.game_speed = 60
        self.stats = Stats()
        self.time = 0
        self.timer = 0
        self.control = False
        self.palace = None
        self.resources = {"Wood": 10250,
                          "Food": 100,
                          "Stone": 5000,
                          "Labor": 1100}
        self.last_step_consumed_resources = {"Wood": 0,
                                             "Food": 0,
                                             "Stone": 0,
                                             "Copper": 0,
                                             "Labor": 0}
        self.last_step_produced_resources = {"Wood": 0,
                                             "Food": 0,
                                             "Stone": 0,
                                             "Copper": 0,
                                             "Labor": 0}

        self.active_map = None
        self.remove = False
        self.activation_mode = False
        self.build_menu = False
        self.build_candidate = "None"
        self.selected_construct = None
        self.reset_surfaces()

    def reset_surfaces(self):
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

    def log_statistics(self):
        self.stats.total_steps += 1
        house_count = 0
        for each_building in self.active_map.buildings:
            if each_building.display_name == "House":
                house_count += 1
        self.victory_points = house_count
        self.stats.houses.append(house_count)
        for each_key, each_value in self.resources.items():
            self.stats.resources[each_key].append(each_value)
        for each_key, each_value in self.last_step_consumed_resources.items():
            self.stats.consumed_resources[each_key].append(each_value)
        for each_key, each_value in self.last_step_produced_resources.items():
            self.stats.produced_resources[each_key].append(each_value)

    def aura_bonuses(self, active_map):
        for building in active_map.buildings:
            if building.active:
                building.aura_bonus(active_map)

    def unit_production(self, active_map, last_step_consumed_resources, last_step_produced_resources):
        for building in active_map.buildings:
            resources_consumed, resources_produced = building.produce(active_map, self.resources)
            for key, value in resources_consumed.items():
                last_step_consumed_resources[key] += value
                self.resources[key] -= value
            for key, value in resources_produced.items():
                last_step_produced_resources[key] += value
                self.resources[key] += value
        return last_step_consumed_resources, last_step_produced_resources

    def cull_terrain_objects(self, active_map):
        def check_resources(terrain_object):
            if all([terrain_object.raw_resources["Wood"] == 0,
                    terrain_object.raw_resources["Stone"] == 0,
                    terrain_object.raw_resources["Food"] == 0,
                    terrain_object.raw_resources["Copper"] == 0,
                    terrain_object.raw_resources["Labor"] == 0]):
                return False
            return True

        terrain_removal_flag = False
        for terrain in active_map.terrain:
            if not check_resources(terrain):
                terrain_removal_flag = True
                active_map.terrain.remove(terrain)
                active_map.game_tile_rows[terrain.tile_y][terrain.tile_x].construct = None
        return terrain_removal_flag

    def unit_processing(self):
        last_step_consumed_resources = {"Wood": 0,
                                        "Food": 0,
                                        "Stone": 0,
                                        "Copper": 0,
                                        "Labor": 0}
        last_step_produced_resources = {"Wood": 0,
                                        "Food": 0,
                                        "Stone": 0,
                                        "Copper": 0,
                                        "Labor": 0}

        if self.timer < self.game_speed:
            self.timer += 1
            return
        self.timer = 0
        active_map = self.active_map

        self.aura_bonuses(active_map)
        self.unit_production(active_map, last_step_consumed_resources, last_step_produced_resources)
        self.last_step_consumed_resources = last_step_consumed_resources
        self.last_step_produced_resources = last_step_produced_resources

        terrain_removal_flag = self.cull_terrain_objects(active_map)
        if terrain_removal_flag:
            active_map.paint_resources()
        self.log_statistics()


class Stats(object):
    def __init__(self):
        self.total_steps = 0
        self.resources = {"Wood": [],
                          "Food": [],
                          "Stone": [],
                          "Copper": [],
                          "Labor": []}
        self.consumed_resources = {"Wood": [],
                                   "Food": [],
                                   "Stone": [],
                                   "Copper": [],
                                   "Labor": []}
        self.produced_resources = {"Wood": [],
                                   "Food": [],
                                   "Stone": [],
                                   "Copper": [],
                                   "Labor": []}
        self.houses = []
