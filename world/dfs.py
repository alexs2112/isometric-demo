# Implementation of depth first search for dungeon_gen to use for Kruskal's algorithm
class Node:
  def __init__(self, pos):
    self.pos = pos
    self.neighbors = []
  
def get_node_by_vertex(nodes, vertex):
  for node in nodes:
    if node.pos == vertex:
      return node

def build_graph(vertices, edges):
  nodes = []
  for vertex in vertices:
    nodes.append(Node(vertex))

  for edge in edges:
    for node in nodes:
      if edge.touches(node.pos):
        other_vertex = edge.get_other_node(node.pos)
        node.neighbors.append(get_node_by_vertex(nodes, other_vertex))
  return nodes

# Returns True if there is a cycle, returns the list of visited nodes if there are not so we can see if
# we have checked every node or not
def dfs(current, visited, parent):
  visited.append(current)
  for node in current.neighbors:
    if node == parent:
      continue
    if node in visited:
      return True
    if dfs(node, visited, current) == True:
      return True
  return visited

def contains_cycle(vertices, edges):
  graph = build_graph(vertices, edges)

  visited = []
  for vertex in graph:
    if vertex in visited:
      continue
    output = dfs(vertex, visited, None)
    if output == True:
      return True
    visited = output
  return False
