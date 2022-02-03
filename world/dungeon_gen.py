import random, math, misc.helpers as helpers
import world.dfs as dfs

FLOOR = 0
WALL = 1
ROOM_MIN_SIZE = 3
ROOM_MAX_SIZE = 7

def generate_dungeon(world, width, height, room_count):
  world, rooms = create_rooms(world, width, height, room_count)
  world, doors = place_hallways(world, rooms)
  start_room, end_room = get_start_and_end_rooms(rooms)
  return world, rooms, start_room, end_room, doors

def create_rooms(world, width, height, amount):
  # Returns the updated world along with a list of rooms
  # A room is just a tuple (x,y) of the center of that room to be used for generating a graph
  attempts = 1000
  rooms = []
  room_id = 0
  while attempts > 0 and len(rooms) < amount:
    attempts -= 1
    room = try_to_place_room(world, width, height, room_id)
    if room != None:
      rooms.append(room)
      room_id += 1
  return world, rooms
    
# Return False, None if the new room overlaps with an existing room
# Return True, (x,y) if the room can be placed
def try_to_place_room(world, width, height, room_id):
  from world.world_builder import Room    
  # This is really awkward import to have here, otherwise we need to have Room in dungeon_gen.py which doesnt
  # make a ton of sense, or we have a circular import and everything breaks
  # Fix this when we come up with a better solution

  sx = random.randint(0 + math.ceil(ROOM_MAX_SIZE / 2), width - 1 - math.ceil(ROOM_MAX_SIZE / 2))
  sy = random.randint(0 + math.ceil(ROOM_MAX_SIZE / 2), height - 1 - math.ceil(ROOM_MAX_SIZE / 2))
  room_width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
  room_height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)

  short_width = math.floor(room_width/2)
  short_height = math.floor(room_height/2)
  long_width = math.ceil(room_width/2)
  long_height = math.ceil(room_height/2)

  # Inefficient to iterate over each potential room twice, fix later if we can think of a fix
  for x in range(-long_width - 1, short_width + 1):
    for y in range(-long_height - 1, short_height + 1):
      if world[sx+x][sy+y] == FLOOR:
        return None

  for x in range(-long_width, short_width):
    for y in range(-long_height, short_height):
      world[sx+x][sy+y] = FLOOR
  
  return Room(room_id, (sx,sy), (sx - long_width, sy - long_height), (sx + short_width, sy + short_height))

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

      path = helpers.get_line_no_diagonal(sx, sy, dx, dy)
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
  origins = list(map(lambda room: room.origin, rooms))
  doors = []
  hallways = find_good_hallways(origins)
  for edge in hallways:
    room1 = None
    room2 = None
    for room in rooms:
      if edge.vertex_a == room.origin:
        room1 = room
      elif edge.vertex_b == room.origin:
        room2 = room
    room1.add_neighbor(room2)
    room2.add_neighbor(room1)

# Hallway optimization and door finding algorithm
# Get a list of tiles cardinally adjacent to the start room and the end room. Then for each tile in the path:
# - If the tile is already a floor, continue
# - If the tile is in the end room list, turn into floor, mark as door, and break
# - If the tile is in the start room list AND the next tile is NOT in the start room list, turn into floor and mark as door
# - If the tile is in the start room list AND the next tile is ALSO in the start room list, continue
    tiles1 = room1.get_adjacent_tiles()
    tiles2 = room2.get_adjacent_tiles()
    for i in range(edge.length):
      x,y = edge.path[i]

      if world[x][y] == FLOOR:
        continue

      if (x,y) in tiles2:
        world[x][y] = FLOOR

        if not_adjacent_to_door(doors, x, y):
          doors.append((x,y))
        break

      if i < edge.length - 1:
        x2,y2 = edge.path[i+1]
        if (x,y) in tiles1:
          if (x2,y2) in tiles1:
            continue
          else:
            world[x][y] = FLOOR
            if not_adjacent_to_door(doors, x, y):
              doors.append((x,y))
        else:
          world[x][y] = FLOOR

  # Temporary, clean up invalid doors aftwards (doors in corners and stuff)
  for (x,y) in doors:
    if not valid_door(world,x,y):
      doors.remove((x,y))
  return world, doors

def valid_door(world, sx, sy):
  valid = world[sx-1][sy] == FLOOR and world[sx+1][sy] == FLOOR and world[sx][sy-1] == WALL and world[sx][sy+1] == WALL
  if not valid:
    valid = world[sx-1][sy] == WALL and world[sx+1][sy] == WALL and world[sx][sy-1] == FLOOR and world[sx][sy+1] == FLOOR
  if not valid:
    return False
  return True

def not_adjacent_to_door(doors, sx, sy):
  n = []
  for x in range(sx-1, sx+2):
    for y in range(sy-1, sy+2):
      n.append((x,y))
  
  for t in n:
    if t in doors:
      return False
  return True

# The start and end rooms should be the rooms with the largest number of intervening rooms
def get_start_and_end_rooms(rooms):
  for room in rooms:
    room.relative_costs = [-1] * len(rooms)
    room.relative_costs[room.id] = 0
    for n in room.neighbors:
      room.relative_costs[n.id] = 1
  
  # For each iteration, pass over each rooms neighbours and pass relative costs between them
  total_ids = len(rooms)
  iterations = int(total_ids / 2)
  longest_length = -1
  start, end = -1, -1
  for _ in range(iterations):
    for room in rooms:
      for n in room.neighbors:
        for i in range(total_ids):
          room_cost = room.relative_costs[i]
          n_cost = n.relative_costs[i]
          if room_cost == -1 and n_cost > -1:
            room.relative_costs[i] = n_cost + 1
            if n_cost + 1 > longest_length:
              longest_length = n_cost + 1
              start, end = room.id, i
          elif room_cost > -1 and n_cost == -1:
            n.relative_costs[i] = room_cost + 1
            if room_cost + 1 > longest_length:
              longest_length = room_cost + 1
              start, end = n.id, i
  return rooms[start], rooms[end]
