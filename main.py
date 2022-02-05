import pygame, sys
from items.inventory import Inventory
import misc.init as init
from items.item_factory import ItemFactory
from screens.character_screen import CharacterScreen
from screens.pickup_screen import PickupScreen
from screens.screen import Button
from screens.skill_screen import SkillScreen
from skills.effect_factory import EffectFactory
from skills.skill_factory import SkillFactory
from creatures.creature_factory import CreatureFactory
from world.feature_factory import FeatureFactory
from screens.help_screen import HelpScreen
from screens.inventory_screen import InventoryScreen
from screens.party_screen import PartyScreen
from screens.subscreen import StartScreen
from screens.map_screen import MapScreen
from screens.main_graphics import *
from misc.helpers import *
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_RETURN,
    K_m, K_i, K_s, K_h, K_p, K_c,
    K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    K_LSHIFT,
    QUIT
)

# How long (in milliseconds) between each frame
FRAME_DELAY = 50

# Dimensions of the screen in pixels
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

class Game:
  def __init__(self, args):
    self.args = args
    self.screen = initialize_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    self.feature_factory = FeatureFactory(self.screen.tileset)
    self.world = init.create_world(args, self.feature_factory)
    self.effect_factory = EffectFactory(self.screen.tileset)
    self.skill_factory = SkillFactory(self.screen.tileset, self.effect_factory)
    self.item_factory = ItemFactory(self.world, self.screen.tileset, self.effect_factory, self.skill_factory)
    self.creature_factory = CreatureFactory(self.world, self.screen.tileset, self.item_factory)

    self.messages = [] # Keep track of all the notifications each turn
    init.create_creatures(args, self.world, self.creature_factory, self.messages)
    init.create_items(self.world, self.item_factory)
    self.subscreen = StartScreen()

    self.buttons = [] # Keep track of all the buttons in the main screen
    self.end_turn_button = None
    self.initialize_buttons(760 - 4*32, self.screen.height - 52)

  # Run the main game loop
  def main(self):
    running = True
    frame_counter = 0
    out_of_combat_counter = 0   # Keep track of how many frames are out of combat, to tick cooldowns and effects
    self.active: Creature = self.world.players[0]
    self.screen.center_offset_on_creature(self.active)
    while running:
      self.screen.clear()
      mouse_x, mouse_y = pygame.mouse.get_pos()
      tile_x, tile_y = get_mouse_tile(self.screen.offset_x, self.screen.offset_y, mouse_x, mouse_y)

      if self.subscreen:
        if self.subscreen.is_overlay():
          draw_world(self.screen, self.world)
          if self.active.is_player():
            draw_player_stats(self.screen, self.active, path, target)
            self.active.action_bar.draw(self.screen, mouse_x, mouse_y)
          draw_buttons(self.screen, self.buttons, mouse_x, mouse_y)
          display_messages(self.screen, self.messages)
        self.subscreen.draw(self.screen)

        self.subscreen = self.subscreen.respond_to_events(pygame.event.get())

        # If we move from a subscreen back to main, refocus on the active player
        if not self.subscreen:
          self.screen.center_offset_on_creature(self.active)
      else:
        keys = pygame.key.get_pressed()

        # If we are waiting for movement, projetiles, or for AI
        if self.world.movement_in_progress():
          if frame_counter == 0:
            combat_before = self.world.in_combat()
            self.world.apply_next_move()
            if not combat_before and self.world.in_combat():
              self.active = self.world.get_current_active_creature()
            self.screen.center_offset_on_creature(self.active)
        elif self.world.projectile_sequence:
          self.world.iterate_projectiles()
        elif not self.active.is_player():
          if frame_counter == 0:
            done_turn = self.active.take_turn()
            self.screen.center_offset_on_creature(self.active)
            if done_turn:
              self.active = self.world.get_next_active_creature()
              self.screen.center_offset_on_creature(self.active)
        else:
          # Take player input
          for event in pygame.event.get():
            if event.type == QUIT:
              pygame.quit()
              sys.exit(0)

            if event.type == MOUSEBUTTONDOWN:
              left, _, right = pygame.mouse.get_pressed()

              # Right clicking unloads the current loaded skill
              if self.active.loaded_skill and right:
                self.active.loaded_skill = None

              # If we are clicking a button
              elif mouse_x > self.active.action_bar.screen_x and mouse_y > self.active.action_bar.screen_y:
                self.active.action_bar.mouse_click(mouse_x, mouse_y)
              elif self.clicking_button(self.buttons + [self.end_turn_button], mouse_x, mouse_y):
                pass

              # If we are activating a skill
              elif self.active.loaded_skill:
                self.activate_loaded_skill(tile_x, tile_y)

              # If we are in combat
              elif self.world.in_combat():
                c = self.world.get_creature_at_location(tile_x, tile_y)
                if c:
                  if self.active.can_attack(c.x, c.y):
                    attack_path = get_line(self.active.x, self.active.y, tile_x, tile_y)
                    self.attack_target(attack_path, c)
                  else:
                    path = self.active.get_path_to(c.x, c.y)
                    self.active.move_along_path(path[:-self.active.get_attack_range()])
                else:
                  path = self.active.get_path_to(tile_x, tile_y)
                  self.active.move_along_path(path)
              
              # If we aren't in combat
              else:
                c = self.world.get_creature_at_location(tile_x, tile_y)
                i = self.world.get_inventory(tile_x, tile_y)
                f = self.world.get_feature(tile_x, tile_y)

                if c:
                  if c.is_player():
                    self.active = c
                  else:
                    if self.active.can_attack(c.x, c.y):
                      attack_path = get_line(self.active.x, self.active.y, tile_x, tile_y)
                      self.attack_target(attack_path, c)
                    else:
                      path = self.active.get_path_to(c.x, c.y)
                      self.active.move_along_path(path[:-self.active.get_attack_range()])
                elif i:
                  if self.active.simple_distance_to(tile_x, tile_y) <= 1:
                    self.loot_inventory_at(tile_x, tile_y)
                  else:
                    path = self.active.get_path_to(tile_x, tile_y)
                    self.active.move_along_path(path[:-1])
                elif f:
                  if self.active.simple_distance_to(tile_x, tile_y) <= 1:
                    self.subscreen = f.interact(self.active)
                  else:
                    path = self.active.get_path_to(tile_x, tile_y)
                    self.active.move_along_path(path[:-1])
                else:
                  if keys[K_LSHIFT]:
                    start = self.active.x, self.active.y
                    path = self.active.get_path_to(tile_x, tile_y)
                    self.active.move_along_path_old(path)
                    end = self.active.x, self.active.y
                    self.move_party(start, end)
                  else:
                    path = self.active.get_path_to(tile_x, tile_y)
                    self.active.move_along_path(path)
              
                # At the end of a turn, if a combat has started during that turn reset self.active
                if self.world.in_combat():
                  self.active = self.world.get_current_active_creature()
                  if self.world.can_see(self.active.x, self.active.y):
                    self.screen.center_offset_on_creature(self.active)

            if event.type == KEYDOWN:
              if event.key == K_SPACE:
                self.screen.center_offset_on_creature(self.active)
              elif event.key == K_RETURN:
                self.messages.clear()
                if self.active.loaded_skill:
                  self.activate_loaded_skill(tile_x, tile_y)
                elif self.world.in_combat():
                  self.end_player_turn()
              elif event.key == K_ESCAPE:
                if self.active.loaded_skill:
                  self.active.loaded_skill = None
                else:
                  # Preferably open a game menu here instead of just ending the game lol
                  running = False
              elif event.key == K_m:
                self.subscreen = MapScreen(self.world, self.screen, self.active)
              elif event.key == K_i:
                self.subscreen = InventoryScreen(self.world.players)
              elif event.key == K_p:
                self.subscreen = PartyScreen(self.world.players)
              elif event.key == K_h:
                self.subscreen = HelpScreen()
              elif event.key == K_s:
                if self.active.skills:
                  self.subscreen = SkillScreen(self.active)
                else:
                  self.active.notify(self.active.name + " has no skills to activate.")
              elif event.key == K_c:
                if self.active.is_player():
                  self.subscreen = CharacterScreen(self.screen.tileset, self.active, self.world.players)
              elif event.key in [K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0]:
                self.active.action_bar.activate(event.key)
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
        if self.active.loaded_skill:
          highlight_ability_target(self.screen, self.active, tile_x, tile_y)
          path = None
          target = None
        else:
          path, target = draw_path_to_mouse(self.screen, self.active, tile_x, tile_y)

        if self.world.in_combat():
          self.world.combat_queue.draw(self.screen, 200, 0)

        if self.active.is_player():
          draw_player_stats(self.screen, self.active, path, target)
          self.active.action_bar.draw(self.screen, mouse_x, mouse_y)
        draw_buttons(self.screen, self.buttons, mouse_x, mouse_y)
        if self.world.in_combat() and self.active.is_player():
          draw_end_turn_button(self.screen, self.end_turn_button, self.active, mouse_x, mouse_y)
        show_mouse_tooltips(self.screen, self.world, mouse_x, mouse_y, tile_x, tile_y)
        display_messages(self.screen, self.messages)
        write_active_player(self.screen, self.active)

      pygame.display.update()
      pygame.time.delay(FRAME_DELAY)

      # For now the frame counter just flips a bit
      if frame_counter == 0:
        frame_counter = 1
      else:
        frame_counter = 0
      
      if self.world.in_combat():
        out_of_combat_counter = 0
      else:
        out_of_combat_counter += 1

        # Each turn is 1.5 seconds
        if out_of_combat_counter % 30 == 0:
          for c in self.world.players:
            c.tick_out_of_combat()

        if out_of_combat_counter % 15 == 0:
          if len(self.messages) > 0:
            self.messages.pop(0)

        if out_of_combat_counter >= 30:
          out_of_combat_counter = 0
  
  def end_player_turn(self):
    if self.world.in_combat():
      self.messages.clear()
      self.active = self.world.get_next_active_creature()
      self.screen.center_offset_on_creature(self.active)

  def clicking_button(self, buttons, mouse_x, mouse_y):
    for b in buttons:
      if b.in_bounds(mouse_x, mouse_y):
        b.click()
        return True
    return False 
  
  def activate_loaded_skill(self, tile_x, tile_y):
    tiles = self.active.loaded_skill.get_target_tiles(self.active.x, self.active.y, tile_x, tile_y)
    if not tiles:
      return
    self.active.loaded_skill.cast(self.active, tiles)
    self.active.loaded_skill = None

  def attack_target(self, path, target: Creature):
    w = self.active.get_main_hand()
    if w:
      if w.projectile:
        self.world.add_projectile_path(w.projectile, path[1:])
    self.active.attack_creature(target)

  def loot_inventory_at(self, tile_x, tile_y):
    self.subscreen = PickupScreen(self.screen, self.active, self.world.get_inventory(tile_x, tile_y))

  def move_party(self, start, end):
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
      if c == self.active or (c.x, c.y) in tiles:
        continue
      try:
        px, py = self.world.get_random_floor_from_set(tiles)
        c.x, c.y = px, py
        self.world.update_fov(c)
      except:
        # Just dont move the creature if we can't find a valid tile
        pass
  
  def initialize_buttons(self, x, y):
    # This needs to go here instead of in init because we need access to instance variables
    self.buttons = []

    button_full = pygame.image.load("assets/ui/main_buttons.png")
    base_x, base_y = 0, 52
    width = 32
    height = 52

    def help_func():
      self.subscreen = HelpScreen()
    help_button = Button((x,y,width,height), 
      button_full.subsurface((base_x,base_y,width,height)),
      button_full.subsurface((base_x,base_y+height,width,height)),
      button_full.subsurface((base_x,base_y+height+height,width,height)),
      help_func
    )
    help_button.set_tooltip("H: Help")
    self.buttons.append(help_button)
    base_x += width
    x += width

    def character_func():
      self.subscreen = CharacterScreen(self.screen.tileset, self.active, self.world.players)
    character_button = Button((x,y,width,height), 
      button_full.subsurface((base_x,base_y,width,height)),
      button_full.subsurface((base_x,base_y+height,width,height)),
      button_full.subsurface((base_x,base_y+height+height,width,height)),
      character_func
    )
    character_button.set_tooltip("C: Character")
    self.buttons.append(character_button)
    base_x += width
    x += width

    def skill_func():
      self.subscreen =  SkillScreen(self.active)
    skill_button = Button((x,y,width,height), 
      button_full.subsurface((base_x,base_y,width,height)),
      button_full.subsurface((base_x,base_y+height,width,height)),
      button_full.subsurface((base_x,base_y+height+height,width,height)),
      skill_func
    )
    skill_button.set_tooltip("S: Skills")
    self.buttons.append(skill_button)
    base_x += width
    x += width

    def map_func():
      self.subscreen = MapScreen(self.world, self.screen, self.active)
    map_button = Button((x,y,width,height), 
      button_full.subsurface((base_x,base_y,width,height)),
      button_full.subsurface((base_x,base_y+height,width,height)),
      button_full.subsurface((base_x,base_y+height+height,width,height)),
      map_func
    )
    map_button.set_tooltip("M: Map")
    self.buttons.append(map_button)

    width, height = 160, 64
    self.end_turn_button = Button((self.screen.width - width, y - height, width, height),
      button_full.subsurface((0, 208, width, height)),
      button_full.subsurface((0, 208 + height, width, height)),
      button_full.subsurface((width, 208, width, height)),
      self.end_player_turn
    )
    self.end_turn_button.set_text("End Turn", 26)

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
  Note: maze, no_paths, no_walls are not self.actively supported and kind of suck

  Press [h] in game to view the controls""")
  sys.exit(0)

if __name__ == "__main__":
  start()
