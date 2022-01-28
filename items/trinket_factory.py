from sprites.tileset import TileSet
from items.item import Equipment

class TrinketFactory:
  def __init__(self, tileset: TileSet):
    self.tileset = tileset
    self.cache = {}

  def ring_magic_resist(self):
    name = "Ring of Magic Resistance"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), None, "Ring")
    item.set_bonus("M_ARMOR", 1)
    item.set_description("A metal band charged with arcane forces that help to shield from magical effects.")
    self.cache[name] = item
    return item

  def ring_mana(self):
    name = "Ring of Mana"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), None, "Ring")
    item.set_bonus("MAX_MANA", 3)
    item.set_description("A ring that one can store magical essence in, drawing from it when needed in the future.")
    self.cache[name] = item
    return item
  
  def ring_health(self):
    name = "Ring of Health"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), None, "Ring")
    item.set_bonus("MAX_HP", 2)
    item.set_description("A ring that one can store their life force in, drawing from it when needed in the future.")
    self.cache[name] = item
    return item