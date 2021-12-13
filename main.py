import pygame, sys
import world_builder
import tile
from creature import *
from graphics import *
from helpers import *
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT
)

# How long (in milliseconds) between each frame
FRAME_DELAY = 100

# Dimensions of the screen in pixels
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

# Run the main game loop
def main(args):
  screen = initialize_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
  tileset = tile.TileSet()
  world = create_world(args)
  player = create_player(args, world)
  offset_x, offset_y = center_offset_on_player(player)

  running = True
  while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cart_x, cart_y = get_clicked_tile(offset_x, offset_y, mouse_x, mouse_y)
        player.move_to(world, cart_x, cart_y)
      if event.type == KEYDOWN:
        if event.key == K_SPACE:
          offset_x, offset_y = center_offset_on_player(player)
        if event.key == K_ESCAPE:
          running = False

    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
      offset_x += 15
    if keys[K_LEFT]:
      offset_x -= 15
    if keys[K_UP]:
      offset_y -= 15
    if keys[K_DOWN]:
      offset_y += 15

    draw_world(offset_x, offset_y, screen, tileset, world, player)
    pygame.display.update()
    pygame.time.delay(FRAME_DELAY)

def create_world(args):
  world_width = 30
  world_height = 40

  if "--no_paths" in args:
    world = world_builder.place_rooms(6, world_width, world_height)
  elif "--maze" in args:
    world = world_builder.generate_maze(world_width, world_height)
  elif "--no_walls" in args:
    world = world_builder.only_floors(world_width, world_height)
  else: # Default to --dungeon
    world = world_builder.generate_dungeon(world_width, world_height, 90)
  world.print_world()
  
  return world

def create_player(args, world):
  start_x, start_y = world.get_floor_coordinate()
  player_icon = pygame.image.load("assets/player.png")
  player = Creature(start_x, start_y, player_icon, 5)
  player.initialize_fov(world)
  return player

def center_offset_on_player(player):
  offset_x, offset_y = get_tile_position((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2), player.x * 32, player.y * 32)
  return offset_x + 32, offset_y

def start():
  args = sys.argv
  if "--help" in args or "-h" in args:
    print_help()

  pygame.init()
  pygame.display.set_caption('Isometric Demo')
  main(args)

def print_help():
  print("""Isometric Prototype
  Options:
    -h, --help
  
  World Types:
    --dungeon           (default)
    --maze
    --no_paths
    --no_walls
    
  Controls:
   - Arrow keys to scroll the screen
   - Spacebar to center screen on player
   - Left click to move
   - Escape to exit""")
  sys.exit(0)

if __name__ == "__main__":
  start()
