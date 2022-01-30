import random
from items.item import Item
from items.tome_factory import TomeFactory
from skills.effect_factory import EffectFactory
from items.equipment_factory import EquipmentFactory
from items.trinket_factory import TrinketFactory
from items.weapon_factory import WeaponFactory
from items.potion_factory import PotionFactory
from skills.skill_factory import SkillFactory
from world.world_builder import World
from sprites.tileset import TileSet

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

    # Skill Tomes
    ["Tome of Embers", "Tome of Flame Lash"]
  ]
  return image_ids

class ItemFactory:
  def __init__(self, world: World, tileset: TileSet, effect: EffectFactory, skill: SkillFactory):
    self.world = world
    self.tileset = tileset

    # Store all non-unique items in a hash, like the tileset
    self.cache = {}

    # To make file less huge and verbose, break each item type into its own factory
    self.effect = effect
    self.skills = skill
    self.equipment = EquipmentFactory(tileset)
    self.trinket = TrinketFactory(tileset)
    self.weapon = WeaponFactory(tileset)
    self.potion = PotionFactory(tileset, self.effect)
    self.tomes = TomeFactory(tileset, skill)

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

  def get_win_condition(self):
    item = Item("Stone of Power", self.tileset.get_item("Stone of Power"), True)
    item.set_description("The stone of power! If you have picked this up, consider the game won...")
    return item
