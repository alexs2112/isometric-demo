import random
from spells.effect_factory import EffectFactory
from sprites.tileset import TileSet
from items.item import Potion
from creatures.creature import Creature

class PotionFactory:
  def __init__(self, tileset: TileSet, effect: EffectFactory):
    self.tileset = tileset
    self.effect = effect
    self.cache = {}

  def potion_minor_healing(self):
    name = "Potion of Minor Healing"
    if name in self.cache:
      return self.cache[name]
    item = Potion(name, self.tileset.get_item(name))
    item.set_description("A magical healing elixir which causes minor wounds to close and heal almost instantly, doing little to heal more extensive injury.")
    item.set_effect(self.effect.minor_heal())
    self.cache[name] = item
    return item
  
  def potion_regeneration(self):
    name = "Potion of Regeneration"
    if name in self.cache:
      return self.cache[name]
    item = Potion(name, self.tileset.get_item(name))
    item.set_description("A glittering potion that increases the rate of ones natural healing ability, removing injury over a far shorter time period than one would expect.")
    item.set_effect(self.effect.regenerate())
    self.cache[name] = item
    return item
  