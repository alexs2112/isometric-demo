import pygame
from creature import Creature
from world_builder import World
from screen import Screen
from tileset import TileSet
from helpers import get_tile_position

def initialize_screen(width, height):
  tileset = TileSet()
  display = pygame.display.set_mode((width, height))
  return Screen(width, height, display, tileset)

def draw_interface(screen, active: Creature):
  line_base = 40
  line_height = 36
  line = 0
  move_string = "AP: " + str(active.ap) + "/" + str(active.max_ap)
  if active.free_movement > 0:
    move_string += " [" + str(active.free_movement) + "]"
  elif active.ap == 0:
    move_string += " (Press ENTER to end turn)"
  screen.write(move_string, (12, screen.height - line_base - line_height * line), screen.tileset.get_font())

  line += 1
  hp_string = "HP: " + str(active.hp) + "/" + str(active.max_hp)
  screen.write(hp_string, (12, screen.height - line_base - line_height * line), screen.tileset.get_font())

  line += 1
  screen.write(active.name + "'s Turn", (12, screen.height - line_base - line_height * line), screen.tileset.get_font())

def draw_world(screen, world: World):
  width, height = world.dimensions()
  creature_locations = world.creature_location_dict()
  for x in range(width):
    for y in range(height):
      if not world.has_seen(x,y):
        continue
      sx, sy = get_tile_position(screen.offset_x, screen.offset_y, x * 32, y * 32)
      if sx < -96 or sy < -64 or sx > screen.width or sy > screen.height:
        continue

      tileset_id = world.tile(x,y).tileset_id

      if world.is_floor(x,y):
        screen.blit(screen.tileset.get_floor(tileset_id), (get_tile_position(screen.offset_x, screen.offset_y, x * 32, y * 32)))
        if (x,y) in creature_locations:
          creature = creature_locations[(x,y)]
          p_x, p_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32, y * 32)
          screen.blit(creature.icon, (p_x + 16, p_y - 16))
          healthbar = get_healthbar(screen.tileset, creature)
          if healthbar:
            screen.blit(healthbar, (p_x + 16, p_y + 16))
        continue

      # These need to be if statements in case its both NW and NE wall (corners)
      nw_wall = is_nw_wall(world, x, y)
      ne_wall = is_ne_wall(world, x, y)
      iso_x, iso_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32, y * 32)
      if is_outer_corner(world, x, y):
        corner_x, corner_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32 + 4, y * 32 - 20)
        screen.blit(screen.tileset.get_corner(tileset_id), (corner_x, corner_y))
      if nw_wall:
        screen.blit(screen.tileset.get_nw_wall(tileset_id), (iso_x + 32 - 8, iso_y - 16 - 4))
      if ne_wall:
        screen.blit(screen.tileset.get_ne_wall(tileset_id), (iso_x, iso_y - 16 - 4))
      if nw_wall and ne_wall:
        corner_x, corner_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32 + 4, y * 32 - 20)
        screen.blit(screen.tileset.get_corner(tileset_id), (corner_x, corner_y))
      # We probably want to handle corners on the left and right so that it looks like a corner when only one wall is shown
      # This might be a massive pain in the ass to how we are drawing walls, maybe redo it

# Use the logic above to simply calculate the offset and position, then blit the tile.image to the screen
def is_nw_wall(world: World, x, y):
  width, _ = world.dimensions()
  if x >= width - 1 or x < 0:
    return False
  return world.is_wall(x,y) and world.is_floor(x+1,y)

def is_ne_wall(world: World, x, y):
  _, height = world.dimensions()
  if y >= height-1 or y < 0:
    return False
  return world.is_wall(x,y) and world.is_floor(x,y+1)

def is_outer_corner(world: World, x, y):
  width, height = world.dimensions()
  if y < height - 1 and x < width - 1:
    if world.is_wall(x,y) and world.is_floor(x+1,y+1):
      if world.is_wall(x+1,y) and world.is_wall(x,y+1):
        return True
  return False

def get_healthbar(tileset: TileSet, creature: Creature):
  quarter = creature.max_hp / 4
  if creature.hp == creature.max_hp:
    return None
  elif creature.hp > 3 * quarter:
    return tileset.get_ui("health_full")
  elif creature.hp > 2 * quarter:
    return tileset.get_ui("health_most")
  elif creature.hp > quarter:
    return tileset.get_ui("health_half")
  else:
    return tileset.get_ui("health_quarter")

highlight = pygame.image.load("assets/floor_highlights.png")
def draw_path_to_mouse(screen, creature, x, y):
  path = creature.get_path_to(x, y)[:creature.get_possible_distance()]
  for tile in path:
    tile_x, tile_y = tile
    iso_x, iso_y = get_tile_position(screen.offset_x, screen.offset_y, tile_x * 32, tile_y * 32)
    screen.blit(highlight, (iso_x, iso_y))
