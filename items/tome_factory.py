from items.item import Tome
from spells.spell_factory import SpellFactory
from tileset import TileSet

class TomeFactory:
  def __init__(self, tileset: TileSet, spell_factory: SpellFactory):
    self.tileset = tileset
    self.spells = spell_factory
    self.cache = {}

  def tome_of_embers(self):
    name = "Tome of Embers"
    if name in self.cache:
      return self.cache[name]
    tome = Tome(name, self.tileset.get_item(name), self.spells.embers())
    tome.set_description("A tome containing knowledge of the basic Embers fire spell.")
    self.cache[name] = tome
    return tome

  def tome_of_flame_lash(self):
    name = "Tome of Flame Lash"
    if name in self.cache:
      return self.cache[name]
    tome = Tome(name, self.tileset.get_item(name), self.spells.flame_lash())
    tome.set_description("A tome containing knowledge of the Flame Lash fire spell.")
    self.cache[name] = tome
    return tome
