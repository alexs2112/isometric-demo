import creatures.ai as ai
from creatures.creature import Creature
from tileset import TileSet
from world.world_builder import World

class CreatureFactory:
  def __init__(self, world: World, tileset: TileSet):
    self.world = world
    self.tileset = tileset

  def new_edward(self, x, y):
    name = "Edward"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_base_stats(max_hp=10, max_mana=2, p_armor=2, m_armor=2)
    creature.set_misc_stats(max_ap=3, speed=3, vision_radius=5)
    creature.set_attack_stats(attack_min=2, attack_max=4)
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
    creature.set_attack_stats(attack_min=1, attack_max=3, attack_cost=1)
    creature.move_to(x, y)
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature
  
  def new_wizard(self, x, y):
    name = "Wizard"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_base_stats(max_hp=8, max_mana=5, p_armor=0, m_armor=3)
    creature.set_misc_stats(max_ap=3, speed=3, vision_radius=5)
    creature.set_attack_stats(attack_min=2, attack_max=4, base_damage_type="magical")
    creature.move_to(x, y)
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature
  
  def new_harold(self, x, y):
    name = "Harold"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_base_stats(max_hp=15, max_mana=0, p_armor=3, m_armor=0)
    creature.set_misc_stats(max_ap=2, speed=3, vision_radius=5)
    creature.set_attack_stats(attack_min=3, attack_max=4)
    creature.move_to(x, y)
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature

  def new_mushroom(self, x, y):
    name = "Mushroom"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Plant", self.world)
    creature.set_ai(ai.Plant(creature))
    creature.set_base_stats(max_hp=5, max_mana=0, p_armor=0, m_armor=1)
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
    creature.move_to(x, y)
    self.world.add_creature(creature)
    return creature
