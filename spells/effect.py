from creatures.creature import Creature
from world.world_builder import World

# A way to collect a bunch of different methods to affect a creature over time
class Effect:
  def __init__(self, name, duration):
    self.name = name
    self.duration = duration
    self.start = []
    self.end = []
    self.tick = []
  
  def add_start(self, func):
    self.start.append(func)
  
  def add_end(self, func):
    self.end.append(func)
  
  def add_tick(self, func):
    self.tick.append(func)
  
  def clone(self):
    new = Effect(self.name, self.duration)
    new.start = self.start
    new.end = self.end
    new.tick = self.tick
    return new

  def apply(self, creature: Creature):
    c = self.clone()
    if self.duration > 0:
      creature.effects.append(c)
    
    for f in self.start:
      f(self, creature)

  def update(self, creature: Creature):
    for f in self.tick:
      f(self, creature)
    self.duration -= 1
    if self.duration <= 0:
      self.remove(creature)

  def remove(self, creature: Creature):
    for f in self.end:
      f(self, creature)
    creature.effects.remove(self)
