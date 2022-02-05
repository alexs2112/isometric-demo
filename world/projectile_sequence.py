from misc.helpers import get_projectile_path

class ProjectileSequence:
  def __init__(self):
    self.sequence = []

  def add_projectile_path(self, projectile, path):
    res = get_projectile_path(projectile, path)
    if res:
      self.sequence.append(res)

  def get_iteration(self):
    out = []
    for s in self.sequence:
      if s:
        out.append(s.pop(0))
    return out
  
  def is_complete(self):
    for s in self.sequence:
      if s:
        return False
    return True
