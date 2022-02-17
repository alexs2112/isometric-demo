import pygame
from screens.screen import Button, Screen
from screens.subscreen import Subscreen
from sprites.tileset import TileSet
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
            print("Descending")
            return None
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
  def __init__(self, world, next_level_func):
    self.next_level_func = next_level_func
    self.players = world.players
    self.buttons = []
    self.tooltips = []    # TO DO, same as character screen

  def draw(self, screen: Screen):
    pass

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
