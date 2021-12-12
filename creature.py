import line
from world_builder import world_dimensions, is_floor, is_wall, FLOOR, WALL

class Creature:
  def __init__(self, x, y, icon, vision_radius = 5):
    self.x = x
    self.y = y
    self.icon = icon
    self.vision_radius = vision_radius

  def move(self, dx, dy, world):
    if is_floor(world, self.x+dx, self.y+dy):
      self.x += dx
      self.y += dy
      self.update_fov(world)

  def initialize_fov(self, world):
    self.fov = []
    world_width, world_height = world_dimensions(world)
    for _ in range(world_width):
      col = []
      for _ in range(world_height):
        col.append(False)
      self.fov.append(col)
    self.update_fov(world)
  
  def update_fov(self, world):
    r = self.vision_radius
    world_width, world_height = world_dimensions(world)
    for x in range(-self.vision_radius, self.vision_radius):
      for y in range(-self.vision_radius, self.vision_radius):
        to_x, to_y = self.x + x, self.y + y
        if to_x < 0 or to_y < 0 or to_x >= world_width or to_y >= world_height:
          continue

        if self.has_seen(to_x, to_y):
          continue

        if self.can_see(world, to_x, to_y):
          # If a player can see a floor they can see the walls adjacent to it, so we dont get weird visual errors of "floating" walls
          if is_floor(world, to_x, to_y):
            self.fov[to_x][to_y] = True
            if is_wall(world, to_x - 1, to_y):
              self.fov[to_x-1][to_y] = True
            if is_wall(world, to_x, to_y - 1):
              self.fov[to_x][to_y-1] = True
            if is_wall(world, to_x - 1, to_y - 1):
              self.fov[to_x-1][to_y-1] = True

  def has_seen(self, x, y):
    return self.fov[x][y]
  
  def can_see(self, world, to_x, to_y):
    if (self.x - to_x) * (self.x - to_x) + (self.y - to_y) * (self.y - to_y) > self.vision_radius * self.vision_radius:
      return False

    l = line.get_line(self.x, self.y, to_x, to_y)
    for p_x, p_y in l:
      if world[p_x][p_y] == FLOOR or (p_x == to_x and p_y == to_y):
        continue
      return False
    return True
