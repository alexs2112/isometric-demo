import random
from items.tome_factory import TomeFactory
from spells.effect_factory import EffectFactory
from items.equipment_factory import EquipmentFactory
from items.trinket_factory import TrinketFactory
from items.weapon_factory import WeaponFactory
from items.potion_factory import PotionFactory
from spells.spell_factory import SpellFactory
from world.world_builder import World
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

    # Weapons
    ["Dagger", "Short Sword", "Wooden Club", "Hand Axe", "Shortbow", "Spear"],

    # Rings
    ["Ring of Magic Resistance", "Ring of Mana", "Ring of Health"],

    # Potions
    ["Potion of Minor Healing", "Potion of Regeneration"],

    # Spell Tomes
    ["Tome of Embers", "Tome of Flame Lash"]
  ]
  return image_ids

class ItemFactory:
  def __init__(self, world: World, tileset: TileSet, effect: EffectFactory, spell: SpellFactory):
    self.world = world
    self.tileset = tileset

    # Store all non-unique items in a hash, like the tileset
    self.cache = {}

    # To make file less huge and verbose, break each item type into its own factory
    self.effect = effect
    self.spells = spell
    self.equipment = EquipmentFactory(tileset)
    self.trinket = TrinketFactory(tileset)
    self.weapon = WeaponFactory(tileset)
    self.potion = PotionFactory(tileset, self.effect)
    self.tomes = TomeFactory(tileset, spell)

    self.item_functions = [
      self.equipment.robe,
      self.equipment.leather_armor,
      self.equipment.wizard_hat,
      self.equipment.basic_helm,
      self.equipment.shoes,
      self.equipment.gloves,
      self.equipment.cloak,
      self.weapon.dagger,
      self.weapon.short_sword,
      self.weapon.wooden_club,
      self.weapon.hand_axe,
      self.weapon.shortbow,
      self.weapon.spear,
      self.trinket.ring_magic_resist,
      self.trinket.ring_health,
      self.trinket.ring_mana,
      self.potion.potion_minor_healing,
      self.potion.potion_regeneration,
      self.tomes.tome_of_embers,
      self.tomes.tome_of_flame_lash
    ]

  # Temporary, just return a random item out of all the available items
  def get_random_item(self):
    f = random.choice(self.item_functions)
    return f()
