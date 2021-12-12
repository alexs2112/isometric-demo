import random, maze_gen, dungeon_gen
FLOOR = 0
WALL = 1

# Fill a world of the specified dimensions with walls and return it
def make_empty_world(width, height):
  world = []
  for x in range(width):
    col = []
    for y in range(height):
      col.append(WALL)
    world.append(col)
  return world

def generate_maze(world, width, height):
  return maze_gen.generate_maze(world, width, height)

def generate_dungeon(world, width, height, rooms):
  # Will generate at most the number of rooms specified, constrained by world size
  return dungeon_gen.generate_dungeon(world, width, height, rooms)

# Return a tuple of the (width, height) of the world
def world_dimensions(world):
  return len(world), len(world[0])

# A simple algorithm, place a bunch of random squares in a world and return it
def place_rooms(world, rooms):
  width, height = world_dimensions(world)
  minsize, maxsize = 3, 7
  for i in range(rooms):
    x_start = random.randint(1, width - maxsize - 2)
    y_start = random.randint(1, height - maxsize - 2)
    x_len = random.randint(minsize, maxsize)
    y_len = random.randint(minsize, maxsize)
    for x in range(x_start, x_start + x_len):
      for y in range(y_start, y_start + y_len):
        world[x][y] = FLOOR
  return world

# Simply print the world to the terminal
def print_world(world):
  width, height = world_dimensions(world)
  for y in range(height):
    for x in range(width):
      print(str(world[x][y]), end='')
    print()
    
  print()

def is_floor(world, x, y):
  width, height = world_dimensions(world)
  if x < 0 or y < 0 or x >= width or y >= height:
    return False
  if world[x][y] == FLOOR:
    return True
  return False

def is_wall(world, x, y):
  return not is_floor(world, x, y)

def get_floor_tile(world):
  width, height = world_dimensions(world)
  attempts = 1000
  while attempts > 0:
    attempts -= 1
    x = random.randint(0, width-1)
    y = random.randint(0, height-1)
    if world[x][y] == FLOOR:
      return x, y

  # Honestly this shouldnt happen but right now the maze generator just sometimes just doesn't make a maze
  raise Exception("Could not find an empty floor tile in world!")
