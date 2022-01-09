from screens.screen import Screen
from screens.subscreen import Subscreen
from pygame.locals import (
  KEYDOWN,
  K_UP,
  K_DOWN,
  K_RIGHT,
  K_LEFT,
  K_RETURN,
  K_d,
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

    self.cache_item = None
    self.cache_item_desc = []
  
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
      x = 900
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

    i, _ = self.get_current_item()
    self.set_cache_item(screen, font, i)
    if self.cache_item:
      x = 420
      y = 12
      screen.blit(screen.tileset.get_item_large(self.cache_item.name), (x,y))
      y += 22
      screen.write(self.cache_item.name, (x+70,y), font)
      x += 12
      y += 20
      y += line_height
      y = screen.write_list(self.cache_item_desc, (x, y), font)

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          if self.picking_up:
            self.picking_up = False
          else:
            self.cleanup()
            return None
        elif event.key == K_DOWN:
          if self.picking_up:
            self.player_index = min(len(self.players) - 1, self.player_index + 1)
          else:
            if self.column == 0:
              self.selected_index = min(self.max_index, self.selected_index + 1)
            else:
              self.selected_index = min(self.max_index_pickup, self.selected_index + 1)
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
        elif event.key == K_d:  # Drop
          p = self.get_current_selected_player()
          i, q = self.get_current_item()
          p.remove_item(i, q)
          p.world.add_item(i, (p.x, p.y), q)
          self.inventory = p.world.get_inventory(p.x, p.y)
          self.set_min_max_indices()
          self.selected_index = max(0, self.selected_index - 1)
        elif event.key == K_RETURN:
          self.cache_item = None
          self.cache_item_desc = []
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
            i, _ = self.get_current_item()
            if not i:
              return self
            if i.is_equipment():
              if p.is_equipped(i):
                p.unequip(i)
              else:
                p.equip(i)
            elif i.is_consumable():
              worked = i.consume(p)
              if worked:
                p.remove_item(i)
              self.cleanup()
              return None     # After drinking a potion, immediately return to the main screen
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
        for item, quantity in p.inventory.get_items():
          if item_index == self.selected_index:
            return item, quantity
          item_index += 1
    else:
      i, q = self.inventory.get_item_at_index(self.selected_index)
      return i, q

  def set_min_max_indices(self):
    # Reset the indices whenever an item is moved between a player and the inventory
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

  def set_cache_item(self, screen, font, i):
    if i != self.cache_item:
      self.cache_item = i
      if i:
        self.cache_item_desc = screen.split_text_to_list(i.description, 400, font)
        
        if i.is_equipment():
          self.cache_item_desc.append("")
          for b, v in i.all_bonuses():
            self.cache_item_desc.append(b + " : " + str(v))
          
          if i.is_weapon():
            self.cache_item_desc.append(i.weapon_string())

        self.cache_item_desc += [""] + self.get_item_options(i)
      else:
        self.cache_item_desc = []

  def get_item_options(self, item):
    options = []
    if self.column == 1:
      options.append("[ENTER]: Pick Up")
    else:
      if item.is_equipment():
        creature = self.get_current_selected_player()
        if creature.is_equipped(item):
          options.append("[ENTER]: Unequip")
        else:
          options.append("[ENTER]: Equip")
      if item.is_consumable():
        options.append("[ENTER]: Use")
      options.append("[D]: Drop")
    return options

  # Call this before returning None
  def cleanup(self):
    if self.inventory and self.inventory.number_of_different_items() == 0:
      self.players[0].world.remove_inventory(self.inventory)
