import pygame
import art


class Construct(object):
    def __init__(self, x, y):
        self.tile_x = x
        self.tile_y = y
        self.sprite = pygame.sprite.Sprite()

    def __lt__(self, other):
        return False

    def set_image(self):
        self.sprite.rect = self.sprite.image.get_rect()

    def spread(self):
        pass


class House(Construct):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.house_image_1
        self.sprite.image = self.sprite.image.convert_alpha()


class Tree(Construct):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.set_image()

    def set_image(self):
        self.sprite.image = art.tree_image_1
        self.sprite.image = self.sprite.image.convert_alpha()
