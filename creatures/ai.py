import random
from world.world_builder import World
from creatures.creature import Creature
from helpers import get_line

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

  def get_skills_in_range(self, range):
    if range < 0:
      return []
    out = []
    for s in self.creature.get_castable_skills():
      if s.get_range() >= range:
        out.append(s)
    return out

# Simple turn logic:
# - If we can see a player, move within range of our basic attack or ability and try to attack or cast if able
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

    # Try to cast a skill if we can
    if p: skills = self.get_skills_in_range(self.creature.simple_distance_to(p.x, p.y))
    if p and skills:
      s = random.choice(skills)
      tiles = s.get_target_tiles(self.creature.x, self.creature.y, p.x, p.y)
      creatures = self.creature.world.creature_location_dict()
      targets = []
      for t in tiles:
        if t in creatures:
          c = creatures[t]
          if not s.friendly_fire:
            if not c.is_player:
              continue
          targets.append(creatures[t])
      s.cast(self.creature, targets)
    elif p and self.creature.simple_distance_to(p.x, p.y) <= self.creature.get_attack_range():
      if self.creature.ap >= self.creature.get_attack_cost():
        self.creature.attack_creature(p)

        w = self.creature.get_main_hand()
        if w:
          if w.projectile:
            attack_path = get_line(self.creature.x, self.creature.y, p.x, p.y)
            self.creature.world.add_projectile_path(w.projectile, attack_path)
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

class Mushroom(AI):
  def take_turn(self, world: World):
    p: Creature = self.get_closest_player(world)
    if p:
      self.active = True
      skills = self.get_skills_in_range(self.creature.simple_distance_to(p.x, p.y))
      if skills:
        s = skills[0]
        s.cast(self.creature, [p])
      else:
        # Random flavour when the mushroom doesn't do anything on its turn
        self.creature.notify_player(self.creature.name + " " + random.choice(["shudders", "quivers", "trembles", "shakes", "vibrates", "jerks", "twitches", "spasms"]))
    else:
      self.active = False
    return True
