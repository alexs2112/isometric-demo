import helpers

# A way to get specific arrays of points for different target types for skills
class Target:
  def __init__(self, range):
    self.range = range

  def get_points(self, sx, sy, dx, dy):
    if abs(sx - dx) > self.range or abs(sy - dy) > self.range:
      return []
    return [(dx,dy)]

class SelfTarget(Target):
  def __init__(self):
    super().__init__(0)

  def get_points(self, sx, sy, dx, dy):
    return [(sx, sy)]

class LineTarget(Target):
  def get_points(self, sx, sy, dx, dy):
    return helpers.get_line(sx, sy, dx, dy)[1:self.range]

class AdjacentTarget(Target):
  def get_points(self, sx, sy, dx, dy):
    out = []
    for x in range(-self.range, self.range+1):
      for y in range(-self.range, self.range+1):
        if x == 0 and y == 0:
          continue
        out.append((sx + x, sy + y))
    return out
