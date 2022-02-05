import pygame
from screens.screen import Screen, Button, split_text_to_list
from screens.subscreen import Subscreen
from pygame.locals import (
  KEYDOWN,
  MOUSEBUTTONDOWN,
  K_ESCAPE
)

class PickupScreen(Subscreen):
  def __init__(self, screen, creature, inventory):
    self.creature = creature
    self.inventory = inventory
    self.start_x = 480
    self.start_y = 200
    self.window_width = 320
    self.window_height = 416

    self.pick_up_all = None
    self.exit_button = None
    self.option_buttons = []
    self.selected_item = None
    self.initialize_buttons(screen.tileset)

  def is_overlay(self):
    return True
  
  def draw(self, screen: Screen):
    x, y = self.start_x, self.start_y
    screen.blit(screen.tileset.get_ui("pickup_screen_background"), (x, y))
    x += 4
    y += 4

    mouse_x, mouse_y = pygame.mouse.get_pos()
    self.pick_up_all.draw(screen, mouse_x, mouse_y)
    self.exit_button.draw(screen, mouse_x, mouse_y)
    mouse_item = self.get_item_at_mouse(mouse_x, mouse_y)
    if mouse_item == None or self.get_moused_option(mouse_x, mouse_y):
      mouse_item = self.selected_item

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

        item_index += 1
    
    item = self.get_item_at_mouse(mouse_x, mouse_y)
    if item:
      screen.blit(item.icon, (14 + self.start_x, 230 + self.start_y))
      screen.write(item.name, (74 + self.start_x, 242 + self.start_y), screen.tileset.get_font(20))
      x,y = 14 + self.start_x, 290 + self.start_y
      lines = split_text_to_list(item.description, 300, screen.tileset.get_font(16))
      for l in lines:
        screen.write(l, (x,y), screen.tileset.get_font(16))
        y += 18
    
    if self.selected_item:
      for b in self.option_buttons:
        b.draw(screen, mouse_x, mouse_y)
  
  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          if self.selected_item:
            self.selected_item = None
          return None
      elif event.type == MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        option = self.get_moused_option(mouse_x, mouse_y)
        if option:
          option.click()
          if self.inventory.number_of_different_items() <= 0:
            return None
          if self.inventory.get_quantity(self.selected_item) == 0:
            self.selected_item = None
          return self
        elif self.pick_up_all.in_bounds(mouse_x, mouse_y):
          self.pick_up_all.click()
          return None
        elif self.exit_button.in_bounds(mouse_x, mouse_y):
          return None

        # Clicking off the window closes it
        #elif self.mouse_out_of_bounds(mouse_x, mouse_y):
        #  return None

        self.selected_item = None
        left, _, right = pygame.mouse.get_pressed()
        item = self.get_item_at_mouse(mouse_x, mouse_y)
        if not item:
          return self
        elif right:
          self.selected_item = item
          self.refresh_option_buttons(mouse_x, mouse_y)
        elif left:
          empty = self.pickup_item(item, self.creature)
          if empty:
            return None
    return self

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
      if self.pick_up_all.not_in_bounds(mouse_x, mouse_y) and self.get_moused_option == None:
        return True
    return False

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

  def initialize_buttons(self, tileset):
    def pick_up_all():
      items = self.inventory.get_items()
      for i, q in items:
        self.creature.add_item(i, q)
        self.inventory.remove_item(i, q)
      self.creature.notify(self.creature.name + " picks up items.")
      self.creature.world.remove_inventory(self.inventory)

    self.pick_up_all = Button((self.start_x, self.start_y - 40, 120, 40), 
      tileset.get_ui("pick_up_all"), tileset.get_ui("pick_up_all_highlight"),
      func=pick_up_all)
    self.pick_up_all.set_text("Pick Up All", 18)

    self.exit_button = Button((self.start_x + self.window_width - 40, self.start_y - 35, 40, 35),
      tileset.get_ui("exit_button"), tileset.get_ui("exit_button_highlight"))

    for p in self.creature.world.players:
      b = Button((self.start_x, self.start_y, 128, 18),
        tileset.get_ui("option_button"), tileset.get_ui("option_button_highlight"),
        func = self.get_option_func(p))
      if p == self.creature:
        b.set_text("Pick up", size=14)
      else:
        b.set_text("Send to " + p.name, size=14)
      self.option_buttons.append(b)
  
  def get_option_func(self, creature):
    def func():
      self.inventory.remove_item(self.selected_item)
      creature.add_item(self.selected_item)
      creature.notify(creature.name + " picks up " + self.selected_item.name)
      if self.inventory.number_of_different_items() == 0:
        creature.world.remove_inventory(self.inventory)
    return func

  def refresh_option_buttons(self, mouse_x, mouse_y):
    # Send to P4
    # Send to P3
    # Send to P2
    # Pick Up
    inc = 0
    for b in self.option_buttons:
      b.x = mouse_x - 8
      b.y = mouse_y - 9 - inc
      inc += 18
  
  def get_moused_option(self, mouse_x, mouse_y):
    if self.selected_item:
      for b in self.option_buttons:
        if b.in_bounds(mouse_x, mouse_y):
          return b
    return None
