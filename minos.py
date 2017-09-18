import pygame
import utilities
import game_map
import art
import construct
import state
import math


### TODO ###
# Ctrl + D for unit deselect

pygame.init()
pygame.display.set_mode([0, 0])


tiny_font = pygame.font.SysFont('Calibri', 11, True, False)
small_font = pygame.font.SysFont('Calibri', 14, True, False)


def cost_check(game_state, building):
    for each_resource, each_value in building.cost.items():
        if game_state.resources[each_resource] - building.cost[each_resource] < 0:
            return False
    return True


def build(game_state, selected_tile, background_left, background_top, background_right, background_bottom, mouse_pos):
    if utilities.check_if_inside(background_left,
                                 background_right,
                                 background_top,
                                 background_bottom,
                                 mouse_pos):
        if selected_tile is not None and selected_tile.construct is None:
            if not cost_check(game_state, state.build_dict[game_state.build_candidate]):
                print("Not Enough Resources!")
                return
            new_building = state.build_dict[game_state.build_candidate](selected_tile.column, selected_tile.row, game_state.active_map)
            game_state.active_map.buildings.append(new_building)
            game_state.active_map.game_tile_rows[selected_tile.row][selected_tile.column].construct = new_building
            for each_resource, each_value in new_building.cost.items():
                game_state.resources[each_resource] -= new_building.cost[each_resource]
            game_state.active_map.paint_resources()
            game_state.active_map.paint_buildings()
        else:
            return


def remove(game_state, selected_tile):
    if selected_tile.construct and selected_tile.construct in game_state.active_map.buildings:
        game_state.active_map.buildings.remove(selected_tile.construct)
        selected_tile.construct = None
    game_state.active_map.paint_buildings()


def do_nothing(game_state):
    pass


def b_key(game_state):
    game_state.remove = False
    game_state.build_candidate = "None"
    game_state.build_candidate = "House"
    game_state.build_menu = not game_state.build_menu


def d_key(game_state):
    if not game_state.control:
        return
    game_state.selected_construct = None


def f_key(game_state):
    if game_state.build_menu:
        game_state.build_candidate = "Farm"


def g_key(game_state):
    if not game_state.control:
        return
    print_stat_graph(game_state)


def h_key(game_state):
    if game_state.build_menu:
        game_state.build_candidate = "House"


def l_key(game_state):
    if game_state.build_menu:
        game_state.build_candidate = "Lumber Camp"


def p_key(game_state):
    if game_state.build_menu:
        game_state.build_candidate = "Palace"


def r_key(game_state):
    game_state.remove = not game_state.remove
    game_state.build_menu = False


def control_key(game_state):
    game_state.control = True


def up_key(game_state):
    game_state.active_map.world_scroll(0,
                                       40,
                                       game_state.screen_width,
                                       game_state.screen_height)


def down_key(game_state):
    game_state.active_map.world_scroll(0,
                                       -40,
                                       game_state.screen_width,
                                       game_state.screen_height)


def left_key(game_state):
    game_state.active_map.world_scroll(40,
                                       0,
                                       game_state.screen_width,
                                       game_state.screen_height)


def right_key(game_state):
    game_state.active_map.world_scroll(-40,
                                       0,
                                       game_state.screen_width,
                                       game_state.screen_height)


key_functions = {pygame.K_UP: up_key,
                 pygame.K_DOWN: down_key,
                 pygame.K_LEFT: left_key,
                 pygame.K_RIGHT: right_key,
                 pygame.K_LCTRL: control_key,
                 pygame.K_b: b_key,
                 pygame.K_f: f_key,
                 pygame.K_g: g_key,
                 pygame.K_h: h_key,
                 pygame.K_l: l_key,
                 pygame.K_p: p_key,
                 pygame.K_r: r_key}


