# Implementation of the A* algorithm: http://trystans.blogspot.com/2011/09/roguelike-tutorial-13-aggressive.html
class Pathfinder:
  def __init__(self):
    self.open = []
    self.closed = []
    self.parents = {}
    self.costs = {}
  
  def heuristic_cost(self, source, dest):
    return max(abs(source[0] - dest[0]), abs(source[1] - dest[1]))
  
  def cost_to_get_to(self, point):
    if point in self.parents:
      parent = self.parents[point]
      return 1 + self.cost_to_get_to(parent)
    else:
      return 0

  def total_cost(self, source, dest):
    if source in self.costs:
      return self.costs[source]

    cost = self.cost_to_get_to(source) + self.heuristic_cost(source, dest)
    self.costs[source] = cost
    return cost
  
  def reparent(self, child, parent):
    self.parents[child] = parent
    if child in self.costs:
      self.costs.pop(child)
  
  def find_path(self, creature, end, max_tries):
    # Might need to clear the class variables here
    start = (creature.x, creature.y)
    self.open.append(start)

    for _ in range(max_tries):
      if len(self.open) == 0:
        break
      closest = self.get_closest_point(end)
      self.open.remove(closest)
      self.closed.append(closest)

      if closest == end:
        return self.create_path(start, closest)
      else:
        self.check_neighbours(creature, end, closest)
    return []
  
  def get_closest_point(self, end):
    closest = self.open[0]
    for other in self.open:
      if self.total_cost(other, end) < self.total_cost(closest, end):
        closest = other
    return closest
  
  def check_neighbours(self, creature, end, closest):
    for neighbour in self.get_neighbours(closest):
      if neighbour in self.closed \
        or not creature.has_seen(neighbour[0], neighbour[1]) \
        or not creature.can_enter(neighbour[0], neighbour[1]) and neighbour != end:
        continue
      
      if neighbour in self.open:
        self.reparent_neighbour_if_necessary(closest, neighbour)
      else:
        self.reparent_neighbour(closest, neighbour)

  def get_neighbours(self, point):
    # First add the cardinal directions, and then the diagonals to bias towards straight lines
    x,y = point
    neighbours = [
      (x+1, y),
      (x-1, y),
      (x, y+1),
      (x, y-1),
      (x+1, y+1),
      (x-1, y+1),
      (x+1, y-1),
      (x-1, y-1)
    ]

    return neighbours
  
  def reparent_neighbour(self, closest, neighbour):
    self.reparent(neighbour, closest)
    self.open.append(neighbour)
  
  def reparent_neighbour_if_necessary(self, closest, neighbour):
    original_parent = self.parents[neighbour]
    current_cost = self.cost_to_get_to(neighbour)
    self.reparent(neighbour, closest)

    reparent_cost = self.cost_to_get_to(neighbour)
    if reparent_cost < current_cost:
      self.open.remove(neighbour)
    else:
      self.reparent(neighbour, original_parent)

  def create_path(self, start, end):
    path = []
    while end != start:
      path.append(end)
      end = self.parents[end]
    path.reverse()
    return path

class Path:
  def __init__(self, creature, dx, dy):
    pathfinder = Pathfinder()
    self.points = pathfinder.find_path(creature, (dx,dy), 300)
