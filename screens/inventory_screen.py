from screens.screen import Screen
from screens.subscreen import Subscreen
from pygame.locals import (
  KEYDOWN,
  K_UP,
  K_DOWN,
  K_RETURN,
  K_ESCAPE
)

class InventoryScreen(Subscreen):
  def __init__(self, players):
    self.players = players
    self.selected_index = 0
  
  def draw(self, screen: Screen):
    line_height = 22
    y = 12
    font = screen.tileset.get_font(20)
    line_index = 0
    for p in self.players:
      screen.write(p.name, (12, y), font)
      y += line_height
      for item, quantity in p.inventory.get_items():
        s = ""
        if quantity > 1:
          s += str(quantity) + " "
        s  += item.name
        if quantity > 1 and not item.unique:
          s += "s"

        if p.is_equipped(item):
          s += " (Equipped)"
        
        if self.selected_index == line_index:
          color = screen.tileset.PHYSICAL_YELLOW
        elif p.is_equipped(item):
          color = screen.tileset.EQUIPPED_GREEN
        else:
          color = screen.tileset.WHITE
        screen.write(s, (24, y), screen.tileset.get_font(20), color)
        line_index += 1

        y += line_height

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
        elif event.key == K_DOWN:
          self.selected_index += 1
        elif event.key == K_UP:
          self.selected_index -= 1
        elif event.key == K_RETURN:
          p = self.get_current_selected_player()
          i = self.get_current_item()
          if i.is_equipment():
            if p.is_equipped(i):
              p.unequip(i)
            else:
              p.equip(i)
    return self

  def get_current_selected_player(self):
    item_count = 0
    for p in self.players:
      items, _ = p.inventory.get_items()
      item_count += len(items)
      if self.selected_index < item_count:
        return p
  
  def get_current_item(self):
    item_index = 0
    for p in self.players:
      for item, _ in p.inventory.get_items():
        if item_index == self.selected_index:
          return item
        item_index += 1