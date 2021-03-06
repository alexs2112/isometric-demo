import pygame
import sprites.projectile as projectile

# Keep track of how many are even available in the files
WALL_TILESETS = 8
FLOOR_TILESETS = 5

# Load all relevant images and assets at the start and store them here so that we can quickly access them without
# reloading images all the time
class TileSet:
  WHITE = (255, 255, 255)
  HP_RED = (172, 50, 50)
  MANA_BLUE = (99, 155, 255)
  PHYSICAL_YELLOW = (251, 242, 54)
  MAGICAL_CYAN = (95, 205, 228)
  EQUIPPED_GREEN = (106, 190, 48)
  ORANGE = (223, 113, 38)
  DARK_GREY = (34, 32, 52)
  LIGHT_GREY = (139, 147, 175)

  def __init__(self):
    self.corners = []
    self.ne_walls = []
    self.nw_walls = []
    self.floors = []
    self.corners_small = []
    self.ne_walls_small = []
    self.nw_walls_small = []
    self.floors_small = []
    self.initialize_floors()
    self.initialize_walls()

    self.shadows = {} # Not initialized, just appended to by a bunch of functions

    self.creatures = {}
    self.initialize_creatures()
    self.item_icons = {}
    self.item_sprites = {}
    self.initialize_items()
    self.ui = {}
    self.initialize_ui()
    self.misc = {}
    self.initialize_misc()
    self.features = {}
    self.initialize_features()
    self.projectiles = {}
    self.initialize_projectiles()
    self.skill_icons = {}
    self.initialize_skill_icons()
    self.effect_icons = {}
    self.effect_sprites = {}
    self.initialize_effect()

    # Some subscreen related inits that don't have specific image hashes
    self.initialize_character_screen()
    self.initialize_skill_screen()
    self.initialize_pickup_screen()
    self.initialize_staircase_screen()

    # Fonts do not have to be initialized, they are dynamically loaded when needed
    self.fonts = {}

  def get_corner(self, tileset_id, small=False):
    if small: return self.corners_small[tileset_id]
    return self.corners[tileset_id]

  def get_floor(self, tileset_id, small=False):
    if small: return self.floors_small[tileset_id]
    return self.floors[tileset_id]

  def get_ne_wall(self, tileset_id, small=False):
    if small: return self.ne_walls_small[tileset_id]
    return self.ne_walls[tileset_id]

  def get_nw_wall(self, tileset_id, small=False):
    if small: return self.nw_walls_small[tileset_id]
    return self.nw_walls[tileset_id]
  
  def get_creature(self, image_id):
    return self.creatures[image_id] 
  
  def get_item(self, item_name):
    return self.item_icons[item_name]

  def get_item_sprite(self, item_name):
    return self.item_sprites[item_name]
  
  def get_skill_icons(self, skill_name):
    return self.skill_icons[skill_name]

  def get_effect_icons(self, effect_name):
    return self.effect_icons[effect_name]
  
  def get_effect_sprites(self, effect_name):
    return self.effect_sprites[effect_name]
  
  def get_projectile(self, projectile_name):
    # Returns a projectile.Projectile object instead of just an image
    return self.projectiles[projectile_name]

  def get_misc(self, image_id):
    return self.misc[image_id]

  def get_ui(self, image_id):
    return self.ui[image_id]

  def get_feature(self, image_id):
    return self.features[image_id]

  def get_shadow(self, image_id):
    return self.shadows[image_id] 

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
    small_width = 20
    small_height = 30
    for i in range(WALL_TILESETS):
      ym = i % 6
      xm = int(i / 6) * 96  # Width of both walls + corner
      ne = walls_full.subsurface((offset_x_ne + xm, offset_y * ym, image_width, image_height))
      nw = walls_full.subsurface((offset_x_nw + xm, offset_y * ym, image_width, image_height))
      self.ne_walls.append(ne)
      self.nw_walls.append(nw)
      self.ne_walls_small.append(pygame.transform.scale(ne, (small_width, small_height)))
      self.nw_walls_small.append(pygame.transform.scale(nw, (small_width, small_height)))
    
    offset_x = 80
    offset_y = 64
    image_width = 16
    image_height = 48
    small_width = 8
    small_width = 24
    for i in range(WALL_TILESETS):
      ym = i % 6
      xm = int(i / 6) * 96
      corner = walls_full.subsurface((offset_x + xm, offset_y * ym, image_width, image_height))
      self.corners.append(corner)

  def initialize_floors(self):
    floors_full = pygame.image.load("assets/floors.png")
    image_width = 64
    image_height = 40
    small_width = 32
    small_height = 20

    for i in range(FLOOR_TILESETS):
      floor = floors_full.subsurface((0, image_height * i, image_width, image_height))
      self.floors.append(floor)
      self.floors_small.append(pygame.transform.scale(floor, (small_width, small_height)))

  def initialize_creatures(self):
    creatures_full = pygame.image.load("assets/creatures.png")
    image_width = 32
    image_height = 32
    
    # Images are stored in rows of 10, this will hopefully keep it organized
    image_ids = [
      'Rat', 'Mushroom', 'Skeleton', 'Ghoul'
    ]

    for i in range(len(image_ids)):
      x = (i % 10) * image_width
      y = int(i / 10) * image_height
      image = creatures_full.subsurface((x, y, image_width, image_height))
      self.creatures[image_ids[i]] = image

    players_full = pygame.image.load("assets/bodies.png")
    player_ids = [
      'Edward', 'Goobert', 'Wizard', 'Harold'
    ]
    for i in range(len(player_ids)):
      x = (i % 10) * image_width
      y = int(i / 10) * image_height
      image = players_full.subsurface((x, y, image_width, image_height))
      self.creatures[player_ids[i]] = image


  def initialize_items(self):
    from items.item_factory import get_item_image_ids
    items_full = pygame.image.load("assets/item_icons.png")
    sprites_full = pygame.image.load("assets/item_sprites.png")
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
        self.item_icons[type[i]] = pygame.transform.scale(image, (48,48))

    y = 0
    # Chest
    y = self.item_sprites_helper(image_ids, sprites_full, 32, 32, 0, y)

    # Head
    y = self.item_sprites_helper(image_ids, sprites_full, 32, 16, 1, y)

    # Feet
    y = self.item_sprites_helper(image_ids, sprites_full, 32, 16, 2, y)

    # Hands
    y = self.item_sprites_helper(image_ids, sprites_full, 32, 16, 3, y)

    # Cloak
    y = self.item_sprites_helper(image_ids, sprites_full, 32, 32, 4, y)

    # Weapons
    y = self.item_sprites_helper(image_ids, sprites_full, 16, 32, 5, y)

  def item_sprites_helper(self, image_ids, sprites_full, image_width, image_height, item_type_index, y):
    for i in range(len(image_ids[item_type_index])):
      x = (i % 10) * image_width
      if i > 0 and (i % 10) == 0:
        y += image_height
      sprite = sprites_full.subsurface((x, y, image_width, image_height))
      self.item_sprites[image_ids[item_type_index][i]] = sprite
    return y + image_height

  def initialize_skill_icons(self):
    from skills.skill_factory import ALL_SKILLS
    full = pygame.image.load("assets/skill_icons.png")
    width, height = 48, 48
    skills = ALL_SKILLS
    for i in range(len(skills)):
      x = (i % 10) * width
      y = (i // 10) * height
      self.skill_icons[skills[i]] = full.subsurface((x, y, width, height))
  
  def initialize_effect(self):
    effect_names = [
      "Stunned",
      "Rapid Slashes",
      "Fire Vulnerability",
      "Regenerating",
      "Burning",
      "Poisoned",
      "Spores"
    ]

    icons = pygame.image.load("assets/effect_icons.png")
    w_i, h_i = 48, 48
    sprites = pygame.image.load("assets/effect_sprites.png")
    w_s, h_s = 16, 16
    for i in range(len(effect_names)):
      x = (i % 10) * w_i
      y = (i // 10) * h_i
      self.effect_icons[effect_names[i]] = icons.subsurface((x, y, w_i, h_i))
      x = i * w_s
      y = 0
      self.effect_sprites[effect_names[i]] = sprites.subsurface((x,y,w_s,h_s))
  
  def initialize_misc(self):
    base = pygame.image.load("assets/misc.png")
    self.misc["satchel"] = base.subsurface((0,0,32,32))

    win_con = base.subsurface((32,0,32,32))
    self.item_icons["Stone of Power"] = pygame.transform.scale(win_con, (48,48))

    self.misc["unknown_creature_sprite"] = base.subsurface((64,0,64,64))
      
  def initialize_ui(self):
    main_icons = pygame.image.load("assets/ui/main_icons.png")
    image_width = 32
    image_height = 6
    health_ids = ["health_full", "health_most", "health_half", "health_quarter"]
    for i in range(4):
      image = main_icons.subsurface((0, i * image_height, image_width, image_height))
      self.ui[health_ids[i]] = image
    self.ui["armor_physical_bar"] = main_icons.subsurface((0, 24, 4, 6))
    self.ui["armor_magical_bar"] = main_icons.subsurface((4, 24, 4, 6))
    self.ui["inactive_icon"] = main_icons.subsurface((8, 24, 8, 8))
    
    tile_highlight = pygame.image.load("assets/ui/tile_highlights.png")
    self.ui["floor_highlight_green"] = tile_highlight.subsurface((0,0,64,32))
    self.ui["floor_highlight_red"] = tile_highlight.subsurface((0,32,64,32))
    self.ui["floor_highlight_yellow"] = tile_highlight.subsurface((0,64,64,32))
    self.ui["floor_highlight_blue"] = tile_highlight.subsurface((0,96,64,32))
    self.ui["floor_highlight_purple"] = tile_highlight.subsurface((64,96,64,32))
    self.shadows["floor"] = tile_highlight.subsurface((64,0,64,32))
    self.shadows["wall"] = tile_highlight.subsurface((64,32,64,48))

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
    image_width = 72
    image_height = 72
    y = 50
    self.ui["queue_box_player"] = ui_icons.subsurface((0,y,image_width,image_height))
    self.ui["queue_box_enemy"] = ui_icons.subsurface((image_width,y,image_width,image_height))
    self.ui["queue_box_active"] = ui_icons.subsurface((image_width * 2,y,image_width,image_height))

    map_icons = pygame.image.load("assets/ui/map_icons.png")
    self.ui["map_player_dot"] = map_icons.subsurface((0,0,24,8))
    self.ui["map_enemy_dot"] = map_icons.subsurface((0,8,24,8))
    self.ui["map_items_dot"] = map_icons.subsurface((24,0,24,8))
    self.ui["map_floor_orange"] = map_icons.subsurface((0,16,32,16))

    buttons = pygame.image.load("assets/ui/main_buttons.png")
    self.ui["end_turn_highlight"] = buttons.subsurface((160,272,160,64))

  def initialize_character_screen(self):
    full = pygame.image.load("assets/screens/character_screen_icons.png")
    self.ui["char_screen_inv_name"] = full.subsurface((0,0,416,36))
    self.ui["char_screen_inv_name_highlighted"] = full.subsurface((0,36,416,36))
    self.ui["item_icon_box"] = full.subsurface((0,72,52,52))
    self.ui["item_icon_box_green"] = full.subsurface((52,72,52,52))
    self.ui["item_icon_box_yellow"] = full.subsurface((104,72,52,52))
    self.ui["stats_health_icon"] = full.subsurface((160,80,32,32))
    self.ui["stats_mana_icon"] = full.subsurface((192,80,32,32))
    self.ui["stats_question_icon"] = full.subsurface((224,80,32,32))
    self.ui["stats_title_box"] = full.subsurface((0,124,420,36))
    self.ui["stats_icon_half_box"] = full.subsurface((0,160,210,36))
    self.ui["stats_icon_third_box"] = full.subsurface((210,160,140,36))
    self.ui["stats_divider"] = full.subsurface((0,196,420,12))
    self.ui["stats_weapon_box"] = full.subsurface((0,208,420,52))
    self.ui["stats_icon_third_box_large"] = full.subsurface((0,260,140,52))
    self.ui["brawn_icon"] = full.subsurface((140,260,48,48))
    self.ui["agility_icon"] = full.subsurface((188,260,48,48))
    self.ui["will_icon"] = full.subsurface((236,260,48,48))
    self.ui["unarmed_icon"] = full.subsurface((284,260,48,48))
    self.ui["stats_stat_box"] = full.subsurface((0,312,420,36))
    self.ui["stats_tooltip_line_header"] = full.subsurface((0,348,220,22))
    self.ui["stats_tooltip_line"] = full.subsurface((0,350,220,20))
    self.ui["stats_tooltip_line_bottom"] = full.subsurface((0,350,220,22))

  def initialize_skill_screen(self):
    full = pygame.image.load("assets/screens/skills_screen.png")
    self.ui["skill_box_grey"] = full.subsurface((0,0,56,56))
    self.ui["skill_box_blue"] = full.subsurface((56,0,56,56))
    self.ui["skill_box_red"] = full.subsurface((112,0,56,56))
    self.ui["skill_box_yellow"] = full.subsurface((168,0,56,56))
    self.ui["skill_box_orange"] = full.subsurface((224,0,56,56))
    self.ui["skill_box_purple"] = full.subsurface((280,0,56,56))


  def initialize_pickup_screen(self):
    full = pygame.image.load("assets/screens/pickup_screen.png")
    self.ui["pickup_screen_background"] = full.subsurface((0,0,320,416))
    self.ui["item_box"] = full.subsurface((0,416,52,52))
    self.ui["item_box_highlight"] = full.subsurface((52,416,52,52))
    self.ui["pick_up_all"] = full.subsurface((104,416,120,40))
    self.ui["pick_up_all_highlight"] = full.subsurface((224,416,120,40))
    self.ui["option_button"] = full.subsurface((0,468,128,18))
    self.ui["option_button_highlight"] = full.subsurface((128,468,128,18))
    self.ui["exit_button"] = full.subsurface((256,456,40,35))
    self.ui["exit_button_highlight"] = full.subsurface((296,456,40,35))
  
  def initialize_staircase_screen(self):
    full = pygame.image.load("assets/screens/staircase_screen.png")
    self.ui["confirmation_box"] = full.subsurface((0,0,360,128))
    self.ui["confirm_button_highlight"] = full.subsurface((0,128,180,52))
    self.ui["confirm_button_default"] = full.subsurface((180,128,180,52))
    self.ui["stats_bar_default"] = full.subsurface((0,180,288,36))
    self.ui["stats_bar_default_highlight"] = full.subsurface((0,216,288,36))
    self.ui["stats_bar_toggle"] = full.subsurface((0,252,288,36))
    self.ui["stats_bar_toggle_highlight"] = full.subsurface((0,288,288,36))
    self.ui["character_sprite_box"] = full.subsurface((288,180,92,92))

  def initialize_features(self):
    full = pygame.image.load("assets/features.png")
    self.features["door_closed_east"] = full.subsurface((0,0,40,52))
    self.features["door_closed_west"] = full.subsurface((40,0,40,52))
    self.features["door_open_east"] = full.subsurface((0,52,40,52))
    self.features["door_open_west"] = full.subsurface((40,52,40,52))
    self.shadows["door_east"] = full.subsurface((0,104,40,35))
    self.shadows["door_west"] = full.subsurface((40,104,40,35))
    self.features["staircase"] = full.subsurface((80,0,64,40))

  def initialize_projectiles(self):
    full = pygame.image.load("assets/projectiles.png")
    self.projectiles["default_arrow"] = projectile.init_default_arrow(full)
    self.projectiles["poison_cloud"] = projectile.init_poison_cloud(full)
    self.projectiles["fire_cloud"] = projectile.init_fire_cloud(full)
