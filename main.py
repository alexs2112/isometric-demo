import pygame, sys, random
import world.world_builder as world_builder
from creatures.creature_factory import CreatureFactory
from screens.main_graphics import *
from helpers import *
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_RETURN,
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
  creature_factory = CreatureFactory(world, screen.tileset)
  create_creatures(world, creature_factory)
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
          screen.center_offset_on_creature(active)
        if event.key == K_RETURN:
          active = take_turns(world)
          if active:
            screen.center_offset_on_creature(active)
          else:
            # Once we have more functional screens, we will want a game over screen here instead of a force quit
            print("You Lose!")
            pygame.quit()
            sys.exit()
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
    draw_path_to_mouse(screen, active, mouse_x, mouse_y)
    draw_interface(screen, active)
    pygame.display.update()
    pygame.time.delay(FRAME_DELAY)

# Move to the next active creature and keep taking their turn until it is a human player
def take_turns(world: world_builder.World):
  while len(world.creatures) > 0:
    if len(world.players) == 0:
      return None
    active = world.get_next_active_creature()
    active.take_turn()
    if not active.ai:
      return active

def create_world(args):
  world_width = 30
  world_height = 40
  if "--small" in args:
    world_width = 25
    world_height = 25

  if "--no_paths" in args:
    world = world_builder.place_rooms(6, world_width, world_height)
  elif "--maze" in args:
    world = world_builder.generate_maze(world_width, world_height)
  elif "--no_walls" in args:
    world = world_builder.only_floors(world_width, world_height)
  else: # Default to --dungeon
    world = world_builder.generate_dungeon(world_width, world_height, 15)

  if '-v' in args:
    world.print_world()
  
  return world

def create_players(world: world_builder.World, cf: CreatureFactory):
  if world.start_room:
    room = world.start_room
  elif world.rooms:
    room = random.choice(world.rooms)
  else:
    room = None

  if '--solo' in sys.argv:
    player_num = 1
  else:
    player_num = 4
  for i in range(player_num):
    if room:
      x, y = world.get_random_floor_in_room(room)
    else:
      x, y = world.get_floor_coordinate()
    if i == 0:
      cf.new_edward(x,y)
    elif i == 1:
      cf.new_goobert(x,y)
    elif i == 2:
      cf.new_wizard(x,y)
    elif i == 3:
      cf.new_harold(x,y)

def create_creatures(world: world_builder.World, cf: CreatureFactory):
  create_players(world, cf)
  for room in world.rooms:
    if room == world.start_room:
      continue

    for _ in range(3):
      x, y = world.get_random_floor_in_room(room)
      if random.random() < 0.5:
        c = cf.new_mushroom(x,y)
      else:
        c = cf.new_skeleton(x,y)
      c.set_home_room(room)

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
    -v
    --solo
  
  World Types:
    --dungeon           (default)
    --small
    --maze
    --no_paths
    --no_walls
    
  Controls:
   - Arrow keys to scroll the screen
   - Spacebar to center screen on active player
   - Enter to end turn
   - Left click to move and attack
   - Escape to exit""")
  sys.exit(0)

if __name__ == "__main__":
  start()
