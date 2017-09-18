import pygame
import math
import utilities
import state
import art


tiny_font = pygame.font.SysFont('Calibri', 11, True, False)
small_font = pygame.font.SysFont('Calibri', 14, True, False)


def print_stats(game_state, selected_construct):
    wood_stamp = tiny_font.render("Wood: {0} (-{1}) (+{2})".format(str(math.floor(game_state.resources["Wood"])),
                                                                   str(math.floor(game_state.last_step_consumed_resources["Wood"])),
                                                                   str(math.floor(game_state.last_step_produced_resources["Wood"]))),
                                  True, utilities.colors.white)
    food_stamp = tiny_font.render("Food: {0} (-{1}) (+{2})".format(str(math.floor(game_state.resources["Food"])),
                                                                   str(math.floor(game_state.last_step_consumed_resources["Food"])),
                                                                   str(math.floor(game_state.last_step_produced_resources["Food"]))),
                                  True, utilities.colors.white)
    stone_stamp = tiny_font.render("Stone: {0} (-{1}) (+{2})".format(str(math.floor(game_state.resources["Stone"])),
                                                                     str(math.floor(game_state.last_step_consumed_resources["Stone"])),
                                                                     str(math.floor(game_state.last_step_produced_resources["Stone"]))),
                                   True, utilities.colors.white)
    copper_stamp = tiny_font.render("Copper: {0} (-{1}) (+{2})".format(str(math.floor(game_state.resources["Copper"])),
                                                                       str(math.floor(game_state.last_step_consumed_resources["Copper"])),
                                                                       str(math.floor(game_state.last_step_produced_resources["Copper"]))),
                                    True, utilities.colors.white)
    labor_stamp = tiny_font.render("Labor: {0} (-{1}) (+{2})".format(str(math.floor(game_state.resources["Labor"])),
                                                                     str(math.floor(game_state.last_step_consumed_resources["Labor"])),
                                                                     str(math.floor(game_state.last_step_produced_resources["Labor"]))),
                                   True, utilities.colors.white)
    game_state.screen.blit(wood_stamp, [10, 10])
    game_state.screen.blit(food_stamp, [10, 21])
    game_state.screen.blit(stone_stamp, [10, 32])
    game_state.screen.blit(copper_stamp, [10, 43])
    game_state.screen.blit(labor_stamp, [10, 54])
    if selected_construct:
        selected_construct_stamp = small_font.render("{0}".format(selected_construct.display_name), True, utilities.colors.white)
        center_offset = selected_construct_stamp.get_width() / 2
        construct_display_x = game_state.screen.get_width() / 2 - center_offset
        construct_display_y = 10
        game_state.screen.blit(selected_construct_stamp, [construct_display_x, construct_display_y])
        construct_display_y += 14
        if selected_construct.active:
            active_state = "Active"
        else:
            active_state = "Inactive"
        game_state.screen.blit(tiny_font.render(active_state, True, utilities.colors.white), [construct_display_x, construct_display_y])
        for each_resource, each_value in selected_construct.raw_resources.items():
            if each_value > 0:
                construct_display_y += 11
                resource_stamp = tiny_font.render("{0}: {1}".format(each_resource, str(each_value)), True, utilities.colors.white)
                game_state.screen.blit(resource_stamp, [construct_display_x, construct_display_y])


def print_activate_menu(game_state):
    activate_margin = game_state.screen.get_height() - 80
    activate_stamp = tiny_font.render("Toggle Active / Deactive on left click: ", True, utilities.colors.white)
    game_state.screen.blit(activate_stamp, [10, activate_margin])


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
                                           math.floor(game_state.screen.get_height() - game_state.stats.resources["Wood"][step] / 5)])
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
    build_stamp_margin = game_state.screen.get_height() - 80
    build_stamp = tiny_font.render("Build:", True, utilities.colors.white)
    game_state.screen.blit(build_stamp, [10, build_stamp_margin])
    if game_state.build_candidate:
        candidate_stamp = tiny_font.render(game_state.build_candidate, True, utilities.colors.white)
        game_state.screen.blit(candidate_stamp, [40, build_stamp_margin])
        build_stamp_margin += 15
        game_state.screen.blit(tiny_font.render("Cost:", True, utilities.colors.white),
                               [10, build_stamp_margin])
        for each_resource, each_value in state.build_dict[game_state.build_candidate].cost.items():
            game_state.screen.blit(tiny_font.render("{0}: {1}".format(each_resource, each_value), True, utilities.colors.white),
                                   [40, build_stamp_margin])
            build_stamp_margin += 11


def print_build_line(game_state, selected_tile, background_left, background_top, background_x_middle):
    if not game_state.palace:
        return
    line_length = math.ceil(utilities.distance(game_state.palace.tile_x,
                                               game_state.palace.tile_y,
                                               selected_tile.column,
                                               selected_tile.row))
    line_color = utilities.colors.red
    if line_length < game_state.palace.radius + game_state.palace.radius_bonus:
        line_color = utilities.colors.light_green
    point_a = utilities.get_screen_coords(game_state.palace.tile_x, game_state.palace.tile_y)
    point_b = utilities.get_screen_coords(selected_tile.column, selected_tile.row)
    pygame.draw.line(game_state.screen,
                     line_color,
                     (point_a[0] + background_x_middle + 20, point_a[1] + background_top + 7),
                     (point_b[0] + background_x_middle + 20, point_b[1] + background_top + 7),
                     2)


def print_remove(game_state):
    remove_margin = game_state.screen.get_height() - 80
    remove_stamp = tiny_font.render("Remove: ", True, utilities.colors.white)
    game_state.screen.blit(remove_stamp, [10, remove_margin])


def update_display(game_state, selected_tile, background_left, background_top, background_right, background_bottom, background_x_middle, mouse_pos):
    active_map = game_state.active_map
    game_state.screen.fill(utilities.colors.background_blue)
    game_state.screen.blit(active_map.tile_display_layer.image, [background_left,
                                                                 background_top])
    if selected_tile is None:
        return
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
    if game_state.selected_construct and game_state.selected_construct.radius:
        radius_preview = utilities.get_nearby_tiles(active_map,
                                                    (game_state.selected_construct.tile_x, game_state.selected_construct.tile_y),
                                                    game_state.selected_construct.radius)
        for each_tile in radius_preview:
            x, y = utilities.get_screen_coords(each_tile.column, each_tile.row)
            game_state.screen.blit(art.radius_tile_image_1, [x + background_x_middle, y + background_top])
    if game_state.build_menu and selected_tile.construct:
        game_state.screen.blit(art.invalid_tile_image, [selected_coords[0] + background_x_middle, selected_coords[1] + background_top])
    else:
        game_state.screen.blit(art.selected_tile_image, [selected_coords[0] + background_x_middle, selected_coords[1] + background_top])
    game_state.screen.blit(active_map.terrain_display_layer.image, [background_left,
                                                                    background_top])
    game_state.screen.blit(active_map.building_display_layer.image, [background_left,
                                                                     background_top])
    print_stats(game_state, game_state.selected_construct)
    if game_state.build_menu:
        print_build_menu(game_state)
        print_build_line(game_state, selected_tile, background_left, background_top, background_x_middle)
    if game_state.remove:
        print_remove(game_state)
    if game_state.activation_mode:
        print_activate_menu(game_state)
    pygame.display.flip()
