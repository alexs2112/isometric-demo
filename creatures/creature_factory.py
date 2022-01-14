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
    creature.set_attributes(1,2,1)
    creature.set_misc_stats()
    creature.add_and_equip(self.items.weapon.shortbow())
    creature.add_and_equip(self.items.equipment.leather_armor())
    creature.update_sprite()
    creature.move_to(x, y)
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature

  def new_goobert(self, x, y):
    name = "Goobert"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_base_stats(max_hp=8, max_mana=1, p_armor=1, m_armor=1)
    creature.set_attributes(1,2,1)
    creature.set_misc_stats()
    creature.set_unarmed_stats(min=2, max=3, cost=1)
    creature.move_to(x, y)
    creature.add_and_equip(self.items.equipment.cloak())
    creature.add_and_equip(self.items.equipment.shoes())
    creature.update_sprite()
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature
  
  def new_wizard(self, x, y):
    name = "Wizard"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_base_stats(max_hp=8, max_mana=5, p_armor=1, m_armor=2)
    creature.set_attributes(1,1,2)
    creature.set_misc_stats()
    creature.move_to(x, y)
    creature.set_unarmed_stats(min=3, max=5, type="magical")
    creature.add_and_equip(self.items.equipment.wizard_hat())
    creature.add_and_equip(self.items.equipment.robe())
    creature.modify_skill("Fire", 1)
    creature.update_sprite()
    creature.add_item(self.items.potion.potion_minor_healing())
    creature.add_spell(self.items.spells.embers())
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature
  
  def new_harold(self, x, y):
    name = "Harold"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_base_stats(max_hp=15, max_mana=0, p_armor=2, m_armor=1)
    creature.set_attributes(2,1,1)
    creature.set_misc_stats(max_ap=2)
    creature.move_to(x, y)
    creature.add_and_equip(self.items.weapon.hand_axe())
    creature.add_and_equip(self.items.equipment.leather_armor())
    creature.update_sprite()
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature

  def new_mushroom(self, x, y):
    name = "Mushroom"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Plant", self.world)
    creature.set_ai(ai.Plant(creature))
    creature.set_base_stats(max_hp=5, max_mana=0, p_armor=0, m_armor=0)
    creature.set_attributes(0,0,0)
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
    creature.set_attributes(1,1,1)
    creature.set_misc_stats(speed=2, initiative=2)
    creature.set_unarmed_stats(min=2, max=3)
    if random.random() < 0.3:
      i = random.random()
      if i < 0.1:
        creature.add_and_equip(self.items.weapon.dagger())
      elif i < 0.2:
        creature.add_and_equip(self.items.weapon.short_sword())
      elif i < 0.3:
        creature.add_and_equip(self.items.weapon.spear())
      elif i < 0.4:
        creature.add_and_equip(self.items.weapon.shortbow())
      elif i < 0.5:
        creature.add_and_equip(self.items.weapon.hand_axe())
      else:
        creature.add_and_equip(self.items.weapon.wooden_club())
    creature.move_to(x, y)
    self.world.add_creature(creature)
    return creature
