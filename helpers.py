from pathfinder import Path

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
