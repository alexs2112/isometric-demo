import random
from abilities.effect import Effect
from abilities.effect_factory import EffectFactory
from items.equipment_factory import EquipmentFactory
from items.trinket_factory import TrinketFactory
from items.weapon_factory import WeaponFactory
from items.potion_factory import PotionFactory
from world.world_builder import World
from items.item import Equipment, Weapon, Potion
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
    ["Potion of Minor Healing", "Potion of Regeneration"]
  ]
  return image_ids

class ItemFactory:
  def __init__(self, world: World, tileset: TileSet):
    self.world = world
    self.tileset = tileset

    # Store all non-unique items in a hash, like the tileset
    self.cache = {}

    # To make file less huge and verbose, break each item type into its own factory
    self.effect = EffectFactory()
    self.equipment = EquipmentFactory(tileset)
    self.trinket = TrinketFactory(tileset)
    self.weapon = WeaponFactory(tileset)
    self.potion = PotionFactory(tileset, self.effect)

  def get_random_item(self):
    i = random.randint(0,13)
    if i == 0: return self.equipment.robe()
    elif i == 1: return self.equipment.leather_armor()
    elif i == 2: return self.equipment.wizard_hat()
    elif i == 3: return self.equipment.basic_helm()
    elif i == 4: return self.equipment.shoes()
    elif i == 5: return self.equipment.gloves()
    elif i == 6: return self.equipment.cloak()
    elif i == 7: return self.weapon.dagger()
    elif i == 8: return self.weapon.short_sword()
    elif i == 9: return self.weapon.hand_axe()
    elif i == 10: return self.trinket.ring_magic_resist()
    elif i == 11: return self.trinket.ring_health()
    elif i == 12: return self.potion.potion_minor_healing()
    elif i == 12: return self.potion.potion_regeneration()
