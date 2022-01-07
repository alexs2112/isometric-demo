from abilities.effect import Effect
from creatures.creature import Creature

# All functions should take exactly two parameters
# effect: Effect
# creature: Creature

# Heals a creature for 10% of their max HP
def tiny_heal(effect: Effect, creature: Creature):
  amount = round(creature.get_max_hp() * 0.1)
  creature.heal(amount)

# Heals a creature for 35% of their max HP
def minor_heal(effect: Effect, creature: Creature):
  amount = round(creature.get_max_hp() * 0.35)
  creature.heal(amount)
