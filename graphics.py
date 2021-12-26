import pygame
from pathfinder import Path
from helpers import get_tile_position
from main import SCREEN_WIDTH, SCREEN_HEIGHT

def initialize_screen(width, height):
  screen = pygame.display.set_mode((width, height))
  return screen

def draw_world(offset_x, offset_y, screen, tileset, world, player):
  width, height = world.dimensions()
  for x in range(width):
    for y in range(height):
      if not player.has_seen(x, y):
        continue
      sx, sy = get_tile_position(offset_x, offset_y, x * 32, y * 32)
      if sx < -96 or sy < -64 or sx > SCREEN_WIDTH or sy > SCREEN_HEIGHT:
        continue

      tileset_id = world.tile(x,y).tileset_id

      if world.is_floor(x,y):
        screen.blit(tileset.get_floor(tileset_id), (get_tile_position(offset_x, offset_y, x * 32, y * 32)))
        if x == player.x and y == player.y:
          p_x, p_y = get_tile_position(offset_x, offset_y, x * 32, y * 32)
          screen.blit(player.icon, (p_x + 16, p_y - 16))
        continue

      # These need to be if statements in case its both NW and NE wall (corners)
      nw_wall = is_nw_wall(world, x, y)
      ne_wall = is_ne_wall(world, x, y)
      iso_x, iso_y = get_tile_position(offset_x, offset_y, x * 32, y * 32)
      if is_outer_corner(world, x, y):
        corner_x, corner_y = get_tile_position(offset_x, offset_y, x * 32 + 4, y * 32 - 20)
        screen.blit(tileset.get_corner(tileset_id), (corner_x, corner_y))
      if nw_wall:
        screen.blit(tileset.get_nw_wall(tileset_id), (iso_x + 32 - 8, iso_y - 16 - 4))
      if ne_wall:
        screen.blit(tileset.get_ne_wall(tileset_id), (iso_x, iso_y - 16 - 4))
      if nw_wall and ne_wall:
        corner_x, corner_y = get_tile_position(offset_x, offset_y, x * 32 + 4, y * 32 - 20)
        screen.blit(tileset.get_corner(tileset_id), (corner_x, corner_y))
      # We probably want to handle corners on the left and right so that it looks like a corner when only one wall is shown
      # This might be a massive pain in the ass to how we are drawing walls, maybe redo it

# Use the logic above to simply calculate the offset and position, then blit the tile.image to the screen
def is_nw_wall(world, x, y):
  width, _ = world.dimensions()
  if x >= width - 1 or x < 0:
    return False
  return world.is_wall(x,y) and world.is_floor(x+1,y)

def is_ne_wall(world, x, y):
  _, height = world.dimensions()
  if y >= height-1 or y < 0:
    return False
  return world.is_wall(x,y) and world.is_floor(x,y+1)

def is_outer_corner(world, x, y):
  width, height = world.dimensions()
  if y < height - 1 and x < width - 1:
    if world.is_wall(x,y) and world.is_floor(x+1,y+1):
      if world.is_wall(x+1,y) and world.is_wall(x,y+1):
        return True
  return False

highlight = pygame.image.load("assets/floor_highlights.png")
def draw_path_to_mouse(offset_x, offset_y, screen, world, player, x, y):
  if world.outside_world(x,y) or not (player.has_seen(x,y) and world.is_floor(x,y)):
    return

  path = Path(world, player.x, player.y, x, y).points
  
  # Temporary limitation on the length of the line
  for tile in path:
    tile_x, tile_y = tile
    iso_x, iso_y = get_tile_position(offset_x, offset_y, tile_x * 32, tile_y * 32)
    screen.blit(highlight, (iso_x, iso_y))
