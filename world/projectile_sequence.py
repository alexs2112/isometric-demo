from helpers import get_projectile_path

class ProjectileSequence:
  def __init__(self):
    self.sequence = []

  def add_projectile_path(self, projectile, path):
    self.sequence.append(get_projectile_path(projectile, path))

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
