from skills.effect import Effect
from creatures.creature import Creature
import skills.effect_functions as func
from sprites.tileset import TileSet

class EffectFactory:
  def __init__(self, tileset: TileSet):
    self.tileset = tileset

  def minor_heal(self, multiple_of_max):
    effect = Effect("Minor Heal", self.tileset.get_effect_icons("Regenerating"), self.tileset.get_effect_sprites("Regenerating"), 0)
    effect.add_start(func.get_heal_function(multiple_of_max))
    return effect

  def regenerate(self, duration, multiple_of_max):
    name = "Regenerating"
    effect = Effect(name, self.tileset.get_effect_icons(name), self.tileset.get_effect_sprites(name), duration)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + " begins to regenerate!"))
    effect.add_start(func.get_heal_function(multiple_of_max))
    effect.add_tick(func.get_heal_function(multiple_of_max))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + " stops regenerating."))
    return effect
  
  def burning(self):
    name = "Burning"
    effect = Effect(name, self.tileset.get_effect_icons(name), self.tileset.get_effect_sprites(name), 4)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + " catches fire!"))
    effect.add_start(func.get_damage_function(1, 2, "fire", "Burning"))
    effect.add_tick(func.get_damage_function(1, 1, "fire", "Burning"))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + " puts out the flames."))
    return effect
  
  def stunned(self, duration):
    name = "Stunned"
    effect = Effect(name, self.tileset.get_effect_icons(name), self.tileset.get_effect_sprites(name), duration)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + " becomes stunned!"))
    effect.add_tick(lambda _, creature: creature.notify_player(creature.name + " is stunned!"))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + " shakes off the stun."))
    return effect

  def rapid_slashes(self, duration):
    name = "Rapid Slashes"
    effect = Effect(name, self.tileset.get_effect_icons(name), self.tileset.get_effect_sprites(name), duration)
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
    effect = Effect(name, self.tileset.get_effect_icons(name), self.tileset.get_effect_sprites(name), duration)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + s1))
    effect.add_start(lambda _, creature: creature.modify_resistance(type, value))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + s2))
    effect.add_end(lambda _, creature: creature.modify_resistance(type, -value))
    return effect
  
  def poisoned(self, duration):
    name = "Poisoned"
    effect = Effect(name, self.tileset.get_effect_icons(name), self.tileset.get_effect_sprites(name), duration)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + " is poisoned!"))
    effect.add_tick(func.get_damage_function(1, 2, "poison", "Poisoned"))
    effect.add_end(lambda _, creature: creature.notify_player(creature.name + " is no longer poisoned"))
    return effect

  def toxic_spores(self, duration):
    name = "Spores"
    effect = Effect(name, self.tileset.get_effect_icons(name), self.tileset.get_effect_sprites(name), duration)
    effect.add_start(lambda _, creature: creature.notify_player(creature.name + " inhales the spores!"))
    effect.add_tick(func.get_damage_function(1, 2, "poison", "Spores"))
    return effect
