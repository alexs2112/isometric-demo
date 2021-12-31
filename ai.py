from world_builder import World
from creature import Creature

# Basic class to override
class AI:
  def __init__(self, creature: Creature):
    self.creature = creature
    # We could also point self.world = self.creature.world here, but it could be useful to have world as a param in other methods?
  
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

# Does nothing each turn
class Plant(AI):
  def take_turn(self, world: World):
    return

# Spends its turns getting as close as possible to the closest player and attacks them if able
class Basic(AI):
  def take_turn(self, world: World):
    p: Creature = self.get_closest_player(world)
    if p == None:
      return
    path = self.creature.get_path_to(p.x, p.y)[:-1]
    self.creature.move_along_path(path)

    if abs(self.creature.x - p.x) <= 1 and abs(self.creature.y - p.y) <= 1:
      self.creature.attack_creature(p)

    

