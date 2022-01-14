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
    
    # What each player can currently see, to darken tiles outside of FOV
    self.current = []
    self.reset_current()

  def reset_current(self):
    self.current = []
    for _ in range(self.width):
      col = []
      for _ in range(self.height):
        col.append(False)
      self.current.append(col)

  def contains(self, x, y):
    return self[x][y]
  
  def can_see(self, x, y):
    return self.current[x][y]

  # Add new tiles to the remembered FOV, and then recalculate the current tiles each player can see
  def update(self, world, creature):
    for x in range(-creature.vision_radius, creature.vision_radius + 1):
      for y in range(-creature.vision_radius, creature.vision_radius + 1):
        to_x, to_y = creature.x + x, creature.y + y
        if to_x < 0 or to_y < 0 or to_x >= self.width or to_y >= self.height:
          continue

        if self[to_x][to_y]:
          continue

        # If a player can see a floor they can see the walls adjacent to it, so we dont get weird visual errors of "floating" walls
        if creature.can_see(to_x, to_y):
          if world.is_floor(to_x, to_y):
            self[to_x][to_y] = True
            if world.is_wall(to_x - 1, to_y):
              self[to_x-1][to_y] = True
            if world.is_wall(to_x, to_y - 1):
              self[to_x][to_y-1] = True
            if world.is_wall(to_x - 1, to_y - 1):
              self[to_x-1][to_y-1] = True

    self.reset_current()
    for p in world.players:
      self.update_current(p)
  
  def update_current(self, creature):
    for x in range(-creature.vision_radius, creature.vision_radius + 1):
      for y in range(-creature.vision_radius, creature.vision_radius + 1):
        to_x, to_y = creature.x + x, creature.y + y
        if to_x < 0 or to_y < 0 or to_x >= self.width or to_y >= self.height:
          continue

        if self.current[to_x][to_y]:
          continue
      
        if creature.can_see(to_x, to_y):
          self.current[to_x][to_y] = True

          # If you see a non-active creature, activate all enemies in the room
          c = creature.world.get_creature_at_location(to_x, to_y)
          if c and c.can_be_activated() and not c.is_active():
            if c.home_room:
              c.world.activate_room_enemies(c.home_room, creature)
            else:
              c.activate(creature)
              s = "You see a " + c.name
              w = c.equipment.slot("Main")
              if w:
                s += " wielding a " + w.name
              creature.notify(s)
  
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