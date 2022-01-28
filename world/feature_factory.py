from sprites.tileset import TileSet
from world.features import *

class FeatureFactory:
  def __init__(self, tileset: TileSet):
    self.tileset = tileset
    # Features can't really have a cache

  def east_door(self):
    closed = self.tileset.get_feature("door_closed_east")
    open = self.tileset.get_feature("door_open_east")
    shadow = self.tileset.get_shadow("door_east")
    return Door(0, closed, open, shadow)

  def west_door(self):
    closed = self.tileset.get_feature("door_closed_west")
    open = self.tileset.get_feature("door_open_west")
    shadow = self.tileset.get_shadow("door_west")
    return Door(1, closed, open, shadow)
