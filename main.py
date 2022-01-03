import pygame, sys
import init
from screens.subscreen import GameOverScreen, StartScreen
from screens.map_screen import MapScreen
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
    K_m,
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
  world = init.create_world(args)
  messages = [] # Keep track of all the notifications each turn
  creature_factory = CreatureFactory(world, screen.tileset)
  init.create_creatures(world, creature_factory, messages)
  active = world.get_active_creature()
  screen.center_offset_on_creature(active)
  subscreen = StartScreen()

  running = True
  while running:
    screen.clear()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    tile_x, tile_y = get_mouse_tile(screen.offset_x, screen.offset_y, mouse_x, mouse_y)

    if subscreen:
      subscreen.draw(screen)
      subscreen = subscreen.respond_to_events(pygame.event.get())

      # If we move from a subscreen back to main, refocus on the active player
      if not subscreen:
        screen.center_offset_on_creature(active)
    else:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit(0)
        if event.type == MOUSEBUTTONDOWN:
          c = world.get_creature_at_location(tile_x, tile_y)
          path = active.get_path_to(tile_x, tile_y)
          if c:
            path = path[:-1]
          active.move_along_path(path)
          if c:
            active.attack_creature(c)
        if event.type == KEYDOWN:
          if event.key == K_SPACE:
            screen.center_offset_on_creature(active)
          elif event.key == K_RETURN:
            active = take_turns(world, messages)
            if active:
              screen.center_offset_on_creature(active)
            else:
              subscreen = GameOverScreen()
          elif event.key == K_ESCAPE:
            running = False
          elif event.key == K_m:
            messages.clear()
            subscreen = MapScreen(world, screen, active)

      # Not sure if we need to be able to scroll anymore
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
      path = draw_path_to_mouse(screen, active, tile_x, tile_y)
      draw_interface(screen, active, path)
      display_messages(screen, messages)

    pygame.display.update()
    pygame.time.delay(FRAME_DELAY)

# Move to the next active creature and keep taking their turn until it is a human player
def take_turns(world: world_builder.World, messages):
  messages.clear()
  while len(world.creatures) > 0:
    if len(world.players) == 0:
      return None
    active = world.get_next_active_creature()
    active.take_turn()
    if active.is_player():
      return active

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
   - M to show the map view to travel and rest
   - Escape to exit""")
  sys.exit(0)

if __name__ == "__main__":
  start()
