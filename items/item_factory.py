from world.world_builder import World
from items.item import Equipment
from tileset import TileSet

def get_item_image_ids():
  # Similar to creatures, these are also stored by type
  image_ids = [
    # Chest
    ["Robe", "Leather Armor"],
    # Head
    ["Wizard Hat", "Basic Helm"],
    # Feet
    ["Shoes"],
    # Hands
    ["Gloves"],
    # Cloak
    ["Cloak"],
    # Rings
    [],
    # Amulet
    [],
    # Weapons
    ["Dagger", "Short Sword", "Hand Axe"]
  ]
  return image_ids

class ItemFactory:
  def __init__(self, world: World, tileset: TileSet):
    self.world = world
    self.tileset = tileset

    # Store all non-unique items in a hash, like the tileset
    self.cache = {}
  
  def robe(self):
    name = "Robe"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Chest")
    item.set_bonus("M_ARMOR", 1)
    self.cache[name] = item
    return item
  
  def leather_armor(self):
    name = "Leather Armor"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Chest")
    item.set_bonus("P_ARMOR", 1)
    self.cache[name] = item
    return item
  
  def wizard_hat(self):
    name = "Wizard Hat"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Head")
    item.set_bonus("M_ARMOR", 1)
    self.cache[name] = item
    return item
  
  def basic_helm(self):
    name = "Basic Helm"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Head")
    item.set_bonus("P_ARMOR", 1)
    self.cache[name] = item
    return item

  def shoes(self):
    name = "Shoes"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Feet")
    self.cache[name] = item
    return item
  
  def gloves(self):
    name = "Gloves"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Hands")
    self.cache[name] = item
    return item

  def dagger(self):
    name = "Dagger"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Main")
    item.set_bonus("ATK_MIN", 1)
    item.set_bonus("ATK_MAX", 1)
    item.set_bonus("ATK_COST", -1)
    self.cache[name] = item
    return item
  
  def short_sword(self):
    name = "Short Sword"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Main")
    item.set_bonus("ATK_MIN", 2)
    item.set_bonus("ATK_MAX", 2)
    self.cache[name] = item
    return item
  
  def hand_axe(self):
    name = "Hand Axe"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Main")
    item.set_bonus("ATK_MIN", 2)
    item.set_bonus("ATK_MAX", 3)
    self.cache[name] = item
    return item
