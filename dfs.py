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
  
  output = []
  for node in nodes:
    if len(node.neighbors) > 0:
      output.append(node)
  return output

# Currently a little broken, can have unconnected parts
def dfs(current, visited, parent):
  visited.append(current)
  for node in current.neighbors:
    if node == parent:
      continue
    if node in visited:
      return True
    if dfs(node, visited, current):
      return True
  return False

def contains_cycle(vertices, edges):
  graph = build_graph(vertices, edges)
  if dfs(graph[0], [], None):
    return True
  return False