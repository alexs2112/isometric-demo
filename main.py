import pygame, sys
import world_builder
import tile
from creature import *
from graphics import *
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
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

  # Temporary: Create the world based on the max size to fit on the screen using tiles that are 64x32
  world_width = int(SCREEN_WIDTH / 64)
  world_height = int(SCREEN_HEIGHT / 32)

  if "--no_paths" in args:
    world = world_builder.place_rooms(6, world_width, world_height)
  elif "--maze" in args:
    world = world_builder.generate_maze(world_width, world_height)
  else: # Default to --dungeon
    world = world_builder.generate_dungeon(world_width, world_height, 9)
  world.print_world()

  start_x, start_y = world.get_floor_coordinate()
  player_icon = pygame.image.load("assets/player.png")
  player = Creature(start_x, start_y, player_icon)
  player.initialize_fov(world)

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN:
        if event.key == K_RIGHT:
          player.move(world, 1, 0)
        if event.key == K_LEFT:
          player.move(world, -1, 0)
        if event.key == K_UP:
          player.move(world, 0, -1)
        if event.key == K_DOWN:
          player.move(world, 0, 1)
        if event.key == K_ESCAPE:
          running = False

    draw_world(SCREEN_WIDTH, screen, tileset, world, player)
    pygame.display.update()
    pygame.time.delay(FRAME_DELAY)

def start():
  args = sys.argv
  if "--help" in args or "-h" in args:
    print_help()

  pygame.init()
  pygame.display.set_caption('Isometric Demo')
  main(args)

def print_help():
  print("""Isometric Proof of Concept
  Options:
    -h, --help
  
  World Types:
    --dungeon           (default)
    --maze
    --no_paths""")
  sys.exit(0)

if __name__ == "__main__":
  start()
