from world.world_builder import World
from creatures.creature import Creature

# Basic class to override
class AI:
  def __init__(self, creature: Creature):
    self.creature = creature
    self.move_to = None       # The tile this creature is actively moving to
    self.active = False       # If the creature is actively hunting a player
    # We could also point self.world = self.creature.world here, but it could be useful to have world as a param in other methods?
  
  def activate(self):
    self.active = True

  def take_turn(self, world: World):
    return
  
  def get_players_in_los(self, world: World):
    players = []
    x,y,r = self.creature.x, self.creature.y, self.creature.vision_radius
    for p in world.players:
      if p.x >= x - r and p.x <= x + r and p.y >= y - r and p.y <= y + r:
        if self.creature.can_see(p.x, p.y):
          players.append(p)
    return players
  
  def get_closest_player(self, world: World):
    players = self.get_players_in_los(world)
    if len(players) == 0:
      return
    
    paths = []
    for p in players:
      paths.append(self.creature.get_path_to(p.x, p.y))
    
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
  def activate(self):
    # This is a plant, it cannot be activated
    return

# Simple turn logic:
# - If we can see a player, move as close as possible and try to attack it if we have AP
# - If we can't see a player, move to where we last saw the player
# - If we can't and haven't seen a player, move back home
# If we can see or are pursuing a player, we are active
class Basic(AI):
  def take_turn(self, world: World):
    if self.move_to and self.creature.x == self.move_to[0] and self.creature.y == self.move_to[1]:
      self.active = False
      self.move_to = None

    p: Creature = self.get_closest_player(world)
    if p:
      self.activate()
      self.move_to = (p.x, p.y)
    elif not self.move_to:
      self.move_to = self.get_home_tile(world)

    if not self.move_to:
      return

    path = self.creature.get_path_to(self.move_to[0], self.move_to[1])
    if world.get_creature_at_location(self.move_to[0], self.move_to[1]):
      path = path[:-1]
    self.creature.move_along_path(path)

    if p:
      if abs(self.creature.x - p.x) <= 1 and abs(self.creature.y - p.y) <= 1:
        self.creature.attack_creature(p)

  def activate(self, creature=None):
      super().activate()

      if creature:
        self.move_to = (creature.x, creature.y)
      

