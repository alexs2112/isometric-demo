import pygame, sys
import world_builder
from fov import FieldOfView
from tileset import TileSet
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
  world = create_world(args)
  create_creatures(world, screen.tileset)
  active = world.get_active_creature()
  screen.center_offset_on_creature(active)

  running = True
  while running:
    screen.display.fill((0,0,0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x, mouse_y = get_mouse_tile(screen.offset_x, screen.offset_y, mouse_x, mouse_y)
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == MOUSEBUTTONDOWN:
        c = world.get_creature_at_location(mouse_x, mouse_y)
        path = active.get_path_to(mouse_x, mouse_y)
        if c:
          path = path[:-1]
        active.move_along_path(path)
        if c:
          active.attack_creature(c)
      if event.type == KEYDOWN:
        if event.key == K_SPACE:
          active = world.get_next_active_creature()
          screen.center_offset_on_creature(active)
        if event.key == K_ESCAPE:
          running = False

    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
      screen.offset_x += 15
    if keys[K_LEFT]:
      screen.offset_x -= 15
    if keys[K_UP]:
      screen.offset_y -= 15
    if keys[K_DOWN]:
      screen.offset_y += 15

    draw_world(screen, world)
    draw_path_to_mouse(screen, world, active, mouse_x, mouse_y)
    draw_interface(screen, active)
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

  if '-v' in args:
    world.print_world()
  
  return world

def create_creatures(world, tileset):
  image_ids = [
    'Edward', 'Goobert', 'Wizard', 'Harold'
  ]

  for i in range(4):
    start_x, start_y = world.get_floor_coordinate()
    name = image_ids[i]
    icon = tileset.get_creature(name)
    creature = Creature(name, icon, world)
    creature.set_stats(max_hp=10, attack=3)
    creature.set_misc_stats(max_ap=3, speed=3, vision_radius=5)
    creature.move_to(start_x, start_y)
    world.add_creature(creature)
    world.update_fov(creature)

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
   - Spacebar to control next creature
   - Left click to move
   - Escape to exit""")
  sys.exit(0)

if __name__ == "__main__":
  start()
