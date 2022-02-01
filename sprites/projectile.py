import pygame

# A way to hold a collection of 8 images that make up a projectile
class Projectile:
  # Letters indicate cardinal cartesian directions the image points towards
  def __init__(self, n=None, e=None, s=None, w=None, ne=None, nw=None, se=None, sw=None, target=None, all=None):
    self.all = all
    self.target = target
    self.n = n
    self.e = e
    self.s = s
    self.w = w
    self.ne = ne
    self.nw = nw
    self.se = se
    self.sw = sw

# A bunch of factory functions to cache projectiles in TileSet for weapons and skills that need them
def init_default_arrow(full):
  n = full.subsurface((0,0,16,16))
  e = full.subsurface((16,0,16,16))
  s = full.subsurface((32,0,16,16))
  w = full.subsurface((48,0,16,16))
  ne = full.subsurface((0,16,16,16))
  nw = full.subsurface((16,16,16,16))
  se = full.subsurface((32,16,16,16))
  sw = full.subsurface((48,16,16,16))
  return Projectile(n, e, s, w, ne, nw, se, sw)

def init_poison_cloud(full):
  target = [
    full.subsurface((0,32,32,32)),
    full.subsurface((32,32,32,32))
  ]
  return Projectile(target=target)

def init_fire_cloud(full):
  target = [
    full.subsurface((0,64,32,32)),
    full.subsurface((32,64,32,32))
  ]
  return Projectile(target=target)
