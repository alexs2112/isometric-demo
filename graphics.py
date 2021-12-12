import pygame

# Load the necessary images
TILE_FLOOR = pygame.image.load("assets/floors/floor_01.png")
TILE_WALL_NE = pygame.image.load("assets/walls/wall_ne_01.png")
TILE_WALL_NW = pygame.image.load("assets/walls/wall_nw_01.png")
TILE_CORNER= pygame.image.load("assets/walls/corner_01.png")

def initialize_screen(width, height):
  screen = pygame.display.set_mode((width, height))
  return screen

def draw_world(screen_width, screen, world, player):
  width, height = world.dimensions()
  for x in range(width):
    for y in range(height):
      if not player.has_seen(x, y):
        continue

      if world.is_floor(x,y):
        screen.blit(TILE_FLOOR, (get_isometric_position(screen_width, x * 32, y * 32)))
        if x == player.x and y == player.y:
          p_x, p_y = get_isometric_position(screen_width, x * 32, y * 32)
          screen.blit(player.icon, (p_x + 16, p_y - 16))
        continue

      # These need to be if statements in case its both NW and NE wall (corners)
      nw_wall = is_nw_wall(world, x, y)
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
      # We probably want to handle corners on the left and right so that it looks like a corner when only one wall is shown
      # This might be a massive pain in the ass to how we are drawing walls, maybe redo it

# Lets move these to the Tile class when we do that
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

# Convert cartesian x and y coordinates to what their x and y should be when drawn to the screen
def get_isometric_position(screen_width, cart_x, cart_y):
  return int(screen_width/2) + cart_x - cart_y, int((cart_x + cart_y) / 2)

# Convert isometric x and y on the screen to their cartesian equivalent
def get_cartesian_position(screen_width, iso_x, iso_y):
  return (2 * iso_y + iso_x) / 2 - int(screen_width/2), (2 * iso_y - iso_x) / 2
