import random, math, line, dfs
 
FLOOR = 0
WALL = 1
ROOM_MIN_SIZE = 3
ROOM_MAX_SIZE = 7

def generate_dungeon(world, width, height, rooms):
  world, rooms = create_rooms(world, width, height, rooms)
  world = place_hallways(world, rooms)
  return world

def create_rooms(world, width, height, amount):
  # Returns the updated world along with a list of rooms
  # A room is just a tuple (x,y) of the center of that room to be used for generating a graph
  attempts = 1000
  rooms = []
  while attempts > 0 and len(rooms) < amount:
    attempts -= 1
    room = try_to_place_room(world, width, height)
    if room != None:
      rooms.append(room)
  return world, rooms
    

def try_to_place_room(world, width, height):
  # Return False, None if the new room overlaps with an existing room
  # Return True, (x,y) if the room can be placed
  sx = random.randint(0 + math.ceil(ROOM_MAX_SIZE / 2), width - 1 - math.ceil(ROOM_MAX_SIZE / 2))
  sy = random.randint(0 + math.ceil(ROOM_MAX_SIZE / 2), height - 1 - math.ceil(ROOM_MAX_SIZE / 2))
  room_width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
  room_height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)

  # Inefficient, fix later
  for x in range(-math.ceil(room_width/2) - 1, math.floor(room_width/2) + 1):
    for y in range(-math.ceil(room_height/2) - 1, math.floor(room_height/2) + 1):
      if world[sx+x][sy+y] == FLOOR:
        return None

  for x in range(-math.ceil(room_width/2), math.floor(room_width/2)):
    for y in range(-math.ceil(room_height/2), math.floor(room_height/2)):
      world[sx+x][sy+y] = FLOOR
  
  return (sx,sy)

class Edge:
  def __init__(self, vertex_a, vertex_b, path, length):
    self.vertex_a = vertex_a
    self.vertex_b = vertex_b
    self.path = path
    self.length = length

  def touches(self, vertex):
    if self.vertex_a == vertex or self.vertex_b == vertex:
      return True
    return False
  
  def get_other_node(self, vertex):
    if self.vertex_a == vertex:
      return self.vertex_b
    if self.vertex_b == vertex:
      return self.vertex_a
    return None

def find_all_hallways(rooms):
  all_edges = []
  rooms2 = rooms.copy()
  for source in rooms:
    rooms2.remove(source)
    for dest in rooms2:
      sx, sy = source
      dx, dy = dest

      path = line.get_line_no_diagonal(sx, sy, dx, dy)
      edge = Edge(source, dest, path, len(path))
      all_edges.append(edge)
  return all_edges

# Using Kruskal's Algorithm
def find_good_hallways(rooms):
  all_edges = find_all_hallways(rooms)
  all_edges.sort(key=lambda x: x.length)

  edges = []
  i = 0
  while len(edges) < len(rooms)-1:
    candidate = all_edges[i]
    if not dfs.contains_cycle(rooms, edges + [candidate]):
      edges.append(candidate)
    i += 1
  return edges

def place_hallways(world, rooms):  
  hallways = find_good_hallways(rooms)
  for edge in hallways:
    for x,y in edge.path:
      world[x][y] = FLOOR
  return world
