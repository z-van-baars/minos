import pygame
import utilities
import game_map
import art
import construct
import state

pygame.init()
pygame.display.set_mode([0, 0])



def build(game_state, selected_tile, background_left, background_top, background_right, background_bottom, mouse_pos):
    if utilities.check_if_inside(background_left,
                                 background_right,
                                 background_top,
                                 background_bottom,
                                 mouse_pos):
        if selected_tile is not None and selected_tile.construct is None:
            print("open")
            print("Mouse Click Event at: {0}, {1}".format(selected_tile.column, selected_tile.row))
            new_lumber_camp = construct.LumberCamp(selected_tile.column, selected_tile.row)
            game_state.active_map.terrain.append(new_lumber_camp)
            game_state.active_map.game_tile_rows[selected_tile.row][selected_tile.column].construct = new_lumber_camp
            game_state.active_map.paint_resources()
            game_state.active_map.paint_buildings()
        else:
            print("blocked")


def do_nothing(game_state):
    pass


def b_key(game_state):
    game_state.build_menu = True


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
                 pygame.K_RIGHT: right_key}


def main(game_state):
    active_map = game_state.active_map
    tiny_font = pygame.font.SysFont('Calibri', 11, True, False)
    small_font = pygame.font.SysFont('Calibri', 14, True, False)

    done = False

    background_width = game_state.active_map.tile_display_layer.image.get_width()
    background_height = game_state.active_map.tile_display_layer.image.get_height()
    active_map.x_shift = game_state.screen_width / 2 - background_width / 2
    active_map.y_shift = game_state.screen_height / 2 - (background_height / 2)
    game_state.year = 1000


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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                build(game_state, selected_tile, background_left, background_top, background_right, background_bottom, mouse_pos)
            elif event.type == pygame.KEYDOWN:
                key_functions.get(event.key, do_nothing)(game_state)




        game_state.calendar.increment_date(game_state.game_speed)

        game_state.screen.fill(utilities.colors.background_blue)
        game_state.screen.blit(active_map.tile_display_layer.image, [background_left,
                                                                     background_top])
        if selected_tile is not None:
            selected_coords = utilities.get_screen_coords(selected_tile.column,
                                                          selected_tile.row)
            game_state.screen.blit(art.selected_tile_image, [selected_coords[0] + background_x_middle, selected_coords[1] + background_top])
        game_state.screen.blit(active_map.terrain_display_layer.image, [background_left,
                                                                        background_top])
        game_state.screen.blit(active_map.building_display_layer.image, [background_left,
                                                                         background_top])


        pygame.display.flip()
        game_state.clock.tick(60)
        game_state.time += 1




screen_width = 800
screen_height = 600

game_state = state.GameState(screen_width, screen_height)


game_state.active_map = game_map.Map((40, 40), (screen_width, screen_height))
game_state.active_map.map_generation()
main(game_state)
