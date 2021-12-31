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
