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

radius_tile_image_1 = pygame.image.load("art/tiles/radius_preview.png").convert()
radius_tile_image_1.set_colorkey(utilities.colors.key)
radius_tile_image_1 = radius_tile_image_1.convert_alpha()



# terrain
tree_image_1 = pygame.image.load("art/constructs/terrain/tree_1.png").convert()
tree_image_1.set_colorkey(utilities.colors.key)
tree_image_1 = tree_image_1.convert_alpha()

copper_pile_image_1 = pygame.image.load("art/constructs/terrain/copper_pile_1.png").convert()
copper_pile_image_1.set_colorkey(utilities.colors.key)
copper_pile_image_1 = copper_pile_image_1.convert_alpha()

stone_pile_image_1 = pygame.image.load("art/constructs/terrain/stone_pile_1.png").convert()
stone_pile_image_1.set_colorkey(utilities.colors.key)
stone_pile_image_1 = stone_pile_image_1.convert_alpha()


# buildings
copper_mine_image_1 = pygame.image.load("art/constructs/buildings/copper_mine_1.png").convert()
copper_mine_image_1.set_colorkey(utilities.colors.key)
copper_mine_image_1 = copper_mine_image_1.convert_alpha()

farm_image_1 = pygame.image.load("art/constructs/buildings/farm_1.png").convert()
farm_image_2 = pygame.image.load("art/constructs/buildings/farm_2.png").convert()
farm_image_1.set_colorkey(utilities.colors.key)
farm_image_2.set_colorkey(utilities.colors.key)
farm_image_1 = farm_image_1.convert_alpha()
farm_image_2 = farm_image_2.convert_alpha()

house_images = []
for ii in range(1, 8):
    house_image = pygame.image.load("art/constructs/buildings/house_{0}.png".format(ii)).convert()
    house_image.set_colorkey(utilities.colors.key)
    house_image = house_image.convert_alpha()
    house_images.append(house_image)

lumber_camp_image_1 = pygame.image.load("art/constructs/buildings/lumber_camp_1.png").convert()
lumber_camp_image_1.set_colorkey(utilities.colors.key)
lumber_camp_image_1 = lumber_camp_image_1.convert_alpha()

palace_image_1 = pygame.image.load("art/constructs/buildings/palace_1.png").convert()
palace_image_1.set_colorkey(utilities.colors.key)
palace_image_1 = palace_image_1.convert_alpha()

road_image_1 = pygame.image.load("art/constructs/buildings/road_1.png").convert()
road_image_1.set_colorkey(utilities.colors.key)
road_image_1 = road_image_1.convert_alpha()


stone_mine_image_1 = pygame.image.load("art/constructs/buildings/stone_mine_1.png").convert()
stone_mine_image_1.set_colorkey(utilities.colors.key)
stone_mine_image_1 = stone_mine_image_1.convert_alpha()

temple_image_1 = pygame.image.load("art/constructs/buildings/temple_1.png").convert()
temple_image_1.set_colorkey(utilities.colors.key)
temple_image_1 = temple_image_1.convert_alpha()
