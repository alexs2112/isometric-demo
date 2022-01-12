import random
from world.world_builder import World
from creatures.creature import Creature

# Basic class to override
class AI:
  def __init__(self, creature: Creature):
    self.creature = creature
    self.move_to = None       # The tile this creature is actively moving to
    self.active = False       # If the creature is actively hunting a player
    # We could also point self.world = self.creature.world here, but it could be useful to have world as a param in other methods?
  
  def can_activate(self):
    return True

  def activate(self, creature=None):
    self.active = True

  def is_active(self):
    return self.active

  # Returns if this creatures turn is complete after making this move
  def take_turn(self, world: World):
    return True
  
  def get_players_in_los(self, world: World):
    players = []
    x,y,r = self.creature.x, self.creature.y, self.creature.vision_radius
    for p in world.players:
      if p.x >= x - r and p.x <= x + r and p.y >= y - r and p.y <= y + r:
        if self.creature.can_see(p.x, p.y):
          players.append(p)
    random.shuffle(players)
    return players
  
  def get_closest_player(self, world: World):
    players = self.get_players_in_los(world)
    if len(players) == 0:
      return
    
    paths = []
    for p in players:
      p = self.creature.get_path_to(p.x, p.y)
      if p:
        paths.append(p)
    
    length = 100
    shortest_i = -1
    for i in range(len(paths)):
      l = len(paths[i])
      if l < length:
        length = l
        shortest_i = i
    
    return players[shortest_i]
  
  def get_home_tile(self, world: World):
    if self.creature.home_room:
      return world.get_random_floor_in_room(self.creature.home_room)
    else:
      return None

# Does nothing each turn
class Plant(AI):
  def can_activate(self):
    return False

# Simple turn logic:
# - If we can see a player, move as close as possible and try to attack it if we have AP
# - If we can't see a player, move to where we last saw the player
# - If we can't and haven't seen a player, move back home
# If we can see or are pursuing a player, we are active
class Basic(AI):
  def take_turn(self, world: World):
    if self.move_to and self.creature.x == self.move_to[0] and self.creature.y == self.move_to[1]:
      self.move_to = None
    
    p: Creature = self.get_closest_player(world)
    if p:
      self.activate(p)
    elif not self.move_to:
      self.active = False
      self.move_to = self.get_home_tile(world)
      if not self.move_to:
        return True

    if p and abs(self.creature.x - p.x) <= self.creature.get_attack_range() and abs(self.creature.y - p.y) <= self.creature.get_attack_range():
      if self.creature.ap >= self.creature.get_attack_cost():
        self.creature.attack_creature(p)
      else:
        return True
    else:
      path = self.creature.get_path_to(self.move_to[0], self.move_to[1])
      if not path:
        return True
      x,y = path[0]
      self.creature.move(x,y)
    
    if self.creature.free_movement == 0 and self.creature.ap == 0:
      return True
    return False

  def activate(self, creature=None):
    super().activate()

    if creature:
      self.move_to = (creature.x, creature.y)
      

