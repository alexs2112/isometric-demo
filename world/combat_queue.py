class CombatQueue:
  def __init__(self, world_creatures):
    self.start_y = -72
    self.creatures = []
    self.index = 0
    for c in world_creatures:
      if self.is_valid(c):
        self.creatures.append(c)
    self.sort()

  def add_creature(self, creature):
    if creature not in self.creatures:
      self.creatures.append(creature)

  def remove_creature(self, creature):
    if creature in self.creatures:
      i = self.creatures.index(creature)
      if i <= self.index:
        self.index -= 1
      self.creatures.remove(creature)

  def sort(self):
    self.creatures.sort(key=lambda creature: creature.get_initiative(), reverse=True)
  
  def get_current_creature(self):
    return self.creatures[self.index]

  def get_next_creature(self):
    self.index = (self.index + 1) % len(self.creatures)
    if self.index == 0:
      # Sort the list at the start of each combat round
      self.sort()

    c = self.get_current_creature()
    if not self.is_valid(c):
      self.remove_creature(c)
      return self.get_next_creature()
    return c

  def is_valid(self, creature):
    return creature.is_player() or creature.is_active()

  def draw(self, screen, x, y):
    player_box = screen.tileset.get_ui("queue_box_player")
    enemy_box = screen.tileset.get_ui("queue_box_enemy")
    active_box = screen.tileset.get_ui("queue_box_active")
    unknown = screen.tileset.get_misc("unknown_creature_sprite")

    y += self.start_y
    if y < 0:
      self.start_y = min(self.start_y + 10, 0)
    for i in range(len(self.creatures)):
      c = self.creatures[i]
      if i == self.index:
        screen.blit(active_box, (x, y))
      elif c.is_player():
        screen.blit(player_box, (x, y))
      else:
        screen.blit(enemy_box, (x, y))

      if c.world.can_see(c.x, c.y):
        screen.blit(c.get_sprite(64), (x+4, y+4))
      else:
        screen.blit(unknown, (x+4, y+4))
      x += 72
