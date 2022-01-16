import pygame, sys
import init
from items.inventory import Inventory
from items.item_factory import ItemFactory
from screens.spell_screen import SpellScreen
from spells.effect_factory import EffectFactory
from spells.spell_factory import SpellFactory
from creatures.creature_factory import CreatureFactory
from world.feature_factory import FeatureFactory
from screens.help_screen import HelpScreen
from screens.inventory_screen import InventoryScreen
from screens.party_screen import PartyScreen
from screens.subscreen import StartScreen
from screens.map_screen import MapScreen
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
    K_LSHIFT,
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

    self.feature_factory = FeatureFactory(self.screen.tileset)
    self.world = init.create_world(args, self.feature_factory)
    self.effect_factory = EffectFactory()
    self.spell_factory = SpellFactory(self.effect_factory)
    self.item_factory = ItemFactory(self.world, self.screen.tileset, self.effect_factory, self.spell_factory)
    self.creature_factory = CreatureFactory(self.world, self.screen.tileset, self.item_factory)

    self.messages = [] # Keep track of all the notifications each turn
    init.create_creatures(args, self.world, self.creature_factory, self.messages)
    init.create_items(self.world, self.item_factory)
    self.subscreen = StartScreen()

  # Run the main game loop
  def main(self):
    running = True
    active: Creature = self.world.players[0]
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
        keys = pygame.key.get_pressed()

        # If we are waiting for movement, or for AI
        if self.world.movement_in_progress():
          self.world.apply_next_move()
          self.screen.center_offset_on_creature(active)
        elif not active.is_player():
          done_turn = active.take_turn()
          self.screen.center_offset_on_creature(active)
          if done_turn:
            active = self.world.get_next_active_creature()
          while not self.world.can_see(active.x, active.y):
            done_turn = active.take_turn()
            print(done_turn)
            if done_turn:
              active = self.world.get_next_active_creature()
        else:
          # Take player input
          for event in pygame.event.get():
            if event.type == QUIT:
              pygame.quit()
              sys.exit(0)

            if event.type == MOUSEBUTTONDOWN:
              # If we are casting a spell
              if active.loaded_spell:
                self.cast_loaded_spell(active, tile_x, tile_y)

              # If we are in combat
              elif self.world.in_combat():
                c = self.world.get_creature_at_location(tile_x, tile_y)
                if c:
                  _, target = active.get_attack_line(tile_x, tile_y)
                  if target and active.ap >= active.get_attack_cost():
                    self.attack_target(active, target)
                  else:
                    path = active.get_path_to(tile_x, tile_y)
                    active.move_along_path(path[:-1])
                else:
                  path = active.get_path_to(tile_x, tile_y)
                  active.move_along_path(path)
              
              # If we aren't in combat
              else:
                c = self.world.get_creature_at_location(tile_x, tile_y)
                i = self.world.get_inventory(tile_x, tile_y)
                f = self.world.get_feature(tile_x, tile_y)

                if c:
                  if c.is_player():
                    active = c
                  else:
                    _, target = active.get_attack_line(tile_x, tile_y)
                    if target:
                      self.attack_target(active, target)
                    else:
                      path = active.get_path_to(tile_x, tile_y)
                      active.move_along_path(path[:-1])
                elif i:
                  if active.simple_distance_to(tile_x, tile_y) <= 1:
                    self.loot_inventory_at(tile_x, tile_y)
                  else:
                    path = active.get_path_to(tile_x, tile_y)
                    active.move_along_path(path[:-1])
                elif f:
                  if active.simple_distance_to(tile_x, tile_y) <= 1:
                    subscreen = f.interact(active)
                  else:
                    path = active.get_path_to(tile_x, tile_y)
                    active.move_along_path(path[:-1])
                else:
                  if keys[K_LSHIFT]:
                    start = active.x, active.y
                    path = active.get_path_to(tile_x, tile_y)
                    active.move_along_path_old(path)
                    end = active.x, active.y
                    self.move_party(active, start, end)
                  else:
                    path = active.get_path_to(tile_x, tile_y)
                    active.move_along_path(path)
              
                # At the end of a turn, if a combat has started during that turn reset active
                if self.world.in_combat():
                  active = self.world.get_current_active_creature()
                  if self.world.can_see(active.x, active.y):
                    self.screen.center_offset_on_creature(active)

            if event.type == KEYDOWN:
              if event.key == K_SPACE:
                self.screen.center_offset_on_creature(active)
              elif event.key == K_RETURN:
                self.messages.clear()
                if self.world.in_combat():
                  active = self.world.get_next_active_creature()
                  if self.world.can_see(active.x, active.y):
                    self.screen.center_offset_on_creature(active)
                else:
                  self.messages.clear()
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
                if active.spells:
                  self.subscreen = SpellScreen(active)
                else:
                  active.notify(active.name + " has no spells to cast.")
        # OUT OF FOR LOOP

        # Not sure if we need to be able to scroll anymore
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

        if active.is_player:
          draw_player_stats(self.screen, active, path, target)
        show_mouse_tooltips(self.screen, self.world, mouse_x, mouse_y, tile_x, tile_y)
        display_messages(self.screen, self.messages)
        write_active_player(self.screen, active)

      pygame.display.update()
      pygame.time.delay(FRAME_DELAY)

  # Move to the next active creature and keep taking their turn until it is a human player
  def take_turns(self):
    while len(self.world.creatures) > 0:
      if len(self.world.players) == 0:
        return None
      active = self.world.get_next_active_creature()
      active.take_turn()
      if active.is_player():
        self.screen.center_offset_on_creature(active)
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
    self.subscreen = InventoryScreen(self.world.players, self.world.get_inventory(tile_x, tile_y))

  def move_party(self, active, start, end):
    # If we arent in combat, we want the party to all follow the active player
    # Draw a 3x3 rectangle behind the player and randomly select tiles in there for the others to be in
    sx, sy = start
    dx, dy = end

    dif_x = dx - sx
    dif_y = dy - sy

    cx, cy = 0, 0 # The center of the rect for the party to be in
    if dif_x < 0: cx = 1
    elif dif_x > 0: cx = -1
    if dif_y < 0: cy = 1
    elif dif_y > 0: cy = -1

    if abs(dif_x) == abs(dif_y):
      cx *= 2
      cy *= 2
    elif abs(dif_x) > abs(dif_y):
      cx *= 2
    elif abs(dif_x) < abs(dif_y):
      cy *= 2

    tiles = []
    for x in range(dx + cx - 1, dx + cx + 2):
      for y in range(dy + cy - 1, dy + cy + 2):
        tiles.append((x,y))

    for c in self.world.players:
      if c == active or (c.x, c.y) in tiles:
        continue
      try:
        px, py = self.world.get_random_floor_from_set(tiles)
        c.x, c.y = px, py
        self.world.update_fov(c)
      except:
        # Just dont move the creature if we can't find a valid tile
        pass

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
    --no-enemies

  World Types:
    --dungeon           (default)
    --small
    --maze
    --no_paths
    --no_walls
  Note: maze, no_paths, no_walls are not actively supported and kind of suck

  Press [h] in game to view the controls""")
  sys.exit(0)

if __name__ == "__main__":
  start()
