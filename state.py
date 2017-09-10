import pygame
import construct
import pickle
import utilities


build_list = ["Palace",
              "Lumber Camp",
              "House"]

build_dict = {"Palace": construct.Palace,
              "House": construct.House,
              "Lumber Camp": construct.LumberCamp}


class GameState(object):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = pygame.time.Clock()
        self.calendar = utilities.Calendar()
        self.game_speed = 1
        self.time = 0
        self.population = 0
        self.wood = 100
        self.labor = 100
        self.food = 100
        self.active_map = None
        self.reset_surfaces()

    def reset_surfaces(self):
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
