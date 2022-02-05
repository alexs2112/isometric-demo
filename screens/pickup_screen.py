import pygame
from screens.screen import Screen, split_text_to_list
from screens.subscreen import Subscreen
from pygame.locals import (
  KEYDOWN,
  MOUSEBUTTONDOWN,
  K_ESCAPE
)

class PickupScreen(Subscreen):
  def __init__(self, creature, inventory):
    self.creature = creature
    self.inventory = inventory
    self.start_x = 480
    self.start_y = 200
    self.window_width = 320
    self.window_height = 216

  def is_overlay(self):
    return True
  
  def draw(self, screen: Screen):
    x, y = self.start_x, self.start_y
    screen.blit(screen.tileset.get_ui("pickup_screen_background"), (x, y))
    x += 4
    y += 4

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_item = self.get_item_at_mouse(mouse_x, mouse_y)

    item_index = 0
    items = self.inventory.get_items()
    for row in range(4):
      for column in range(6):
        if item_index < len(items):
          item, quantity = items[item_index]
          if item == mouse_item:
            screen.blit(screen.tileset.get_ui("item_box_highlight"), (x + column * 52, y + row * 52))
          else:
            screen.blit(screen.tileset.get_ui("item_box"), (x + column * 52, y + row * 52))

          screen.blit(item.icon, (x + column * 52 + 2, y + row * 52 + 2))

          if quantity > 1:
            screen.write(str(quantity), (x + 38, y + 30), screen.tileset.get_font(16))
        else:
          screen.blit(screen.tileset.get_ui("item_box"), (x + column * 52, y + row * 52))
        
        item_index += 1
  
  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
      elif event.type == MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Clicking off the window closes it
        if self.mouse_out_of_bounds(mouse_x, mouse_y):
          return None

        left, _, right = pygame.mouse.get_pressed()
        item = self.get_item_at_mouse(mouse_x, mouse_y)
        if not item:
          return self
        elif left:
          empty = self.pickup_item(item, self.creature)
          if empty:
            return None
    return self

  # Add the item to the creatures inventory, if this inventory is empty, 
  # remove it from the world and return True
  def pickup_item(self, item, creature):
    self.inventory.remove_item(item)
    creature.add_item(item)
    creature.notify(creature.name + " picks up " + item.name)
    if self.inventory.number_of_different_items() == 0:
      creature.world.remove_inventory(self.inventory)
      return True
    return False

  def get_item_at_mouse(self, mouse_x, mouse_y):
    mouse_x -= self.start_x
    mouse_y -= self.start_y
    mouse_x -= 4
    mouse_y -= 4

    column = mouse_x // 52
    row = mouse_y // 52
    index = row * 6 + column
    if index < 0:
      return None
    return self.inventory.get_item_at_index(index)[0]

  def mouse_out_of_bounds(self, mouse_x, mouse_y):
    if mouse_x < self.start_x \
    or mouse_y < self.start_y \
    or mouse_x > self.start_x + self.window_width \
    or mouse_y > self.start_y + self.window_height:
      return True
    return False
