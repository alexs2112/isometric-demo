import random
from world.world_builder import World
from creatures.creature import Creature
from misc.helpers import get_line

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

  def upkeep(self, world: World):
    return
  
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

  def get_skills_in_range(self, range):
    if range < 0:
      return []
    out = []
    for s in self.creature.get_castable_skills():
      if s.get_range() >= range:
        out.append(s)
    return out

  def get_tiles_and_costs(self, self_range, cost_of_action):
    w = self.creature.world
    all_tiles = []
    for p in w.players:
      for mx in range(-self_range, self_range + 1):
        for my in range(-self_range, self_range + 1):
          if self.creature.can_enter(mx+p.x, my+p.y):
            all_tiles.append((mx + p.x, my + p.y))

    tiles = {}
    for (x,y) in all_tiles:

      # Remove the tile if we can't actually reach it
      distance = len(self.creature.get_path_to(x,y))
      if distance == 0 and (x != self.creature.x or y != self.creature.y):
        continue
      if distance > self.creature.get_possible_distance():
        continue

      if (x,y) in tiles:
        # Small negative for each player adjacent to the tile past the first
        # Change this later to be each player in range of the tile instead
        tiles[(x,y)] -= 2
      else:
        # Initial tile value is 0
        tiles[(x,y)] = 0

      if distance > (self.creature.ap - cost_of_action) * self.creature.get_speed() + self.creature.free_movement:
        # Very large negative if moving to the tile doesnt let us take an action
        tiles[(x,y)] -= 15

      if w.get_room_by_tile(x,y) == None:
        # Moderate negative if the tile is in a hallway
        tiles[(x,y)] -= 5
    return tiles
  
  def get_tile_to_move_to(self, self_range, cost_of_action):
    tiles = self.get_tiles_and_costs(self_range, cost_of_action)
    if not tiles:
      return []

    res = []
    highest_value = -100
    for (k, v) in tiles.items():
      if v > highest_value:
        res.clear()
        highest_value = v
      if v == highest_value:
        res.append(k)
    random.shuffle(res)
    return res[0]
  
  def get_max_range(self):
    r = self.creature.get_attack_range()
    for a in self.creature.get_castable_skills():
      if a.get_range() > r:
        r = a.get_range()
    return r

# Simple turn logic:
# - Pick a skill or basic attack that is in range of a player (including our movement)
# - Pick a tile to move to that is (hopefully) in range of a player
# - If we are standing on that tile, cast a skill or make an attack
class Basic(AI):
  def upkeep(self, world: World):
    self.move_to = None

  def take_turn(self, world: World):
    if not self.move_to:
      # A hardcoded AP cost of attacks and skills as 2 for now, otherwise this gets way more complicated
      max_range = self.get_max_range()
      self.move_to = self.get_tile_to_move_to(max_range, 2)
      if not self.move_to:
        self.move_to = self.creature.x, self.creature.y
    
    dx, dy = self.move_to
    if self.creature.x == dx and self.creature.y == dy:
      p: Creature = self.get_closest_player(world)
      # Try to cast a skill if we can
      if p: skills = self.get_skills_in_range(self.creature.simple_distance_to(p.x, p.y))
      if p and skills:
        s = random.choice(skills)
        tiles = s.get_target_tiles(self.creature.x, self.creature.y, p.x, p.y)
        s.cast(self.creature, tiles)
        return False
      elif p and self.creature.simple_distance_to(p.x, p.y) <= self.creature.get_attack_range():
        if self.creature.ap >= self.creature.get_attack_cost():
          self.creature.attack_creature(p)

          w = self.creature.get_main_hand()
          if w:
            if w.projectile:
              attack_path = get_line(self.creature.x, self.creature.y, p.x, p.y)
              self.creature.world.add_projectile_path(w.projectile, attack_path)
          return False
        return True
    else:
      # Otherwise, move to that tile
      p = self.creature.get_path_to(dx,dy)[:self.creature.get_possible_distance()]
      if not p:
        return True
      self.creature.move_along_path(p)
      return False
    
    # If we can't do anything, end the turn
    return True

  def activate(self, creature=None):
    super().activate()

    if creature:
      self.move_to = (creature.x, creature.y)

class Mushroom(AI):
  def take_turn(self, world: World):
    p: Creature = self.get_closest_player(world)
    if p:
      self.active = True
      skills = self.get_skills_in_range(self.creature.simple_distance_to(p.x, p.y))
      if skills:
        s = skills[0]
        s.cast(self.creature, [(p.x, p.y)])
      else:
        # Random flavour when the mushroom doesn't do anything on its turn
        self.creature.notify_player(self.creature.name + " " + random.choice(["shudders", "quivers", "trembles", "shakes", "vibrates", "jerks", "twitches", "spasms"]), (179, 185, 209))
    else:
      self.active = False
    return True
