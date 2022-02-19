import pygame
from screens.screen import Button, Screen, TooltipBox
from screens.subscreen import Subscreen
from sprites.tileset import TileSet
from creatures.stats_helper import STAT_LIST, ATTRIBUTE_LIST
from pygame.locals import (
  MOUSEBUTTONDOWN,
  KEYDOWN,
  K_ESCAPE,
  K_RETURN,
  K_SPACE
)

class StaircaseConfirm(Subscreen):
  def __init__(self, world, next_level_func):
    self.screen_width, self.screen_height = 360, 128
    self.screen_x, self.screen_y = (1280 - self.screen_width) // 2, (800 - self.screen_height) // 2
    self.world = world
    self.next_level_func = next_level_func
    self.confirm_button = None
    self.cancel_button = None

  def initialize_buttons(self, tileset: TileSet):
    self.confirm_button = Button((self.screen_x+180, self.screen_y + self.screen_height - 52, 180, 52), tileset.get_ui("confirm_button_default"), tileset.get_ui("confirm_button_highlight"))
    self.confirm_button.set_text("Descend")
    self.cancel_button = Button((self.screen_x, self.screen_y + self.screen_height - 52, 180, 52), tileset.get_ui("confirm_button_default"), tileset.get_ui("confirm_button_highlight"))
    self.cancel_button.set_text("Cancel")

  def is_overlay(self):
    return True

  def draw(self, screen: Screen):
    if self.confirm_button == None:
      self.initialize_buttons(screen.tileset)

    screen.blit(screen.tileset.get_ui("confirmation_box"), (self.screen_x, self.screen_y))
    screen.write_centered("Proceed to the next level?", (self.screen_x + self.screen_width // 2, self.screen_y + 16), screen.tileset.get_font(26))

    x,y = pygame.mouse.get_pos()
    self.confirm_button.draw(screen, x, y)
    self.cancel_button.draw(screen, x, y)

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
        elif event.key == K_RETURN or event.key == K_SPACE:
          self.next_level_func()
          return None
      elif event.type == MOUSEBUTTONDOWN:
        x,y = pygame.mouse.get_pos()
        _, _, right = pygame.mouse.get_pressed()
        if right or self.mouse_out_of_bounds(x,y):
          return None
        else:
          if self.confirm_button.in_bounds(x,y):
            self.next_level_func()
            return LevelUpStatsScreen(self.world)
          elif self.cancel_button.in_bounds(x,y):
            return None
    return self

  def mouse_out_of_bounds(self, x, y):
    if x < self.screen_x \
    or x > self.screen_x + self.screen_width \
    or y < self.screen_y \
    or y > self.screen_y + self.screen_height:
      return True
    return False

class LevelUpStatsScreen(Subscreen):
  def __init__(self, world):
    self.players = world.players
    self.continue_button = None
    self.buttons = []     # A list of lists, each player has their list of buttons
    self.available_points = []
    self.tooltips = []    # TO DO, same as character screen

  def draw(self, screen: Screen):
    if not self.buttons:
      self.initialize_buttons(screen, screen.tileset)
      self.update_can_continue()

    x,y = pygame.mouse.get_pos()
    for i in range(len(self.players)):
      self.draw_player(screen, self.players[i])
      for b in self.buttons[i]:
        b.draw(screen, x, y)
      self.draw_player_stats(screen, self.players[i], self.buttons[i])
    self.draw_continue(screen, x, y)

    for t in self.tooltips:
      t.draw(screen, x, y)

  def initialize_buttons(self, screen: Screen, tileset: TileSet):
    for p in self.players:
      bs = []
      x,y = self.get_player_start_pos(screen.width, p)
      y += 92
      for key in STAT_LIST.keys():
        btn = Button((x,y,288,36), tileset.get_ui("stats_bar_default"), tileset.get_ui("stats_bar_default_highlight"))
        btn.set_toggle(tileset.get_ui("stats_bar_toggle"), tileset.get_ui("stats_bar_toggle_highlight"))
        btn.set_text(key, size=18)
        btn.stat = key
        bs.append(btn)

        # Identical tooltips to the character screen to reuse their assets
        tip = TooltipBox(STAT_LIST[key], (x,y,288,36), 212, tileset.get_ui("stats_tooltip_line"), tileset.get_font(16))
        tip.set_header(key, tileset.get_ui("stats_tooltip_line_header"), 18)
        tip.set_bottom_bg(tileset.get_ui("stats_tooltip_line_bottom"))
        tip.set_delay(6)
        self.tooltips.append(tip)

        y += 36

      self.buttons.append(bs)
    
    self.continue_button = Button(((screen.width - 180) // 2, screen.height - 64, 180, 52), tileset.get_ui("confirm_button_default"), tileset.get_ui("confirm_button_highlight"))
    self.continue_button.set_text("Continue")
    self.continue_button.active = False

  def get_player_start_pos(self, screen_width, player):
    # A little inefficient to calculate this each time but it probably doesn't matter
    player_width = len(self.players) * 320
    start_x = (screen_width - player_width) // 2
    start_x += 320 * self.players.index(player)
    return start_x + 16, 16
  
  def draw_player(self, screen: Screen, player):
    x,y = self.get_player_start_pos(screen.width, player)
    x += (288 - 92) // 2
    screen.blit(screen.tileset.get_ui("character_sprite_box"), (x,y))
    screen.blit(player.get_sprite(86), (x + 3, y + 3))
    points = self.available_points[self.players.index(player)]
    if points < 0:
      colour = screen.tileset.HP_RED
    else:
      colour = screen.tileset.WHITE
    screen.write("Points: " + str(points), (x + 100, y + 50), screen.tileset.get_font(), colour)

  def draw_player_stats(self, screen: Screen, player, buttons):
    # This is really inefficient to calculate and draw every single frame when most of it doesnt change
    for b in buttons:
      v = player.get_stat(b.stat)
      if b.is_toggled:
        v += 1
        colour = screen.tileset.EQUIPPED_GREEN
      else:
        colour = screen.tileset.WHITE
      screen.write_centered(str(v), (b.x + 271, b.y + 7), screen.tileset.get_font(20), colour)
      screen.blit(screen.tileset.get_ui("stats_question_icon"), (b.x + 2, b.y + 2))
  
  def draw_continue(self, screen: Screen, mouse_x, mouse_y):
    if self.continue_button.active:
      self.continue_button.draw(screen, mouse_x, mouse_y)
    else:
      screen.blit(screen.tileset.get_ui("confirm_button_default"), ((screen.width - 180) // 2, screen.height - 64))
      screen.write_centered("Assign Stats!", (screen.width // 2, screen.height - 52), screen.tileset.get_font())

  def get_player_selected(self, player):
    index = self.players.index(player)
    selected = []
    for b in self.buttons[index]:
      if b.is_toggled:
        selected.append(b.stat)
    return selected
  
  def update_can_continue(self):
    self.available_points.clear()
    res = True
    for p in self.players:
      v = len(self.get_player_selected(p))
      self.available_points.append(2 - v)
      if v != 2:
        res = False
    self.continue_button.active = res

  def finalize_stats(self):
    for p in self.players:
      for s in self.get_player_selected(p):
        p.modify_stat(s, 1)
      p.full_rest()

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
      elif event.type == MOUSEBUTTONDOWN:
        x,y = pygame.mouse.get_pos()
        if self.continue_button.in_bounds(x,y):
          self.finalize_stats()
          return None
        for p in self.buttons:
          for b in p:
            if b.in_bounds(x,y):
              b.click()
              self.update_can_continue()
              return self
    return self
