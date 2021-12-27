import line, fov, math

class Creature:
  def __init__(self, name, icon):
    self.name = name
    self.icon = icon

  def set_misc_stats(self, max_ap, speed, vision_radius):
    self.max_ap = max_ap
    self.ap = max_ap
    self.speed = speed
    self.vision_radius = vision_radius
    self.free_movement = 0  # The remaining moves after moving, so moves arent "wasted"

  def upkeep(self):
    self.ap = self.max_ap
    self.free_movement = 0

  def move_relative(self, world, dx, dy):
    if world.is_floor(self.x + dx, self.y + dy):
      self.x += dx
      self.y += dy

  def move_to(self, world, x, y):
    if world.is_floor(x, y):
      self.x = x
      self.y = y

  def get_possible_distance(self):
    return self.speed * self.ap + self.free_movement

  def move_along_path(self, world, path):
    path = path[:self.get_possible_distance()]
    distance = len(path)
    if distance == 0:
      return
    for (x,y) in path:
      self.move_to(world, x, y)
      world.update_fov(self)
    remaining_distance = max(0, distance - self.free_movement)
    self.free_movement = max(0, self.free_movement - distance)
    self.ap -= math.ceil(remaining_distance / self.speed)
    rem = (remaining_distance % self.speed)
    if rem > 0:
      self.free_movement += self.speed - rem
    
  
  def can_see(self, world, to_x, to_y):
    return fov.can_see(world, self.x, self.y, to_x, to_y, self.vision_radius)
