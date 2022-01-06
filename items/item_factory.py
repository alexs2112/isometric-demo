import random
from world.world_builder import World
from items.item import Item, Equipment, Weapon, Potion
from creatures.creature import Creature
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
    ["Ring of Magic Resistance", "Ring of Mana", "Ring of Health"],
    # Weapons
    ["Dagger", "Short Sword", "Hand Axe"],

    # Potions
    ["Potion of Minor Healing"]
  ]
  return image_ids

class ItemFactory:
  def __init__(self, world: World, tileset: TileSet):
    self.world = world
    self.tileset = tileset

    # Store all non-unique items in a hash, like the tileset
    self.cache = {}

  def get_random_item(self):
    i = random.randint(0,12)
    if i == 0: return self.robe()
    elif i == 1: return self.leather_armor()
    elif i == 2: return self.wizard_hat()
    elif i == 3: return self.basic_helm()
    elif i == 4: return self.shoes()
    elif i == 5: return self.gloves()
    elif i == 6: return self.cloak()
    elif i == 7: return self.dagger()
    elif i == 8: return self.short_sword()
    elif i == 9: return self.hand_axe()
    elif i == 10: return self.ring_magic_resist()
    elif i == 11: return self.ring_health()
    elif i == 12: return self.potion_minor_healing()
  
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

  def ring_magic_resist(self):
    name = "Ring of Magic Resistance"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Ring")
    item.set_bonus("M_ARMOR", 1)
    item.set_description("A metal band charged with arcane forces that help to shield from magical effects.")
    self.cache[name] = item
    return item

  def ring_mana(self):
    name = "Ring of Mana"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Ring")
    item.set_bonus("MAX_MANA", 3)
    item.set_description("A ring that one can store magical essence in, drawing from it when needed in the future.")
    self.cache[name] = item
    return item
  
  def ring_health(self):
    name = "Ring of Health"
    if name in self.cache:
      return self.cache[name]
    item = Equipment(name, self.tileset.get_item(name), "Ring")
    item.set_bonus("MAX_HP", 2)
    item.set_description("A ring that one can store their life force in, drawing from it when needed in the future.")
    self.cache[name] = item
    return item

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

  def potion_minor_healing(self):
    name = "Potion of Minor Healing"
    if name in self.cache:
      return self.cache[name]
    item = Potion(name, self.tileset.get_item(name))
    item.set_description("Temp:	A magical healing elixir which causes wounds to close and heal almost instantly.")
    def effect(creature: Creature):
      creature.heal(random.randint(3, 8))
    item.set_effect(effect)
    self.cache[name] = item
    return item
