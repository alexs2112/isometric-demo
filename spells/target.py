import helpers

# A way to get specific arrays of points for different target types for spells and abilities
class Target:
  def __init__(self, range):
    self.range = range

  def get_points(self, sx, sy, dx, dy):
    return [(dx,dy)]

class LineTarget(Target):
  def get_points(self, sx, sy, dx, dy):
    return helpers.get_line(sx, sy, dx, dy)[1:self.range]
