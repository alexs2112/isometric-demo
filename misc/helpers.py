from typing_extensions import Annotated
from creatures.pathfinder import Path

def get_isometric_position(cart_x, cart_y):
  return cart_x - cart_y, int((cart_x + cart_y) / 2)

def get_cartesian_position(iso_x, iso_y):
  return int((2 * iso_y + iso_x) / 2), int((2 * iso_y - iso_x) / 2)

def get_tile_position(offset_x, offset_y, cart_x, cart_y):
  # cart_x, cart_y are in pixels, not tile coords
  x, y = get_isometric_position(cart_x, cart_y)
  return x - offset_x, y - offset_y

def get_mouse_tile(offset_x, offset_y, mouse_x, mouse_y):
  mouse_x += offset_x
  mouse_y += offset_y
  mouse_x -= 32         # Half the width of a tile
  return get_cartesian_position(mouse_x / 32, mouse_y / 32)

def is_nw_wall(world, x, y):
  width, _ = world.dimensions()
  if x >= width - 1 or x < 0:
    return False
  return world.is_wall(x,y) and world.is_floor(x+1,y)

def is_ne_wall(world, x, y):
  _, height = world.dimensions()
  if y >= height-1 or y < 0:
    return False
  return world.is_wall(x,y) and world.is_floor(x,y+1)

def is_outer_corner(world, x, y):
  width, height = world.dimensions()
  if y < height - 1 and x < width - 1:
    if world.is_wall(x,y) and world.is_floor(x+1,y+1):
      if world.is_wall(x+1,y) and world.is_wall(x,y+1):
        return True
  return False

def get_path_between_points(world, sx, sy, dx, dy):
  if world.outside_world(dx,dy) or not (world.is_floor(dx,dy) and world.has_seen(dx,dy)):
    return []

  path = Path(world, sx, sy, dx, dy).points
  return path

def get_line(x0, y0, x1, y1):
  points = []
  
  dx = abs(x1 - x0)
  dy = abs(y1 - y0)
  
  sx = 1 if x0 < x1 else -1
  sy = 1 if y0 < y1 else -1
  err = dx - dy

  while True:
    points.append((x0, y0))
    if x0 == x1 and y0 == y1:
      break

    e2 = err * 2

    if e2 > -dy:
      err -= dy
      x0 += sx
    if e2 < dx:
      err += dx
      y0 += sy
  return points

def get_line_no_diagonal(x0, y0, x1, y1):
  points = []
  
  dx = abs(x1 - x0)
  dy = abs(y1 - y0)
  
  sx = 1 if x0 < x1 else -1
  sy = 1 if y0 < y1 else -1
  err = dx - dy

  while True:
    points.append((x0, y0))
    if x0 == x1 and y0 == y1:
      break

    e2 = err * 2

    if e2 >= -dy:
      err -= dy
      x0 += sx
    elif e2 < dx:
      err += dx
      y0 += sy
  return points

# Using a projectile and a tile path, return a list of tuples of [((x,y), projectile.image)]
# To be fed into world so we can get the correct "image" at each frame
def get_projectile_path(projectile, tile_path):
  result = []
  for i in range(len(tile_path)):
    (x,y) = tile_path[i]
    if projectile.all:
      result.append(((x,y), projectile.all))
    elif i == len(tile_path) - 1:
      if projectile.target:
        if type(projectile.target) == list:
          for image in projectile.target:
            result.append(((x,y), image))
        else:
          result.append(((x,y), projectile.target))
    else:
      (x2,y2) = tile_path[i+1]
      if x == x2:
        if y > y2:
          image = projectile.ne
        else:
          image = projectile.sw
      elif y == y2:
        if x > x2:
          image = projectile.nw
        else:
          image = projectile.se
      elif x > x2:
        if y > y2:
          image = projectile.n
        else:
          image = projectile.w
      else:
        if y > y2:
          image = projectile.e
        else:
          image = projectile.s
      if image:
        result.append(((x,y), image))
  return result
