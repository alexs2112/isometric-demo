from skills.effect import Effect
from creatures.creature import Creature
import skills.effect_functions as func

class EffectFactory:
  def minor_heal(self, multiple_of_max):
    effect = Effect("Minor Heal", 0)
    effect.add_start(func.get_heal_function(multiple_of_max))
    return effect

  def regenerate(self, duration, multiple_of_max):
    effect = Effect("Regenerating", duration)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + " begins to regenerate!"))
    effect.add_start(func.get_heal_function(multiple_of_max))
    effect.add_tick(func.get_heal_function(multiple_of_max))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + " stops regenerating."))
    return effect
  
  def burning(self):
    effect = Effect("Burning", 4)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + " catches fire!"))
    effect.add_start(func.get_damage_function(1, 2, "fire", "Burning"))
    effect.add_tick(func.get_damage_function(1, 1, "fire", "Burning"))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + " puts out the flames."))
    return effect
  
  def stunned(self, duration):
    effect = Effect("Stunned", duration)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + " becomes stunned!"))
    effect.add_tick(lambda _, creature: creature.notify_player(creature.name + " is stunned!"))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + " shakes off the stun."))
    return effect

  def rapid_slashes(self, duration):
    effect = Effect("Rapid Slashes", duration)
    effect.add_start(lambda _, creature: creature.modify_unarmed_cost(-1))
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + "'s unarmed attacks quicken"))
    effect.add_end(lambda _, creature: creature.modify_unarmed_cost(1))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + "'s unarmed attacks return to normal"))
    return effect

  def modify_resistance(self, type, value, duration):
    name = type.capitalize()
    if value > 0:
      name += " Resistance"
      s1 = " becomes resistant to " + type + " damage."
      s2 = " loses its resistance to " + type + " damage."
    else:
      name += " Vulnerability"
      s1 = " becomes vulnerable to " + type + " damage."
      s2 = " loses its vulnerability to " + type + " damage."
    effect = Effect(name, duration)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + s1))
    effect.add_start(lambda _, creature: creature.modify_resistance(type, value))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + s2))
    effect.add_end(lambda _, creature: creature.modify_resistance(type, -value))
    return effect
  
  def poisoned(self, duration):
    effect = Effect("Poisoned", duration)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + " is poisoned!"))
    effect.add_tick(func.get_damage_function(1, 2, "poison", "Poisoned"))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + " is no longer poisoned"))
    return effect

  def toxic_spores(self, duration):
    effect = Effect("Spores", duration)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + " inhales the spores!"))
    effect.add_tick(func.get_damage_function(1, 2, "poison", "Spores"))
    return effect