def print_stats(game_state, selected_construct):
    wood_stamp = tiny_font.render("Wood: {0} (-{1}) (+{2})".format(str(game_state.resources["Wood"]),
                                                                   str(game_state.last_step_consumed_resources["Wood"]),
                                                                   str(game_state.last_step_produced_resources["Wood"])),
                                  True, utilities.colors.white)
    food_stamp = tiny_font.render("Food: {0} (-{1}) (+{2})".format(str(game_state.resources["Food"]),
                                                                   str(game_state.last_step_consumed_resources["Food"]),
                                                                   str(game_state.last_step_produced_resources["Food"])),
                                  True, utilities.colors.white)
    stone_stamp = tiny_font.render("Stone: {0} (-{1}) (+{2})".format(str(game_state.resources["Stone"]),
                                                                     str(game_state.last_step_consumed_resources["Stone"]),
                                                                     str(game_state.last_step_produced_resources["Stone"])),
                                   True, utilities.colors.white)
    labor_stamp = tiny_font.render("Labor: {0} (-{1}) (+{2})".format(str(game_state.resources["Labor"]),
                                                                     str(game_state.last_step_consumed_resources["Labor"]),
                                                                     str(game_state.last_step_produced_resources["Labor"])),
                                   True, utilities.colors.white)
    game_state.screen.blit(wood_stamp, [10, 10])
    game_state.screen.blit(food_stamp, [10, 21])
    game_state.screen.blit(stone_stamp, [10, 32])
    game_state.screen.blit(labor_stamp, [10, 43])
    if selected_construct:
        selected_construct_stamp = tiny_font.render("{0}".format(selected_construct.display_name), True, utilities.colors.white)
        center_offset = selected_construct_stamp.get_width() / 2
        selected_construct_display_start = game_state.screen.get_width() / 2 - center_offset
        game_state.screen.blit(selected_construct_stamp, [selected_construct_display_start, 10])
        raw_wood_stamp = tiny_font.render("Wood: {0}".format(str(selected_construct.raw_resources["Wood"])), True, utilities.colors.white)
        raw_food_stamp = tiny_font.render("Food: {0}".format(str(selected_construct.raw_resources["Food"])), True, utilities.colors.white)
        raw_stone_stamp = tiny_font.render("Stone: {0}".format(str(selected_construct.raw_resources["Stone"])), True, utilities.colors.white)
        raw_labor_stamp = tiny_font.render("Labor: {0}".format(str(selected_construct.raw_resources["Labor"])), True, utilities.colors.white)
        game_state.screen.blit(raw_wood_stamp, [selected_construct_display_start + 4, 21])
        game_state.screen.blit(raw_food_stamp, [selected_construct_display_start + 4, 32])
        game_state.screen.blit(raw_stone_stamp, [selected_construct_display_start + 4, 43])
        game_state.screen.blit(raw_labor_stamp, [selected_construct_display_start + 4, 54])


def print_stat_graph(game_state):
    viewing_graph = True
    game_state.screen.fill(utilities.colors.black)
    red_dot = pygame.Surface([1, 1])
    red_dot.fill(utilities.colors.red)
    green_dot = pygame.Surface([1, 1])
    green_dot.fill(utilities.colors.light_green)
    blue_dot = pygame.Surface([1, 1])
    blue_dot.fill(utilities.colors.blue)
    white_dot = pygame.Surface([1, 1])
    white_dot.fill(utilities.colors.white)

    step = 0
    while step < game_state.stats.total_steps:
        game_state.screen.blit(red_dot, [step,
                                         math.floor(game_state.screen.get_height() - game_state.stats.resources["Food"][step] / 2)])
        game_state.screen.blit(green_dot, [step,
                                           math.floor(game_state.screen.get_height() - game_state.stats.resources["Wood"][step] / 2)])
        game_state.screen.blit(blue_dot, [step,
                                          game_state.screen.get_height() - game_state.stats.resources["Labor"][step]])
        game_state.screen.blit(white_dot, [step,
                                           game_state.screen.get_height() - game_state.stats.houses[step]])
        pygame.display.flip()
        step += 1
    while viewing_graph:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()


def print_build_menu(game_state):
    build_stamp_margin = game_state.screen.get_height() - 40
    build_stamp = tiny_font.render("Build:", True, utilities.colors.white)
    game_state.screen.blit(build_stamp, [10, build_stamp_margin])
    if game_state.build_candidate:
        candidate_stamp = tiny_font.render(game_state.build_candidate, True, utilities.colors.white)
        game_state.screen.blit(candidate_stamp, [10, build_stamp_margin + 11])


def print_remove(game_state):
    remove_margin = game_state.screen.get_height() - 40
    remove_stamp = tiny_font.render("Remove: ", True, utilities.colors.white)
    game_state.screen.blit(remove_stamp, [10, remove_margin])


def update_display(game_state, selected_tile, background_left, background_top, background_right, background_bottom, background_x_middle, mouse_pos):
    active_map = game_state.active_map
    game_state.screen.fill(utilities.colors.background_blue)
    game_state.screen.blit(active_map.tile_display_layer.image, [background_left,
                                                                 background_top])
    if selected_tile is not None:
        selected_coords = utilities.get_screen_coords(selected_tile.column,
                                                      selected_tile.row)

        if game_state.build_menu:
            if state.build_dict[game_state.build_candidate].radius:
                radius_preview = utilities.get_nearby_tiles(active_map,
                                                            (selected_tile.column, selected_tile.row),
                                                            state.build_dict[game_state.build_candidate].radius)
                for each_tile in radius_preview:
                    x, y = utilities.get_screen_coords(each_tile.column, each_tile.row)
                    game_state.screen.blit(art.radius_tile_image_1, [x + background_x_middle, y + background_top])
        game_state.screen.blit(art.selected_tile_image, [selected_coords[0] + background_x_middle, selected_coords[1] + background_top])
    if game_state.selected_construct and game_state.selected_construct.radius:
        radius_preview = utilities.get_nearby_tiles(active_map,
                                                    (game_state.selected_construct.tile_x, game_state.selected_construct.tile_y),
                                                    game_state.selected_construct.radius)
        for each_tile in radius_preview:
            x, y = utilities.get_screen_coords(each_tile.column, each_tile.row)
            game_state.screen.blit(art.radius_tile_image_1, [x + background_x_middle, y + background_top])
        game_state.screen.blit(art.selected_tile_image, [game_state.selected_construct.tile_x + background_left,
                                                         game_state.selected_construct.tile_y + background_top])
    game_state.screen.blit(active_map.terrain_display_layer.image, [background_left,
                                                                    background_top])
    game_state.screen.blit(active_map.building_display_layer.image, [background_left,
                                                                     background_top])
    print_stats(game_state, game_state.selected_construct)
    if game_state.build_menu:
        print_build_menu(game_state)
    if game_state.remove:
        print_remove(game_state)
    pygame.display.flip()


