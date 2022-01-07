from tileset import TileSet
from items.item import Equipment

class EquipmentFactory:
  def __init__(self, tileset: TileSet):
    self.tileset = tileset
    self.cache = {}

  def robe(self):
    name = "Robe"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Chest")
    item.set_bonus("M_ARMOR", 1)
    item.set_description("Temp: A large, loose-fitting, wide-sleeved outer garment made of light cloth. It offers little protection against physical harm, but does not hinder evasion or spellcasting.")
    self.cache[name] = item
    return item
  
  def leather_armor(self):
    name = "Leather Armor"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Chest")
    item.set_bonus("P_ARMOR", 1)
    item.set_description("Temp: A suit made from layers of tanned animal hide, this light armour provides basic protection with almost no hindrance to elaborate gestures or swift, stealthy movement.")
    self.cache[name] = item
    return item
  
  def wizard_hat(self):
    name = "Wizard Hat"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Head")
    item.set_bonus("M_ARMOR", 1)
    item.set_description("Magical protection woven into the cloth that makes this hat.")
    self.cache[name] = item
    return item
  
  def basic_helm(self):
    name = "Basic Helm"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Head")
    item.set_bonus("P_ARMOR", 1)
    item.set_description("Temp: A simple piece of metal headgear.")
    self.cache[name] = item
    return item

  def shoes(self):
    name = "Shoes"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Feet")
    item.set_bonus("SPEED", 1)
    item.set_description("Simple cloth shoes, they permit faster running on the hard stone tiles of the dungeon.")
    self.cache[name] = item
    return item
  
  def gloves(self):
    name = "Gloves"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Hands")
    item.set_bonus("UNARMED_DAMAGE", 1)
    item.set_description("A pair of weighted gloves, they add a bit of extra force to your punches.")
    self.cache[name] = item
    return item
  
  def cloak(self):
    name = "Cloak"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Cloak")
    item.set_bonus("P_ARMOR", 1)
    item.set_description("A sturdy cloak, it helps protect against errant blades.")
    self.cache[name] = item
    return item

  