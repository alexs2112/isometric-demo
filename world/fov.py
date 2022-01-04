import helpers

# A 2d list that simply stores True if a tile has been seen, or False if it has not
class FieldOfView(list):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    for _ in range(width):
      col = []
      for _ in range(height):
        col.append(False)
      self.append(col)

  def contains(self, x, y):
    return self[x][y]

  def update(self, world, creature):
    for x in range(-creature.vision_radius, creature.vision_radius + 1):
      for y in range(-creature.vision_radius, creature.vision_radius + 1):
        to_x, to_y = creature.x + x, creature.y + y
        if to_x < 0 or to_y < 0 or to_x >= self.width or to_y >= self.height:
          continue

        if self[to_x][to_y]:
          continue

        # If a player can see a floor they can see the walls adjacent to it, so we dont get weird visual errors of "floating" walls
        # Activate any new creatures the player has seen
        if creature.can_see(to_x, to_y):
          if world.is_floor(to_x, to_y):
            self[to_x][to_y] = True
            c = world.get_creature_at_location(to_x, to_y)
            if c:
              c.activate(creature)
              creature.notify("You see a " + c.name)
            if world.is_wall(to_x - 1, to_y):
              self[to_x-1][to_y] = True
            if world.is_wall(to_x, to_y - 1):
              self[to_x][to_y-1] = True
            if world.is_wall(to_x - 1, to_y - 1):
              self[to_x-1][to_y-1] = True
  
  def print(self):
    for y in range(self.height):
      for x in range(self.width):
        if self[x][y] == True:
          c = '0'
        else:
          c = '1'
        print(c, end='')
      print()

def can_see(world, sx, sy, dx, dy, radius):
    if (sx - dx) * (sx - dx) + (sy - dy) * (sy - dy) > radius * radius:
      return False

    l = helpers.get_line(sx, sy, dx, dy)
    for p_x, p_y in l:
      if world.is_floor(p_x, p_y) or (p_x == dx and p_y == dy):
        continue
      return False
    return True