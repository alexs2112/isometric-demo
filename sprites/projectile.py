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

# A bunch of factory functions to cache projectiles in TileSet for weapons and spells that need them
def init_default_arrow():
  full = pygame.image.load("assets/projectiles.png")
  n = full.subsurface((0,0,16,16))
  e = full.subsurface((16,0,16,16))
  s = full.subsurface((32,0,16,16))
  w = full.subsurface((48,0,16,16))
  ne = full.subsurface((0,16,16,16))
  nw = full.subsurface((16,16,16,16))
  se = full.subsurface((32,16,16,16))
  sw = full.subsurface((48,16,16,16))
  return Projectile(n, e, s, w, ne, nw, se, sw)
