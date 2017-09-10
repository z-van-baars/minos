import pygame
import utilities

pygame.init()
pygame.display.set_mode([0, 0])


# tiles
selected_tile_image = pygame.image.load("art/tiles/selected.png").convert()
selected_tile_image.set_colorkey(utilities.colors.key)
selected_tile_image = selected_tile_image.convert_alpha()

grass_tile_image_1 = pygame.image.load("art/tiles/grass_1.png").convert()
grass_tile_image_1.set_colorkey(utilities.colors.key)
grass_tile_image_1 = grass_tile_image_1.convert_alpha()



# terrain
tree_image_1 = pygame.image.load("art/constructs/terrain/tree_1.png").convert()
tree_image_1.set_colorkey(utilities.colors.key)
tree_image_1 = tree_image_1.convert_alpha()


# buildings
house_image_1 = pygame.image.load("art/constructs/buildings/house_1.png").convert()
house_image_1.set_colorkey(utilities.colors.key)
house_image_1 = house_image_1.convert_alpha()