def input_processing(game_state, selected_tile, background_left, background_top, background_right, background_bottom, background_x_middle, mouse_pos):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            print(game_state.victory_points)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state.build_menu and game_state.build_candidate:
                game_state.selected_construct = None
                build(game_state, selected_tile, background_left, background_top, background_right, background_bottom, mouse_pos)
            if game_state.remove:
                remove(game_state, selected_tile)
            elif not game_state.build_menu and not game_state.remove:
                game_state.selected_construct = selected_tile.construct
        elif event.type == pygame.KEYDOWN:
            key_functions.get(event.key, do_nothing)(game_state)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                game_state.control = False


def place_palace(game_state, background_width, background_height):
    active_map = game_state.active_map
    palace_placed = False
    game_state.build_menu = True
    while not palace_placed:
        game_state.build_candidate = "Palace"
        game_state.time += 1
        background_left = game_state.active_map.x_shift
        background_top = game_state.active_map.y_shift
        background_x_middle = 20 + (background_left + background_width / 2)
        background_bottom = (background_top + background_height)
        background_right = (background_left + background_width)
        mouse_pos = pygame.mouse.get_pos()
        map_xy = utilities.get_map_coords(mouse_pos,
                                          game_state.active_map.x_shift,
                                          game_state.active_map.y_shift,
                                          background_x_middle)

        selected_tile = None
        if 0 <= map_xy[0] <= active_map.width - 1 and 0 <= map_xy[1] <= active_map.height - 1:
            selected_tile = active_map.game_tile_rows[map_xy[1]][map_xy[0]]
        input_processing(game_state, selected_tile, background_left, background_top,
                         background_right, background_bottom, background_x_middle, mouse_pos)

        update_display(game_state, selected_tile, background_left, background_top,
                       background_right, background_bottom, background_x_middle, mouse_pos)
        palace_placement_message = tiny_font.render("Please choose a location for your palace!", True, utilities.colors.white)
        game_state.screen.blit(palace_placement_message, [(game_state.screen.get_width() / 2) - (palace_placement_message.get_width() / 2), 100])
        pygame.display.flip()

        game_state.clock.tick(60)
        if game_state.resources["Labor"] < 1000:
            palace_placed = True
    game_state.build_menu = False
    game_state.build_candidate = "House"


def main(game_state):
    active_map = game_state.active_map

    done = False

    background_width = game_state.active_map.tile_display_layer.image.get_width()
    background_height = game_state.active_map.tile_display_layer.image.get_height()
    active_map.x_shift = game_state.screen_width / 2 - background_width / 2
    active_map.y_shift = game_state.screen_height / 2 - (background_height / 2)
    game_state.year = 1000
    game_state.victory_points = 0
    game_state.selected_construct = None

    place_palace(game_state, background_width, background_height)
    while not done:
        game_state.time += 1
        background_left = game_state.active_map.x_shift
        background_top = game_state.active_map.y_shift
        background_x_middle = 20 + (background_left + background_width / 2)
        background_bottom = (background_top + background_height)
        background_right = (background_left + background_width)
        mouse_pos = pygame.mouse.get_pos()
        map_xy = utilities.get_map_coords(mouse_pos,
                                          game_state.active_map.x_shift,
                                          game_state.active_map.y_shift,
                                          background_x_middle)

        selected_tile = None
        if 0 <= map_xy[0] <= active_map.width - 1 and 0 <= map_xy[1] <= active_map.height - 1:
            selected_tile = active_map.game_tile_rows[map_xy[1]][map_xy[0]]
        input_processing(game_state, selected_tile, background_left, background_top,
                         background_right, background_bottom, background_x_middle, mouse_pos)

        game_state.calendar.increment_date(game_state.game_speed)
        game_state.unit_processing()

        update_display(game_state, selected_tile, background_left, background_top,
                       background_right, background_bottom, background_x_middle, mouse_pos)

        game_state.clock.tick(60)
        game_state.time += 1


screen_width = 800
screen_height = 600

game_state = state.GameState(screen_width, screen_height)


game_state.active_map = game_map.Map((125, 125), (screen_width, screen_height))
game_state.active_map.map_generation()
main(game_state)
