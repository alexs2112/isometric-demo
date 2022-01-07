from tileset import TileSet
from items.item import Weapon

class WeaponFactory:
  def __init__(self, tileset: TileSet):
    self.tileset = tileset
    self.cache = {}

  def dagger(self):
    name = "Dagger"
    if name in self.cache:
      return self.cache[name]
    item = Weapon(name, self.tileset.get_item(name))
    item.set_stats(attack_min=1, attack_max=2, cost=1)
    item.set_description("Temp: A double-edged fighting knife with a sharp point that makes for quick slashes.")
    self.cache[name] = item
    return item
  
  def short_sword(self):
    name = "Short Sword"
    if name in self.cache:
      return self.cache[name]
    item = Weapon(name, self.tileset.get_item(name))
    item.set_stats(attack_min=3, attack_max=4)
    item.set_description("Temp: A small, double-edged blade with a short grip.")
    self.cache[name] = item
    return item
  
  def hand_axe(self):
    name = "Hand Axe"
    if name in self.cache:
      return self.cache[name]
    item = Weapon(name, self.tileset.get_item(name))
    item.set_stats(attack_min=3, attack_max=5)
    item.set_description("A small axe, just as useful for hacking down enemies as breaking down wood.")
    self.cache[name] = item
    return item