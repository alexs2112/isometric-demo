import pygame, sys
import init
from items.inventory import Inventory
from items.item_factory import ItemFactory
from screens.spell_screen import SpellScreen
from spells.effect_factory import EffectFactory
from spells.spell_factory import SpellFactory
from screens.help_screen import HelpScreen
from screens.inventory_screen import InventoryScreen
from screens.party_screen import PartyScreen
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
    K_m, K_i, K_s, K_h, K_g, K_p,
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
    self.effect_factory = EffectFactory()
    self.spell_factory = SpellFactory(self.effect_factory)
    self.item_factory = ItemFactory(self.world, self.screen.tileset, self.effect_factory, self.spell_factory)
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
            # If we are casting a spell
            if active.loaded_spell:
              self.cast_loaded_spell(active, tile_x, tile_y)

            # If we click a creature in range:
            elif self.world.get_creature_at_location(tile_x, tile_y):
              _, target = active.get_attack_line(tile_x, tile_y)
              self.attack_target(active, target)

            # If we click an inventory and there are no active enemies
            elif self.world.get_inventory(tile_x, tile_y) and self.world.no_active_enemies():
              self.loot_inventory_at(tile_x, tile_y)

            # Otherwise, draw a path and move along it
            else:
              path = active.get_path_to(tile_x, tile_y)
              active.move_along_path(path)
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
              if active.loaded_spell:
                active.loaded_spell = None
              else:
                # Preferably open a game menu here instead of just ending the game lol
                running = False
            elif event.key == K_m:
              self.messages.clear()
              self.subscreen = MapScreen(self.world, self.screen, active)
            elif event.key == K_i:
              self.subscreen = InventoryScreen(self.world.players)
            elif event.key == K_p:
              self.subscreen = PartyScreen(self.world.players)
            elif event.key == K_h:
              self.subscreen = HelpScreen()
            elif event.key == K_g:
              i = Inventory()
              i.add_item(self.item_factory.wizard_hat())
              self.subscreen = InventoryScreen(self.world.players, i)
            elif event.key == K_s:
              if active.get_spells():
                self.subscreen = SpellScreen(active)
              else:
                active.notify(active.name + " has no spells to cast.")

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
        if active.loaded_spell:
          highlight_ability_target(self.screen, active, tile_x, tile_y)
          path = None
          target = None
        else:
          path, target = draw_path_to_mouse(self.screen, active, tile_x, tile_y)
        draw_player_stats(self.screen, active, path, target)
        show_mouse_tooltips(self.screen, self.world, mouse_x, mouse_y, tile_x, tile_y)
        display_messages(self.screen, self.messages)
        write_active_player(self.screen, active)

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
  
  def cast_loaded_spell(self, active: Creature, tile_x, tile_y):
    tiles = active.loaded_spell.get_target_tiles(active.x, active.y, tile_x, tile_y)
    if not tiles:
      return
    creatures = self.world.creature_location_dict()
    targets = []
    for t in tiles:
      if t in creatures:
        c = creatures[t]
        if not active.loaded_spell.friendly_fire:
          if c.faction == active.faction:
            continue
        targets.append(creatures[t])
    active.loaded_spell.cast(active, targets)
    active.loaded_spell = None

  def attack_target(self, active: Creature, target: Creature):
    active.attack_creature(target)

  def loot_inventory_at(self, tile_x, tile_y):
    self.subscreen = InventoryScreen(self.players, self.world.get_inventory(tile_x, tile_y))
    
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
