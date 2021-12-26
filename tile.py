import pygame, random
from maze_gen import WALL

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

class TileSet:
  def __init__(self):
    self.walls_full = pygame.image.load("assets/walls.png")
    self.floors_full = pygame.image.load("assets/floors.png")
    self.corners = []
    self.ne_walls = []
    self.nw_walls = []
    self.floors = []
    self.initialize_corners()
    self.initialize_floors()
    self.initialize_walls()

  def initialize_corners(self):
    offset_x = 80
    offset_y = 64
    image_width = 16
    image_height = 48

    for i in range(WALL_TILESETS):
      corner = self.walls_full.subsurface((offset_x, offset_y * i, image_width, image_height))
      self.corners.append(corner)

  def initialize_walls(self):
    image_width = 40
    image_height = 60

    offset_x_ne = 0
    offset_x_nw = image_width
    offset_y = 64

    for i in range(WALL_TILESETS):
      ne = self.walls_full.subsurface((offset_x_ne, offset_y * i, image_width, image_height))
      nw = self.walls_full.subsurface((offset_x_nw, offset_y * i, image_width, image_height))
      self.ne_walls.append(ne)
      self.nw_walls.append(nw)


  def initialize_floors(self):
    image_width = 64
    image_height = 40

    for i in range(FLOOR_TILESETS):
      floor = self.floors_full.subsurface((0, image_height * i, image_width, image_height))
      self.floors.append(floor)

  def get_corner(self, tileset_id):
    return self.corners[tileset_id]

  def get_floor(self, tileset_id):
    return self.floors[tileset_id]

  def get_ne_wall(self, tileset_id):
    return self.ne_walls[tileset_id]

  def get_nw_wall(self, tileset_id):
    return self.nw_walls[tileset_id]
