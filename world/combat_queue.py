class CombatQueue:
  def __init__(self, world_creatures):
    self.creatures = []
    self.index = 0
    for c in world_creatures:
      if self.is_valid(c):
        self.creatures.append(c)
    # Sort self.creatures by initiative

  def add_creature(self, creature):
    if creature not in self.creatures:
      self.creatures.append(creature)
      # Sort self.creatures by initiative

  def remove_creature(self, creature):
    if creature in self.creatures:
      i = self.creatures.index(creature)
      if i <= self.index:
        self.index -= 1
      self.creatures.remove(creature)
  
  def get_current_creature(self):
    return self.creatures[self.index]

  def get_next_creature(self):
    self.index = (self.index + 1) % len(self.creatures)
    c = self.get_current_creature()
    if not self.is_valid(c):
      self.remove_creature(c)
      return self.get_next_creature()
    return c

  def is_valid(self, creature):
    return creature.is_player() or creature.is_active()
