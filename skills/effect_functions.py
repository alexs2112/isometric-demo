import random
from skills.effect import Effect
from creatures.creature import Creature

# All functions should take exactly two parameters
# effect: Effect
# creature: Creature

# Heals a creature for a multiple of their max HP
def get_heal_function(max_health_multiple):
  def func(effect: Effect, creature: Creature):
    amount = round(creature.get_max_hp() * max_health_multiple)
    creature.heal(amount)
  return func

def get_damage_function(min, max, type, source_name):
  def func(effect: Effect, creature: Creature):
    damage = random.randint(min, max)
    damage_string = str(damage - creature.get_resistance(type))
    creature.notify_player(creature.name + " takes " + damage_string + " " + type + " damage! [" + source_name + "]")
    creature.take_damage(damage, type)
  return func
