import math, random
import world.fov as fov
from creatures.pathfinder import Path
from world.world_builder import World

class Creature:
  # The absolute max amount of some expendable stats
  P_ARMOR_MAX = 5
  M_ARMOR_MAX = 5
  AP_MAX = 8

  def __init__(self, name, icon, faction, world: World):
    self.name = name
    self.icon = icon
    self.faction = faction
    self.world = world
    self.ai = None
    self.home_room = None

  def set_ai(self, ai):
    self.ai = ai

  def set_home_room(self, room):
    self.home_room = room

  def set_base_stats(self, max_hp, max_mana, p_armor, m_armor):
    self.max_hp = max_hp
    self.hp = max_hp
    self.max_mana = max_mana
    self.mana = max_mana
    self.p_armor_cap = p_armor
    self.m_armor_cap = m_armor
    self.p_armor = p_armor
    self.m_armor = m_armor

  def set_misc_stats(self, max_ap, speed, vision_radius):
    self.max_ap = max_ap
    self.ap = max_ap
    self.speed = speed
    self.vision_radius = vision_radius
    self.free_movement = 0  # The remaining moves after moving, so moves arent "wasted"
  
  def set_attack_stats(self, attack_min, attack_max, base_damage_type="physical", attack_cost=2):
    self.attack_min = attack_min
    self.attack_max = attack_max
    self.base_damage_type = base_damage_type
    self.attack_cost = attack_cost

  def upkeep(self):
    self.ap = self.max_ap
    self.free_movement = 0

  def take_turn(self):
    self.upkeep()
    if self.ai:
      self.ai.take_turn(self.world)

  def is_player(self):
    if self.faction == "Player":
      return True
    else:
      return False

  def can_enter(self, x, y):
    if self.world.is_floor(x, y) and not self.world.get_creature_at_location(x,y):
      return True

  def move_relative(self, dx, dy):
    if self.world.is_floor(self.x + dx, self.y + dy):
      self.x += dx
      self.y += dy

  def move_to(self, x, y):
    if self.world.is_floor(x, y):
      self.x = x
      self.y = y

  def get_possible_distance(self):
    return self.speed * self.ap + self.free_movement

  def get_path_to(self, dx, dy):
    if self.world.outside_world(dx,dy) or not (self.world.is_floor(dx,dy) and self.world.has_seen(dx,dy)):
      return []

    path = Path(self, dx, dy).points
    return path

  def move_along_path(self, path):
    path = path[:self.get_possible_distance()]
    distance = len(path)
    if distance == 0:
      return
    if self.is_player():
      for (x,y) in path:
        self.move_to(x, y)
        self.world.update_fov(self)
    else:
      x,y = path[-1]
      self.move_to(x, y)
    remaining_distance = max(0, distance - self.free_movement)
    self.free_movement = max(0, self.free_movement - distance)
    self.ap -= math.ceil(remaining_distance / self.speed)
    rem = (remaining_distance % self.speed)
    if rem > 0:
      self.free_movement += self.speed - rem
  
  def can_see(self, to_x, to_y):
    return fov.can_see(self.world, self.x, self.y, to_x, to_y, self.vision_radius)

  def take_damage(self, damage, type):
    if type == "physical":
      amount = max(0, damage - self.p_armor)
      self.p_armor = max(0, self.p_armor - damage)
    elif type == "magical":
      amount = max(0, damage - self.m_armor)
      self.m_armor = max(0, self.m_armor - damage)
    self.hp -= amount
    if self.hp <= 0:
      print(self.name + " dies!")
      self.world.remove_creature(self)

  def attack_creature(self, target):
    if self.ap < self.attack_cost:
      print(self.name + " does not have enough AP to attack!")
      return
    self.ap -= self.attack_cost

    # Damage will be weighted towards the average
    damage = random.randint(self.attack_min, self.attack_max) + random.randint(self.attack_min, self.attack_max)
    damage = int(damage/2)
    print(self.name + " attacks " + target.name + " for " + str(damage) + " " + self.base_damage_type + " damage!")
    target.take_damage(damage, self.base_damage_type)
