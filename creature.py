import line, fov

class Creature:
  def __init__(self, name, icon, vision_radius = 5):
    self.name = name
    self.icon = icon
    self.vision_radius = vision_radius

  def move(self, world, dx, dy):
    if world.is_floor(self.x + dx, self.y + dy):
      self.x += dx
      self.y += dy

  def move_to(self, world, x, y):
    if world.is_floor(x, y):
      self.x = x
      self.y = y
  
  def can_see(self, world, to_x, to_y):
    return fov.can_see(world, self.x, self.y, to_x, to_y, self.vision_radius)
