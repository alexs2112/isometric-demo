from abilities.effect import Effect
from creatures.creature import Creature
import abilities.effect_functions as func

class EffectFactory:
  def __init__(self):
    self.cache = {}

  def minor_heal(self):
    name = "Minor Heal"
    if name in self.cache:
      return self.cache[name]
    effect = Effect(name, 0)
    effect.set_start(func.minor_heal)
    return effect

  def regenerate(self):
    name = "Regenerate"
    if name in self.cache:
      return self.cache[name]
    effect = Effect(name, 8)
    effect.set_start(lambda _, creature : creature.notify_player(creature.name + " begins to regenerate!"))
    effect.set_tick(func.tiny_heal)
    effect.set_end(lambda _, creature : creature.notify_player(creature.name + " stops regenerating."))
    return effect