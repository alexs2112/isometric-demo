class MovementQueue:
  def __init__(self):
    # A list of lists, each creature that moves at the same time adds their list to the queue and we pop the first element of
    # each list
    self.queue = []

  def add_movement(self, list_of_moves):
    self.queue.append(list_of_moves)

  def get_first_moves(self):
    out = []
    for i in range(len(self.queue)):
      out.append(self.queue[i].pop(0))
      if self.queue[i] == []:
        self.queue.pop(i)
        i -= 1
    return out
  
  def is_complete(self):
    return self.queue == []

class Move:
  def __init__(self, creature, point):
    self.creature = creature
    self.point = point
