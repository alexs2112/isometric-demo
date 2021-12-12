import pygame
import world_builder, creature

# Load the necessary images
TILE_FLOOR = pygame.image.load("assets/floors/floor_01.png")
TILE_WALL_NE = pygame.image.load("assets/walls/wall_ne_01.png")
TILE_WALL_NW = pygame.image.load("assets/walls/wall_nw_01.png")
TILE_CORNER= pygame.image.load("assets/walls/corner_01.png")

def initialize_screen(width, height):
  screen = pygame.display.set_mode((width, height))
  return screen

def draw_world(screen_width, screen, world, player):
  width, height = world_builder.world_dimensions(world)
  for x in range(width):
    for y in range(height):
      if not player.has_seen(x, y):
        continue

      if world[x][y] == world_builder.FLOOR:
        screen.blit(TILE_FLOOR, (get_isometric_position(screen_width, x * 32, y * 32)))
        if x == player.x and y == player.y:
          p_x, p_y = get_isometric_position(screen_width, x * 32, y * 32)
          screen.blit(player.icon, (p_x + 16, p_y - 16))
        continue
      
      # These need to be if statements in case its both NW and NE wall (corners)
      nw_wall = is_nw_wall(world,x, y)
      ne_wall = is_ne_wall(world, x, y)
      iso_x, iso_y = get_isometric_position(screen_width, x * 32, y * 32)
      if is_outer_corner(world, x, y):
        corner_x, corner_y = get_isometric_position(screen_width, x * 32 + 4, y * 32 - 20)
        screen.blit(TILE_CORNER, (corner_x, corner_y))
      if nw_wall:
        screen.blit(TILE_WALL_NW, (iso_x + 32 - 8, iso_y - 16 - 4))
      if ne_wall:
        screen.blit(TILE_WALL_NE, (iso_x, iso_y - 16 - 4))
      if nw_wall and ne_wall:
        corner_x, corner_y = get_isometric_position(screen_width, x * 32 + 4, y * 32 - 20)
        screen.blit(TILE_CORNER, (corner_x, corner_y))

def is_nw_wall(world, x, y):
  width, _ = world_builder.world_dimensions(world)
  if x >= width - 1 or x < 0:
    return False
  return world[x][y] == world_builder.WALL and world[x+1][y] == world_builder.FLOOR

def is_ne_wall(world, x, y):
  _, height = world_builder.world_dimensions(world)
  if y >= height-1 or y < 0:
    return False
  return world[x][y] == world_builder.WALL and world[x][y+1] == world_builder.FLOOR

def is_outer_corner(world, x, y):
  width, height = world_builder.world_dimensions(world)
  if y < height - 1 and x < width - 1:
    if world[x][y] == world_builder.WALL and world[x+1][y+1] == world_builder.FLOOR:
      if world[x+1][y] == world_builder.WALL and world[x][y+1] == world_builder.WALL:
        return True
  return False

# Convert cartesian x and y coordinates to what their x and y should be when drawn to the screen
def get_isometric_position(screen_width, cart_x, cart_y):
  return int(screen_width/2) + cart_x - cart_y, int((cart_x + cart_y) / 2)

# Convert isometric x and y on the screen to their cartesian equivalent
def get_cartesian_position(screen_width, iso_x, iso_y):
  return (2 * iso_y + iso_x) / 2 - int(screen_width/2), (2 * iso_y - iso_x) / 2

