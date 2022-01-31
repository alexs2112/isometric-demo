from sprites.tileset import TileSet
from items.item import Weapon

class WeaponFactory:
  def __init__(self, tileset: TileSet):
    self.tileset = tileset
    self.cache = {}

  def dagger(self):
    name = "Dagger"
    if name in self.cache:
      return self.cache[name]
    item = Weapon(name, self.tileset.get_item(name), self.tileset.get_item_sprite(name), "Light Blade")
    item.set_stats(attack_min=1, attack_max=2, damage_type="piercing", cost=1)
    item.set_description("Temp: A double-edged fighting knife with a sharp point that makes for quick slashes.")
    self.cache[name] = item
    return item
  
  def short_sword(self):
    name = "Short Sword"
    if name in self.cache:
      return self.cache[name]
    item = Weapon(name, self.tileset.get_item(name), self.tileset.get_item_sprite(name), "Light Blade")
    item.set_stats(attack_min=2, attack_max=3, damage_type="slashing")
    item.set_description("Temp: A small, double-edged blade with a short grip.")
    self.cache[name] = item
    return item

  def wooden_club(self):
    name = "Wooden Club"
    if name in self.cache:
      return self.cache[name]
    item = Weapon(name, self.tileset.get_item(name), self.tileset.get_item_sprite(name), "Crushing")
    item.set_stats(attack_min=2, attack_max=3, damage_type="crushing")
    item.set_description("Temp: A heavy piece of wood. While clubs are rather primitive weapons, bashing someone's skull in with one remains a very popular and effective means of dispute resolution.")
    self.cache[name] = item
    return item
  
  def hand_axe(self):
    name = "Hand Axe"
    if name in self.cache:
      return self.cache[name]
    item = Weapon(name, self.tileset.get_item(name), self.tileset.get_item_sprite(name), "Cleaving")
    item.set_stats(attack_min=3, attack_max=4, damage_type="slashing")
    item.set_description("A small axe, just as useful for hacking down enemies as breaking down wood.")
    self.cache[name] = item
    return item

  def shortbow(self):
    name = "Shortbow"
    if name in self.cache:
      return self.cache[name]
    item = Weapon(name, self.tileset.get_item(name), self.tileset.get_item_sprite(name), "Ranged")
    item.set_stats(attack_min=2, attack_max=3, damage_type="piercing", range=5)
    item.set_description("Temp: A curved piece of wood and string, for shooting arrows.")
    item.set_projectile(self.tileset.get_projectile("default_arrow"))
    self.cache[name] = item
    return item
  
  def spear(self):
    name = "Spear"
    if name in self.cache:
      return self.cache[name]
    item = Weapon(name, self.tileset.get_item(name), self.tileset.get_item_sprite(name), "Polearm")
    item.set_stats(attack_min=2, attack_max=2, damage_type="piercing", range=2)
    item.set_description("Temp: A hunting weapon consisting of a wooden shaft with a pointed metal head fastened on one end.")
    self.cache[name] = item
    return item
