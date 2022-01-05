import random
import creatures.ai as ai
from creatures.creature import Creature
from items.item_factory import ItemFactory
from tileset import TileSet
from world.world_builder import World

class CreatureFactory:
  def __init__(self, world: World, tileset: TileSet, item_factory: ItemFactory):
    self.world = world
    self.tileset = tileset
    self.items = item_factory

  def new_edward(self, x, y):
    name = "Edward"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_base_stats(max_hp=10, max_mana=2, p_armor=1, m_armor=1)
    creature.set_misc_stats(max_ap=3, speed=3, vision_radius=5)
    creature.set_attack_stats(attack_min=0, attack_max=1)
    creature.add_and_equip(self.items.short_sword())
    creature.add_and_equip(self.items.leather_armor())
    creature.move_to(x, y)
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature

  def new_goobert(self, x, y):
    name = "Goobert"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_base_stats(max_hp=8, max_mana=1, p_armor=1, m_armor=1)
    creature.set_misc_stats(max_ap=3, speed=3, vision_radius=5)
    creature.set_attack_stats(attack_min=0, attack_max=1)
    creature.move_to(x, y)
    creature.add_and_equip(self.items.dagger())
    creature.add_and_equip(self.items.shoes())
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature
  
  def new_wizard(self, x, y):
    name = "Wizard"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_base_stats(max_hp=8, max_mana=5, p_armor=1, m_armor=2)
    creature.set_misc_stats(max_ap=3, speed=3, vision_radius=5)
    creature.set_attack_stats(attack_min=1, attack_max=2, base_damage_type="magical")
    creature.move_to(x, y)
    creature.add_and_equip(self.items.wizard_hat())
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature
  
  def new_harold(self, x, y):
    name = "Harold"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_base_stats(max_hp=15, max_mana=0, p_armor=2, m_armor=1)
    creature.set_misc_stats(max_ap=2, speed=3, vision_radius=5)
    creature.set_attack_stats(attack_min=1, attack_max=1)
    creature.move_to(x, y)
    creature.add_and_equip(self.items.hand_axe())
    creature.add_and_equip(self.items.leather_armor())
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature

  def new_mushroom(self, x, y):
    name = "Mushroom"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Plant", self.world)
    creature.set_ai(ai.Plant(creature))
    creature.set_base_stats(max_hp=5, max_mana=0, p_armor=0, m_armor=0)
    creature.set_misc_stats(max_ap=0, speed=0, vision_radius=0)
    creature.move_to(x, y)
    self.world.add_creature(creature)
    return creature
  
  def new_skeleton(self, x, y):
    name = "Skeleton"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Undead", self.world)
    creature.set_ai(ai.Basic(creature))
    creature.set_base_stats(max_hp=8, max_mana=0, p_armor=1, m_armor=1)
    creature.set_misc_stats(max_ap=3, speed=2, vision_radius=5)
    creature.set_attack_stats(attack_min=2, attack_max=3)
    if random.random() < 0.2:
      # Armed skeletons will hit like a truck since its just adding directly to attack_min and max
      # This will be fixed when I fix weapons
      i = random.random()
      if i < 0.3:
        creature.add_and_equip(self.items.dagger())
      elif i > 0.9:
        creature.add_and_equip(self.items.hand_axe())
      else:
        creature.add_and_equip(self.items.short_sword())
    if random.random() < 0.5:
      i = random.random()
      if i < 0.25:
        creature.add_and_equip(self.items.wizard_hat())
      elif i < 0.5:
        creature.add_and_equip(self.items.cloak())
      elif i > 0.75:
        creature.add_and_equip(self.items.basic_helm())
      else:
        creature.add_and_equip(self.items.leather_armor())
    creature.move_to(x, y)
    self.world.add_creature(creature)
    return creature
