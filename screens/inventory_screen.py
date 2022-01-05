from screens.screen import Screen
from screens.subscreen import Subscreen
from pygame.locals import (
  KEYDOWN,
  K_UP,
  K_DOWN,
  K_RIGHT,
  K_LEFT,
  K_RETURN,
  K_ESCAPE
)

class InventoryScreen(Subscreen):
  def __init__(self, players, inventory=None):
    self.players = players
    self.selected_index = 0
    self.inventory = inventory    # The inventory we are looting from, if any

    if inventory:
      self.column = 1   # Inventory
    else:
      self.column = 0   # Players

    # If an item has been selected to pick up from an inventory, select which player to give it to
    self.picking_up = False
    self.player_index = 0

    self.set_min_max_indices()
  
  def draw(self, screen: Screen):
    line_height = 22
    y = 12
    font = screen.tileset.get_font(20)
    line_index = 0
    p_index = 0
    for p in self.players:
      if self.picking_up and p_index == self.player_index:
        color = screen.tileset.PHYSICAL_YELLOW
      else:
        color = screen.tileset.WHITE
      screen.write(p.name, (12, y), font, color)
      y += line_height
      for item, quantity in p.inventory.get_items():
        s = self.get_item_string(item, quantity, p)
        color = self.get_item_colour(screen, 0, line_index, item, p)
        screen.write(s, (24, y), screen.tileset.get_font(20), color)
        line_index += 1
        y += line_height
      p_index += 1

    if self.inventory:
      x = 800
      y = 12
      line_index = 0
      screen.write("Picking Up:", (x, y), font)
      y += line_height
      for item, quantity in self.inventory.get_items():
        s = self.get_item_string(item, quantity)
        color = self.get_item_colour(screen, 1, line_index)
        screen.write(s, (x + 12, y), screen.tileset.get_font(20), color)
        line_index += 1
        y += line_height

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          if self.picking_up:
            self.picking_up = False
          else:
            # We want to remove this inventory from the world if it is empty when we are done
            if self.inventory and self.inventory.number_of_different_items() == 0:
              self.players[0].world.remove_inventory(self.inventory)
            return None
        elif event.key == K_DOWN:
          if self.picking_up:
            self.player_index = min(len(self.players) - 1, self.player_index + 1)
          else:
            self.selected_index = min(self.max_index, self.selected_index + 1)
        elif event.key == K_UP:
          if self.picking_up:
            self.player_index = max(0, self.player_index - 1)
          else:
            self.selected_index = max(self.min_index, self.selected_index - 1)
        elif event.key == K_RIGHT:
          if self.inventory and self.inventory.number_of_different_items() > 0:
            self.column = 1
            self.selected_index = min(self.max_index_pickup, self.selected_index)
        elif event.key == K_LEFT:
          if self.inventory:
            self.column = 0
            self.selected_index = min(self.max_index, self.selected_index)
        elif event.key == K_RETURN:
          if self.picking_up:
            p = self.players[self.player_index]
            i, q = self.inventory.get_item_at_index(self.selected_index)
            self.inventory.remove_item(i, q)
            p.add_item(i, q)
            self.picking_up = False
            self.set_min_max_indices()
            if self.inventory.number_of_different_items() > 0:
              self.selected_index = max(self.min_index, self.selected_index - 1)
            else:
              self.column = 0
              self.selected_index = min(self.max_index, self.selected_index)
          elif self.column == 0:
            p = self.get_current_selected_player()
            i = self.get_current_item()
            if i and i.is_equipment():
              if p.is_equipped(i):
                p.unequip(i)
              else:
                p.equip(i)
          else:
            # Mark an item for pickup, then get the player to pick it up
            self.picking_up = True
    return self

  def get_current_selected_player(self):
    item_count = 0
    for p in self.players:
      items = p.inventory.get_items()
      item_count += len(items)
      if self.selected_index < item_count:
        return p
  
  def get_current_item(self):
    item_index = 0
    if self.column == 0:
      for p in self.players:
        for item, _ in p.inventory.get_items():
          if item_index == self.selected_index:
            return item
          item_index += 1

  def set_min_max_indices(self):
    self.min_index = 0
    self.max_index = -1
    for p in self.players:
      self.max_index += p.inventory.number_of_different_items()
    
    self.max_index_pickup = -1
    if self.inventory:
      self.max_index_pickup = self.inventory.number_of_different_items() - 1


  def get_item_string(self, item, quantity, creature=None):
    s = ""
    if quantity > 1:
      s += str(quantity) + " "
    s  += item.name
    if quantity > 1 and not item.unique:
      s += "s"
    if creature and creature.is_equipped(item):
      s += " (Equipped)"
    return s

  def get_item_colour(self, screen, column, index, item=None, creature=None):
    if self.column == column and self.selected_index == index:
      color = screen.tileset.PHYSICAL_YELLOW
    elif creature and creature.is_equipped(item):
      color = screen.tileset.EQUIPPED_GREEN
    else:
      color = screen.tileset.WHITE
    return color
