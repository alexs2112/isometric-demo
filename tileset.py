import pygame

# Keep track of how many are even available in the files
WALL_TILESETS = 6
FLOOR_TILESETS = 5

# Load all relevant images and assets at the start and store them here so that we can quickly access them without
# reloading images all the time
# Using Dungeon Crawl Stone Soup tiles for creatures and items: https://crawl.develz.org/
class TileSet:
  def __init__(self):
    self.corners = []
    self.ne_walls = []
    self.nw_walls = []
    self.floors = []
    self.initialize_floors()
    self.initialize_walls()

    self.corners_small = []
    self.ne_walls_small = []
    self.nw_walls_small = []
    self.floors_small = []
    self.initialize_walls_small()
    self.initialize_floors_small()

    self.creatures = {}
    self.initialize_creatures()
    self.item_icons = {}
    self.initialize_items()
    self.ui = {}
    self.initialize_ui()
    self.misc = {}
    self.initialize_misc()

    # Fonts do not have to be initialized, they are dynamically loaded when needed
    self.fonts = {}

    self.WHITE = (255, 255, 255)
    self.HP_RED = (172, 50, 50)
    self.MANA_BLUE = (99, 155, 255)
    self.PHYSICAL_YELLOW = (251, 242, 54)
    self.MAGICAL_CYAN = (95, 205, 228)
    self.EQUIPPED_GREEN = (106, 190, 48)
    self.DARK_GREY = (34, 32, 52)

  def get_corner(self, tileset_id):
    return self.corners[tileset_id]

  def get_floor(self, tileset_id):
    return self.floors[tileset_id]

  def get_ne_wall(self, tileset_id):
    return self.ne_walls[tileset_id]

  def get_nw_wall(self, tileset_id):
    return self.nw_walls[tileset_id]
  
  def get_corner_small(self, tileset_id):
    return self.corners_small[tileset_id]

  def get_floor_small(self, tileset_id):
    return self.floors_small[tileset_id]

  def get_ne_wall_small(self, tileset_id):
    return self.ne_walls_small[tileset_id]

  def get_nw_wall_small(self, tileset_id):
    return self.nw_walls_small[tileset_id]
  
  def get_creature(self, image_id):
    return self.creatures[image_id] 
  
  def get_item(self, item_name):
    return self.item_icons[item_name]

  def get_misc(self, image_id):
    return self.misc[image_id]

  def get_ui(self, image_id):
    return self.ui[image_id]

  def get_font(self, size=24):
    if size not in self.fonts:
      self.fonts[size] = pygame.font.Font('assets/fonts/DejaVuSans.ttf', size)
    return self.fonts[size]

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

  def initialize_walls_small(self):
    corner_width = 8
    corner_height = 24
    for t in self.corners:
      self.corners_small.append(pygame.transform.scale(t, (corner_width, corner_height)))

    wall_width = 20
    wall_height = 30
    for t in self.ne_walls:
      self.ne_walls_small.append(pygame.transform.scale(t, (wall_width, wall_height)))
    for t in self.nw_walls:
      self.nw_walls_small.append(pygame.transform.scale(t, (wall_width, wall_height)))
    
  def initialize_floors_small(self):
    image_width = 32
    image_height = 20
    for t in self.floors:
      self.floors_small.append(pygame.transform.scale(t, (image_width, image_height)))

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

  def initialize_items(self):
    from items.item_factory import get_item_image_ids
    items_full = pygame.image.load("assets/item_icons.png")
    image_width = 32
    image_height = 32

    image_ids = get_item_image_ids()
    
    y = -image_height # Default to -32 since it will add 32 for the first item
    for type in image_ids:
      x = 0
      for i in range(len(type)):
        x = (i % 10) * image_width
        if (i % 10) == 0:
          y += image_height
        image = items_full.subsurface((x, y, image_width, image_height))
        self.item_icons[type[i]] = image
  
  def initialize_misc(self):
    base = pygame.image.load("assets/misc.png")
    self.misc["satchel"] = base.subsurface((0,0,32,32))
      
  def initialize_ui(self):
    health_bars = pygame.image.load("assets/ui/health_bars.png")
    image_width = 32
    image_height = 6
    health_ids = ["health_full", "health_most", "health_half", "health_quarter"]
    for i in range(4):
      image = health_bars.subsurface((0, i * image_height, image_width, image_height))
      self.ui[health_ids[i]] = image
    self.ui["armor_physical_bar"] = health_bars.subsurface((0, 24, 4, 6))
    self.ui["armor_magical_bar"] = health_bars.subsurface((4, 24, 4, 6))
    
    tile_highlight = pygame.image.load("assets/ui/floor_highlights.png")
    self.ui["floor_highlight_green"] = tile_highlight.subsurface((0,0,64,32))
    self.ui["floor_highlight_red"] = tile_highlight.subsurface((0,32,64,32))

    player_status = pygame.image.load("assets/ui/player_stats_ui.png")
    self.ui["player_name"] = player_status.subsurface((7,0,242,32))
    self.ui["player_health_and_armor"] = player_status.subsurface((0,32,256,97))
    self.ui["player_action_points"] = player_status.subsurface((0,128,256,33))  # There is overlap by 1 px here

    ui_icons = pygame.image.load("assets/ui/base_ui_icons.png")
    image_width = 20
    image_height = 26
    self.ui["armor_physical"] = ui_icons.subsurface((0, 0, image_width, image_height))
    self.ui["armor_magical"] = ui_icons.subsurface((image_width, 0, image_width, image_height))
    self.ui["armor_used"] = ui_icons.subsurface((image_width * 2, 0, image_width, image_height))
    image_width = 24
    image_height = 24
    y = 26
    self.ui["ap_active"] = ui_icons.subsurface((0, y, image_width, image_height))
    self.ui["ap_cost"] = ui_icons.subsurface((image_width, y, image_width, image_height))
    self.ui["ap_inactive"] = ui_icons.subsurface((image_width * 2, y, image_width, image_height))

    map_icons = pygame.image.load("assets/ui/map_icons.png")
    self.ui["map_player_dot"] = map_icons.subsurface((0,0,24,8))
    self.ui["map_enemy_dot"] = map_icons.subsurface((0,8,24,8))
    self.ui["map_items_dot"] = map_icons.subsurface((24,0,24,8))
    self.ui["map_floor_orange"] = map_icons.subsurface((0,16,32,16))
