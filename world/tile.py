# Keep track of the number of tilesets in floors.png and walls.png
WALL_TILESETS = 5
FLOOR_TILESETS = 3

class Tile:
  def __init__(self, is_floor, tileset):
    # is_floor: a bool if it is a floor or not
    # tileset: an int to determine which tileset this tile uses
    self.floor = is_floor
    self.tileset_id = tileset
  
  def is_floor(self):
    return self.floor
  
  def is_wall(self):
    return not self.floor
