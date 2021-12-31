import pygame

# Keep track of how many are even available in the files
WALL_TILESETS = 6
FLOOR_TILESETS = 5

class TileSet:
  def __init__(self):
    self.corners = []
    self.ne_walls = []
    self.nw_walls = []
    self.floors = []
    self.initialize_floors()
    self.initialize_walls()

    # Creatures and ui elements are stored by a tile id and the subsurface
    self.creatures = {}
    self.initialize_creatures()
    self.ui = {}
    self.initialize_ui()

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

  def get_ui(self, image_id):
    return self.ui[image_id]

  def get_font(self):
    return self.fonts[0] 

  def initialize_walls(self):
    walls_full = pygame.image.load("assets/walls.png")
    image_width = 40
    image_height = 60
    offset_x_ne = 0
    offset_x_nw = image_width
    offset_y = 64
    for i in range(WALL_TILESETS):
      ym = i % 6
      xm = int(i / 6) * 96  # Width of both walls + corner
      ne = walls_full.subsurface((offset_x_ne + xm, offset_y * ym, image_width, image_height))
      nw = walls_full.subsurface((offset_x_nw + xm, offset_y * ym, image_width, image_height))
      self.ne_walls.append(ne)
      self.nw_walls.append(nw)
    
    offset_x = 80
    offset_y = 64
    image_width = 16
    image_height = 48
    for i in range(WALL_TILESETS):
      ym = i % 6
      xm = int(i / 6) * 96
      corner = walls_full.subsurface((offset_x + xm, offset_y * ym, image_width, image_height))
      self.corners.append(corner)


  def initialize_floors(self):
    floors_full = pygame.image.load("assets/floors.png")
    image_width = 64
    image_height = 40

    for i in range(FLOOR_TILESETS):
      floor = floors_full.subsurface((0, image_height * i, image_width, image_height))
      self.floors.append(floor)

  def initialize_creatures(self):
    creatures_full = pygame.image.load("assets/creatures.png")
    image_width = 32
    image_height = 32
    
    # Images are stored in rows of 10, this will hopefully keep it organized
    image_ids = [
      'Edward', 'Goobert', 'Wizard', 'Harold', 'Mushroom', 'Skeleton'
    ]

    for i in range(len(image_ids)):
      x = (i % 10) * image_width
      y = int(i / 10) * image_height
      image = creatures_full.subsurface((x, y, image_width, image_height))
      self.creatures[image_ids[i]] = image
    
  def initialize_ui(self):
    health_bars = pygame.image.load("assets/ui/health_bars.png")
    image_width = 32
    image_height = 6
    health_ids = ["health_full", "health_most", "health_half", "health_quarter"]
    for i in range(4):
      image = health_bars.subsurface((0, i * image_height, image_width, image_height))
      self.ui[health_ids[i]] = image
      