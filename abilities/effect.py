from creatures.creature import Creature
from world.world_builder import World

# A way to collect a bunch of different methods to affect a creature over time
class Effect:
  def __init__(self, name, duration):
    self.name = name
    self.duration = duration
    self.start = None
    self.end = None
    self.tick = None
  
  def set_start(self, func):
    self.start = func
  
  def set_end(self, func):
    self.end = func
  
  def set_tick(self, func):
    self.tick = func
  
  def clone(self):
    new = Effect(self.name, self.duration)
    new.set_start(self.start)
    new.set_end(self.end)
    new.set_tick(self.tick)
    return new

  def apply(self, creature: Creature):
    c = self.clone()
    if self.duration > 0:
      creature.effects.append(c)
    self.start(self, creature)

  def update(self, creature: Creature):
    self.tick(self, creature)
    self.duration -= 1
    if self.duration <= 0:
      self.remove(creature)

  def remove(self, creature: Creature):
    self.end(self, creature)
    creature.effects.remove(self)
