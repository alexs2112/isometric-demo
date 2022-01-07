import pygame, sys
import init
from items.inventory import Inventory
from items.item_factory import ItemFactory
from screens.help_screen import HelpScreen
from screens.inventory_screen import InventoryScreen
from screens.stats_screen import StatsScreen
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
    K_m, K_i, K_s, K_h, K_g, K_q,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT
)

# How long (in milliseconds) between each frame
FRAME_DELAY = 100

# Dimensions of the screen in pixels
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

class Game:
  def __init__(self, args):
    self.args = args
    self.screen = initialize_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    self.world = init.create_world(args)
    self.messages = [] # Keep track of all the notifications each turn
    self.item_factory = ItemFactory(self.world, self.screen.tileset)
    self.creature_factory = CreatureFactory(self.world, self.screen.tileset, self.item_factory)
    init.create_creatures(self.world, self.creature_factory, self.messages)
    init.create_items(self.world, self.item_factory)
    self.subscreen = StartScreen()

  # Run the main game loop
  def main(self):
    running = True
    active: Creature = self.world.get_active_creature()
    self.screen.center_offset_on_creature(active)
    while running:
      self.screen.clear()
      mouse_x, mouse_y = pygame.mouse.get_pos()
      tile_x, tile_y = get_mouse_tile(self.screen.offset_x, self.screen.offset_y, mouse_x, mouse_y)

      if self.subscreen:
        self.subscreen.draw(self.screen)
        self.subscreen = self.subscreen.respond_to_events(pygame.event.get())

        # If we move from a subscreen back to main, refocus on the active player
        if not self.subscreen:
          self.screen.center_offset_on_creature(active)
      else:
        for event in pygame.event.get():
          if event.type == QUIT:
            pygame.quit()
            sys.exit(0)

          if event.type == MOUSEBUTTONDOWN:
            c = self.world.get_creature_at_location(tile_x, tile_y)
            
            if self.world.no_active_enemies():
              i = self.world.get_inventory(tile_x, tile_y)
            else:
              i = None

            path = active.get_path_to(tile_x, tile_y)
            if c or i:
              path = path[:-1]
            active.move_along_path(path)
            if c:
              active.attack_creature(c)
            elif i:
              if abs(active.x - tile_x) <= 1 and abs(active.y - tile_y) <= 1:
                if self.world.no_active_enemies():
                  self.subscreen = InventoryScreen(self.world.players, i)
                else:
                  active.notify("There are active enemies!")

          if event.type == KEYDOWN:
            if event.key == K_SPACE:
              self.screen.center_offset_on_creature(active)
            elif event.key == K_RETURN:
              active = self.take_turns()
              if active:
                self.screen.center_offset_on_creature(active)
              else:
                self.subscreen = GameOverScreen()
            elif event.key == K_ESCAPE:
              running = False
            elif event.key == K_m:
              self.messages.clear()
              self.subscreen = MapScreen(self.world, self.screen, active)
            elif event.key == K_i:
              self.subscreen = InventoryScreen(self.world.players)
            elif event.key == K_s:
              self.subscreen = StatsScreen(self.world.players)
            elif event.key == K_h:
              self.subscreen = HelpScreen()
            elif event.key == K_g:
              i = Inventory()
              i.add_item(self.item_factory.wizard_hat())
              self.subscreen = InventoryScreen(self.world.players, i)
            elif event.key == K_q:
              potion = self.item_factory.potion_minor_healing()
              potion.consume(active)

        # Not sure if we need to be able to scroll anymore
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
          self.screen.offset_x += 15
        if keys[K_LEFT]:
          self.screen.offset_x -= 15
        if keys[K_UP]:
          self.screen.offset_y -= 15
        if keys[K_DOWN]:
          self.screen.offset_y += 15

        draw_world(self.screen, self.world)
        path = draw_path_to_mouse(self.screen, active, tile_x, tile_y)
        draw_interface(self.screen, active, path)
        show_mouse_tooltips(self.screen, self.world, mouse_x, mouse_y, tile_x, tile_y)
        display_messages(self.screen, self.messages)

      pygame.display.update()
      pygame.time.delay(FRAME_DELAY)

  # Move to the next active creature and keep taking their turn until it is a human player
  def take_turns(self):
    self.messages.clear()
    while len(self.world.creatures) > 0:
      if len(self.world.players) == 0:
        return None
      active = self.world.get_next_active_creature()
      active.take_turn()
      if active.is_player():
        return active

def start():
  args = sys.argv
  if "--help" in args or "-h" in args:
    print_help()

  pygame.init()
  pygame.display.set_caption('Isometric Demo')
  game = Game(args)
  game.main()

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
    
  Press [h] in game to view the controls""")
  sys.exit(0)

if __name__ == "__main__":
  start()
