from items.item import Tome
from skills.skill_factory import SkillFactory
from sprites.tileset import TileSet

class TomeFactory:
  def __init__(self, tileset: TileSet, skill_factory: SkillFactory):
    self.tileset = tileset
    self.skills = skill_factory
    self.cache = {}

  def tome_of_embers(self):
    name = "Tome of Embers"
    if name in self.cache:
      return self.cache[name]
    tome = Tome(name, self.tileset.get_item(name), self.skills.embers())
    tome.set_description("A tome containing knowledge of the basic Embers fire skill.")
    self.cache[name] = tome
    return tome

  def tome_of_flame_lash(self):
    name = "Tome of Flame Lash"
    if name in self.cache:
      return self.cache[name]
    tome = Tome(name, self.tileset.get_item(name), self.skills.flame_lash())
    tome.set_description("A tome containing knowledge of the Flame Lash fire skill.")
    self.cache[name] = tome
    return tome
