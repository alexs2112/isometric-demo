from spells.effect import Effect
from creatures.creature import Creature
import spells.effect_functions as func

class EffectFactory:
  def __init__(self):
    self.cache = {}

  def minor_heal(self):
    name = "Minor Heal"
    if name in self.cache:
      return self.cache[name]
    effect = Effect(name, 0)
    effect.add_start(func.get_heal_function(0.35))
    self.cache[name] = effect
    return effect

  def regenerate(self):
    name = "Regenerating"
    if name in self.cache:
      return self.cache[name]
    effect = Effect(name, 8)
    effect.add_start(lambda _, creature : creature.notify_player(creature.name + " begins to regenerate!"))
    effect.add_tick(func.get_heal_function(0.1))
    effect.add_end(lambda _, creature : creature.notify_player(creature.name + " stops regenerating."))
    self.cache[name] = effect
    return effect
  
  def burning(self):
    name = "Burning"
    if name in self.cache:
      return self.cache[name]
    effect = Effect(name, 4)
    effect.add_start(lambda _, creature : creature.notify_player(creature.name + " catches fire!"))
    effect.add_start(func.get_damage_function(1, 2, "magical", "Burning"))
    effect.add_tick(func.get_damage_function(1, 1, "magical", "Burning"))
    effect.add_end(lambda _, creature : creature.notify_player(creature.name + " puts out the flames."))
    self.cache[name] = effect
    return effect
