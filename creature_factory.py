import ai
from creature import Creature
from tileset import TileSet
from world_builder import World

class CreatureFactory:
  def __init__(self, world: World, tileset: TileSet):
    self.world = world
    self.tileset = tileset

  def new_edward(self, x, y):
    name = "Edward"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_stats(max_hp=10, attack=3)
    creature.set_misc_stats(max_ap=3, speed=3, vision_radius=5)
    creature.move_to(x, y)
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature

  def new_goobert(self, x, y):
    name = "Goobert"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_stats(max_hp=10, attack=3)
    creature.set_misc_stats(max_ap=3, speed=3, vision_radius=5)
    creature.move_to(x, y)
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature
  
  def new_wizard(self, x, y):
    name = "Wizard"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_stats(max_hp=10, attack=3)
    creature.set_misc_stats(max_ap=3, speed=3, vision_radius=5)
    creature.move_to(x, y)
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature
  
  def new_harold(self, x, y):
    name = "Harold"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Player", self.world)
    creature.set_stats(max_hp=10, attack=3)
    creature.set_misc_stats(max_ap=3, speed=3, vision_radius=5)
    creature.move_to(x, y)
    self.world.add_creature(creature)
    self.world.update_fov(creature)
    return creature

  def new_mushroom(self, x, y):
    name = "Mushroom"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Plant", self.world)
    creature.set_ai(ai.Plant(creature))
    creature.set_stats(max_hp=5, attack=0)
    creature.set_misc_stats(max_ap=0, speed=0, vision_radius=0)
    creature.move_to(x, y)
    self.world.add_creature(creature)
    return creature
  
  def new_skeleton(self, x, y):
    name = "Skeleton"
    icon = self.tileset.get_creature(name)
    creature = Creature(name, icon, "Undead", self.world)
    creature.set_ai(ai.Basic(creature))
    creature.set_stats(max_hp=8, attack=3)
    creature.set_misc_stats(max_ap=3, speed=2, vision_radius=5)
    creature.move_to(x, y)
    self.world.add_creature(creature)
    return creature
