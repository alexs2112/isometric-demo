import random, maze_gen, dungeon_gen
from tile import Tile
from fov import FieldOfView
FLOOR = 0
WALL = 1

class World:
  def __init__(self, initial_array):
    self.width = len(initial_array)
    self.height = len(initial_array[0])
    self.tiles = self.finalize_tiles(initial_array)
    self.fov = FieldOfView(self.width, self.height)
    self.creatures = []
    self.players = []   # A subset of creatures
    self.active_index = 0
    self.rooms = []
    self.start_room = None
    self.end_room = None

  def set_rooms(self, rooms):
    self.rooms = rooms
  
  def finalize_tiles(self, initial_array):
    from tileset import FLOOR_TILESETS, WALL_TILESETS # Kind of lazy here
    tiles = []
    for x in range(self.width):
      col = []
      for y in range(self.height):
        if initial_array[x][y] == FLOOR:
          col.append(Tile(True, random.randint(0, FLOOR_TILESETS-1)))
        else:
          col.append(Tile(False, random.randint(0, WALL_TILESETS-1)))
      tiles.append(col)
    return tiles

  def tile(self, x, y):
    return self.tiles[x][y]
  
  def dimensions(self):
    return self.width, self.height

  def outside_world(self, x, y):
    if x < 0 or y < 0 or x >= self.width or y >= self.height:
      return True
  
  def is_floor(self, x, y):
    if self.outside_world(x,y):
      return False
    if self.tile(x,y).is_floor():
      return True
    return False
  
  def is_wall(self, x, y):
    return not self.is_floor(x,y)
  
  def get_floor_coordinate(self):
    attempts = 1000
    while attempts > 0:
      attempts -= 1
      x = random.randint(0, self.width-1)
      y = random.randint(0, self.height-1)
      if self.is_floor(x,y) and not self.get_creature_at_location(x,y):
        return x, y

    # Honestly this shouldnt happen but right now the maze generator just sometimes just doesn't make a maze
    raise Exception("Could not find an empty floor tile in world!")
  
  def get_random_floor_in_room(self, room):
    x1, y1 = room.p1
    x2, y2 = room.p2

    attempts = 100
    while attempts > 0:
      attempts -= 1
      x = random.randint(x1, x2)
      y = random.randint(y1, y2)
      if self.is_floor(x,y) and not self.get_creature_at_location(x,y):
        return x, y

    raise Exception("Could not find an empty floor tile in world!")

  # Some wrapper methods around our field of view
  def update_fov(self, creature):
    self.fov.update(self, creature)
  
  def has_seen(self, x, y):
    return self.fov.contains(x,y)

  def add_creature(self, creature):
    self.creatures.append(creature)
    if creature.is_player():
      self.players.append(creature)

  def remove_creature(self, creature):
    if creature in self.creatures:
      i = self.creatures.index(creature)
      if i <= self.active_index:
        self.active_index -= 1
      self.creatures.remove(creature)
    if creature.is_player() and creature in self.players:
      self.players.remove(creature)
  
  def get_active_creature(self):
    return self.creatures[self.active_index]
  
  def get_next_active_creature(self):
    self.active_index = (self.active_index + 1) % len(self.creatures)
    active = self.get_active_creature()
    return active
  
  def creature_location_dict(self):
    locations = {}
    for c in self.creatures:
      locations[(c.x, c.y)] = c
    return locations
  
  def get_creature_at_location(self, x, y):
    for c in self.creatures:
      if c.x == x and c.y == y:
        return c
  
  # Simply print the world to the terminal
  def print_world(self):
    for y in range(self.height):
      for x in range(self.width):
        if self.is_floor(x,y):
          print(str(FLOOR), end='')
        else:
          print(str(WALL), end='')
      print()
    print()

class Room:
  def __init__(self, id, origin, p1, p2):
    self.id = id
    self.origin = origin
    self.p1 = p1          # The top left corner of the room
    self.p2 = p2          # The bottom right corner of the room
    self.neighbors = []
  
  def add_neighbor(self, room):
    self.neighbors.append(room)

# Fill a world of the specified dimensions with walls and return it
def make_empty_initial_array(width, height):
  world = []
  for _ in range(width):
    col = []
    for _ in range(height):
      col.append(WALL)
    world.append(col)
  return world

def generate_maze(width, height):
  initial_array = make_empty_initial_array(width, height)
  initial_array = maze_gen.generate_maze(initial_array, width, height)
  return World(initial_array)

# Will generate at most the number of rooms specified, constrained by world size
def generate_dungeon(width, height, rooms):
  initial_array = make_empty_initial_array(width, height)
  initial_array, rooms, start_room, end_room = dungeon_gen.generate_dungeon(initial_array, width, height, rooms)
  world = World(initial_array)
  world.set_rooms(rooms)
  world.start_room = start_room
  world.end_room = end_room
  return world

# A simple algorithm, place a bunch of random squares in a world and return it
def place_rooms(rooms, width, height):
  initial_array = make_empty_initial_array(width, height)
  minsize, maxsize = 3, 7
  for i in range(rooms):
    x_start = random.randint(1, width - maxsize - 2)
    y_start = random.randint(1, height - maxsize - 2)
    x_len = random.randint(minsize, maxsize)
    y_len = random.randint(minsize, maxsize)
    for x in range(x_start, x_start + x_len):
      for y in range(y_start, y_start + y_len):
        initial_array[x][y] = FLOOR
  return World(initial_array)

def only_floors(width, height):
  world = []
  for _ in range(width):
    col = []
    for _ in range(height):
      col.append(FLOOR)
    world.append(col)
  return World(world)
