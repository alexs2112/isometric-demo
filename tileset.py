import pygame

# Keep track of how many are even available in the files
WALL_TILESETS = 5
FLOOR_TILESETS = 3

class TileSet:
  def __init__(self):
    self.walls_full = pygame.image.load("assets/walls.png")
    self.floors_full = pygame.image.load("assets/floors.png")
    self.corners = []
    self.ne_walls = []
    self.nw_walls = []
    self.floors = []
    self.initialize_corners()   # Put corners and walls in one to load images in the methods instead of init
    self.initialize_floors()
    self.initialize_walls()

    # Creatures are stored by a tile id and the subsurface
    self.creatures = {}
    self.initialize_creatures()

    self.fonts = [pygame.font.SysFont('Comic Sans MS', 30)]

  def get_corner(self, tileset_id):
    return self.corners[tileset_id]

  def get_floor(self, tileset_id):
    return self.floors[tileset_id]

  def get_ne_wall(self, tileset_id):
    return self.ne_walls[tileset_id]

  def get_nw_wall(self, tileset_id):
    return self.nw_walls[tileset_id]
  
  def get_creature(self, image_id):
    return self.creatures[image_id] 

  def get_font(self):
    return self.fonts[0] 

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

  def initialize_creatures(self):
    creatures_full = pygame.image.load("assets/creatures.png")
    image_width = 32
    image_height = 32
    
    # Images are stored in rows of 10, this will hopefully keep it organized
    image_ids = [
      'Edward', 'Goobert', 'Wizard', 'Harold'
    ]

    for i in range(len(image_ids)):
      x = (i % 10) * image_width
      y = int(i / 10) * image_height
      image = creatures_full.subsurface((x, y, image_width, image_height))
      self.creatures[image_ids[i]] = image
      