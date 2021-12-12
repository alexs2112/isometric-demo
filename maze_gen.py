import random
FLOOR = 0
WALL = 1

def generate_maze(world, width, height):
  x = random.randint(1,width-1)
  y = random.randint(1,height-1)

  open_list = consider_tile(world, width, height, x, y)
  while open_list:
    tile_x, tile_y = open_list.pop()
    adj = consider_tile(world, width, height, tile_x, tile_y)
    open_list = open_list + adj

  return world
  
def free_space(map, width, height, x, y):
  # If this space is not a floor and is touching at least 2 other floor tiles to create a loop, return false
  # otherwise return true
  if x == 0 or x == width - 1 or y == 0 or y == height - 1:
    return False

  # Hardcoding each corner for now, fix this later
  if map[x-1][y-1] == FLOOR and map[x-1][y] == WALL and map[x][y-1] == WALL:
    return False
  if map[x+1][y-1] == FLOOR and map[x+1][y] == WALL and map[x][y-1] == WALL:
    return False
  if map[x-1][y+1] == FLOOR and map[x-1][y] == WALL and map[x][y+1] == WALL:
    return False
  if map[x+1][y+1] == FLOOR and map[x+1][y] == WALL and map[x][y+1] == WALL:
    return False

  adj_floors = 0
  for x_m, y_m in [(-1,0), (1,0), (0,-1), (0,1)]:
    if map[x+x_m][y+y_m] == FLOOR:
      if adj_floors >= 1:
        return False
      adj_floors += 1
  return True

def consider_tile(map, width, height, x, y):
  if not free_space(map, width, height, x, y):
    return []
  
  map[x][y] = FLOOR
  choices = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
  random.shuffle(choices)
  return choices