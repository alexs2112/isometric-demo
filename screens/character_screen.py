import pygame
from screens.screen import Screen, Button, write, write_centered, split_text_to_list
from sprites.tileset import TileSet
from screens.subscreen import Subscreen
from creatures.creature import Creature
from creatures.stats_helper import ATTRIBUTE_LIST, STAT_LIST
from pygame.locals import (
  MOUSEBUTTONDOWN,
  KEYDOWN,
  K_ESCAPE,
  K_d
)

EQUIPMENT_START_X = 420
INVENTORIES_START_X = 864
EQUIPMENT_ORDER = [
  "Head",
  "Chest",
  "Cloak",
  "Hands",
  "Feet",
  "Ring",
  "Main"
]
class CharacterScreen(Subscreen):
  def __init__(self, tileset: TileSet, creature: Creature, party):
    self.creature = creature
    self.party = party
    self.tileset = tileset

    # Don't cache these rather large images in tileset
    self.stats_cache_surface = None
    self.equipment_block = pygame.image.load("assets/screens/player_equipment_block.png")
    self.update_player_stats(tileset)

    self.clicked_item = None
    self.clicked_player = None

    self.mouse_item = None
    self.mouse_player = None

    self.player_buttons = []
    self.set_player_buttons(tileset)

  def set_player_buttons(self, tileset: TileSet):
    self.player_buttons.clear()
    base_x = INVENTORIES_START_X
    base_y = 0
    button_width = 416
    button_height = 36

    button_default = tileset.get_ui("char_screen_inv_name")
    button_mouse = tileset.get_ui("char_screen_inv_name_highlighted")

    rect = (base_x, base_y, button_width, button_height)
    self.player_buttons.append(Button(rect, button_default, button_mouse, func=self.get_button_function(self.creature, tileset)))
    base_y += self.get_player_height(self.creature)

    for c in self.party:
      if c == self.creature:
        continue
      rect = (base_x, base_y, button_width, button_height)
      self.player_buttons.append(Button(rect, button_default, button_mouse, func=self.get_button_function(c, tileset)))
      base_y += self.get_player_height(c)

  def get_button_function(self, creature, tileset):
    def func():
      if self.creature == creature:
        return
      self.creature = creature
      self.update_player_stats(tileset)
      self.set_player_buttons(tileset)
    return func
  
  def draw(self, screen: Screen):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    self.update_mouse(mouse_x, mouse_y)

    screen.blit(self.stats_cache_surface, (0,0))
    for button in self.player_buttons:
      screen.blit(button.get_image(mouse_x, mouse_y), (button.x, button.y))
    self.draw_player_equipment(screen)
    self.draw_inventories(screen)
    self.write_item_description(screen)

  def update_player_stats(self, tileset: TileSet):
    # Left: All stats, attributes, and statss. Increase them on level up here
    self.stats_cache_surface = pygame.Surface((420, 800))
    y = 0
    self.stats_cache_surface.blit(tileset.get_ui("stats_icon_half_box"), (0,y))
    self.stats_cache_surface.blit(tileset.get_ui("stats_health_icon"), (2,y+2))
    write_centered(self.stats_cache_surface, "HP: " + str(self.creature.hp) + "/" + str(self.creature.get_max_hp()),
          (122, y + 6), tileset.get_font(22))
    self.stats_cache_surface.blit(tileset.get_ui("stats_icon_half_box"), (210,y))
    self.stats_cache_surface.blit(tileset.get_ui("stats_mana_icon"), (212,y+2))
    write_centered(self.stats_cache_surface, "MP: " + str(self.creature.mana) + "/" + str(self.creature.get_max_mana()),
          (332, y + 6), tileset.get_font(22))
    
    y += 36
    self.stats_cache_surface.blit(tileset.get_ui("stats_icon_half_box"), (0,y))
    self.stats_cache_surface.blit(tileset.get_ui("armor_physical"), (8, y + 5))
    write_centered(self.stats_cache_surface, "PA: " + str(self.creature.p_armor) + "/" + str(self.creature.get_p_armor_cap()),
          (122, y + 6), tileset.get_font(22))
    x = 210
    self.stats_cache_surface.blit(tileset.get_ui("stats_icon_half_box"), (x,y))
    self.stats_cache_surface.blit(tileset.get_ui("armor_magical"), (x + 8, y + 5))
    write_centered(self.stats_cache_surface, "MA: " + str(self.creature.m_armor) + "/" + str(self.creature.get_m_armor_cap()),
          (x + 122, y + 6), tileset.get_font(22))
    
    y += 36
    self.stats_cache_surface.blit(tileset.get_ui("stats_icon_third_box"), (0,y))
    self.stats_cache_surface.blit(tileset.get_ui("ap_active"), (6, y + 6))
    write_centered(self.stats_cache_surface, "AP: " + str(self.creature.ap) + "/" + str(self.creature.max_ap),
          (88, y + 6), tileset.get_font(22))
    x = 140
    self.stats_cache_surface.blit(tileset.get_ui("stats_icon_third_box"), (x,y))
    self.stats_cache_surface.blit(tileset.get_ui("stats_question_icon"), (x+2, y+2))
    write_centered(self.stats_cache_surface, "SPD: " + str(self.creature.get_speed()),
          (x+88, y + 6), tileset.get_font(22))
    x = 280
    self.stats_cache_surface.blit(tileset.get_ui("stats_icon_third_box"), (x,y))
    self.stats_cache_surface.blit(tileset.get_ui("stats_question_icon"), (x+2, y+2))
    write_centered(self.stats_cache_surface, "INIT: " + str(self.creature.get_initiative()),
          (x+88, y + 6), tileset.get_font(22))
    
    y += 36
    x = 0
    self.stats_cache_surface.blit(tileset.get_ui("stats_divider"), (x,y))

    y += 12
    self.stats_cache_surface.blit(tileset.get_ui("stats_weapon_box"), (x,y))
    w = self.creature.equipment.slot("Main")
    if w:
      self.stats_cache_surface.blit(w.icon, (x+2,y+2))
    else:
      self.stats_cache_surface.blit(tileset.get_ui("unarmed_icon"), (x+2,y+2))
    write(self.stats_cache_surface, "Damage: " + str(self.creature.get_attack_min()) + "-" + str(self.creature.get_attack_max()) + " " + self.creature.get_damage_type().capitalize(),
          (x + 60, y + 2), tileset.get_font(20))
    write(self.stats_cache_surface, "Cost: " + str(self.creature.get_attack_cost()) + " AP" + ", Range: " + str(self.creature.get_attack_range()),
          (x + 60, y + 24), tileset.get_font(20))

    y += 52
    self.stats_cache_surface.blit(tileset.get_ui("stats_divider"), (x,y))

    y += 12
    self.stats_cache_surface.blit(tileset.get_ui("stats_title_box"), (0,y))
    write(self.stats_cache_surface, "Attributes", (12, y + 4), tileset.get_font())

    y += 36
    self.stats_cache_surface.blit(tileset.get_ui("stats_icon_third_box_large"), (0,y))
    self.stats_cache_surface.blit(tileset.get_ui("brawn_icon"), (2, y + 2))
    write_centered(self.stats_cache_surface, str(self.creature.get_attribute("Brawn")),
          (96, y + 12), tileset.get_font(26))
    x = 140
    self.stats_cache_surface.blit(tileset.get_ui("stats_icon_third_box_large"), (x,y))
    self.stats_cache_surface.blit(tileset.get_ui("agility_icon"), (x+2, y + 2))
    write_centered(self.stats_cache_surface, str(self.creature.get_attribute("Agility")),
          (x+96, y + 12), tileset.get_font(26))
    x = 280
    self.stats_cache_surface.blit(tileset.get_ui("stats_icon_third_box_large"), (x,y))
    self.stats_cache_surface.blit(tileset.get_ui("will_icon"), (x+2, y + 2))
    write_centered(self.stats_cache_surface, str(self.creature.get_attribute("Will")),
          (x+96, y + 12), tileset.get_font(26))

    x = 0
    y += 52
    self.stats_cache_surface.blit(tileset.get_ui("stats_divider"), (x,y))

    y += 12
    self.stats_cache_surface.blit(tileset.get_ui("stats_title_box"), (0,y))
    write(self.stats_cache_surface, "Stats", (12, y + 4), tileset.get_font())

    y += 36
    stats = self.creature.stats.items()
    if stats:
      for stat, value in stats:
        self.stats_cache_surface.blit(tileset.get_ui("stats_stat_box"), (0,y))
        self.stats_cache_surface.blit(tileset.get_ui("stats_question_icon"), (2, y+2))
        write_centered(self.stats_cache_surface, stat, (198, y + 4), tileset.get_font())
        if value < 0:
          colour = tileset.HP_RED
        else:
          colour = tileset.WHITE
        write_centered(self.stats_cache_surface, str(value), (390, y + 4), tileset.get_font(), colour)
        y += 36
    else:
      self.stats_cache_surface.blit(tileset.get_ui("stats_title_box"), (0,y))
      write(self.stats_cache_surface, "No stats to speak of...", (12, y + 4), tileset.get_font())
      y += 36

  def draw_inventories(self, screen: Screen):
    x,y = INVENTORIES_START_X, 0
    y = self.draw_player_inventory(screen, self.creature, x, y)

    for c in self.party:
      if c == self.creature:
        continue
      y = self.draw_player_inventory(screen, c, x, y)

  def draw_player_inventory(self, screen: Screen, creature:  Creature, x, y):
    screen.write_centered(creature.name, (x+210, y+4), screen.tileset.get_font(22))
    y += 36

    items = creature.inventory.get_unequipped_items(creature)
    num_items = len(items)
    rows = int(num_items / 8) + 1
    index = 0
    for _ in range(rows):
      for _ in range(8):
        i = None
        if index < num_items:
          i,q = items[index]

        if i and self.clicked_item == i and self.clicked_player == creature:
          box = screen.tileset.get_ui("item_icon_box_green")
        elif i and self.mouse_item == i and self.mouse_player == creature:
          box = screen.tileset.get_ui("item_icon_box_yellow")
        else:
          box = screen.tileset.get_ui("item_icon_box")
        
        screen.blit(box, (x,y))
        if i:
          screen.blit(i.icon, (x+2,y+2))
          if q > 1:
            screen.write(str(q), (x + 38, y + 34), screen.tileset.get_font(16))
        
        index += 1
        x += 52
        if index % 8 == 0:
          y += 52
    return y + 8

  def get_player_height(self, creature):
    items = creature.inventory.get_unequipped_items(creature)
    num_items = len(items)
    rows = int(num_items / 8) + 1
    return rows * 52 + 36 + 8

  def draw_player_equipment(self, screen: Screen):
    x, y = EQUIPMENT_START_X, 0
    screen.blit(self.equipment_block, (x,y))
    screen.blit(self.creature.get_sprite(86), (x + 342, y + 15))
    x += 12
    y += 6
    screen.write(self.creature.name, (x,y), screen.tileset.get_font(26))
    y += 36
    for slot in EQUIPMENT_ORDER:
      screen.blit(screen.tileset.get_ui("item_icon_box"), (x,y))
      i = self.creature.equipment.slot(slot)
      if i:
        screen.blit(i.icon, (x + 2, y + 2))
        screen.write(i.name, (x + 64, y + 14), screen.tileset.get_font())
      else:
        screen.write("<" + slot + ">", (x + 64, y + 14), screen.tileset.get_font(), screen.tileset.LIGHT_GREY)
      y += 58

  def write_item_description(self, screen: Screen):
    x, y = EQUIPMENT_START_X, 480
    i = self.mouse_item
    if not i:
      i = self.clicked_item
    if not i:
      return
    
    screen.blit(i.icon, (x + 10, y + 10))
    screen.write(i.name, (x + 64, y + 14), screen.tileset.get_font())

    x += 12
    y += 64

    lines = split_text_to_list(i.description, 392, screen.tileset.get_font(20))
    lines.append("")
    lines += self.get_item_description(i, self.creature)
    screen.write_list(lines, (x,y), screen.tileset.get_font(20))

  def get_item_description(self, item, creature):
    options = []
    if item.is_equipment():
      if creature.is_equipped(item):
        options.append("[R_CLICK]: Unequip")
      else:
        options.append("[R_CLICK]: Equip")
    if item.is_consumable():
      options.append("[R_CLICK]: Use")
    options.append("[D]: Drop")
    return options

  def update_mouse(self, x, y):
    self.mouse_item = None
    self.mouse_player = None
    if x > INVENTORIES_START_X:
      x -= INVENTORIES_START_X
      self.mouse_player, player_base_height = self.get_player_by_mouse(y)
      if self.mouse_player == None:
        return
      self.mouse_item = self.get_inventory_item_by_mouse(self.mouse_player, x, y - player_base_height)
    elif x > EQUIPMENT_START_X:
      self.mouse_item = self.get_equipped_item_by_mouse(x,y)
        
  def get_player_by_mouse(self, y):
    base_height = 0
    height = self.get_player_height(self.creature)
    if y < height:
      return self.creature, base_height
    base_height = height
    for c in self.party:
      if c == self.creature:
        continue
      height += self.get_player_height(c)
      if y < height:
        return c, base_height

      base_height = height
    return None, 0

  def get_inventory_item_by_mouse(self, creature, x, y):
    # Uses relative x and y coordinates to the start of the creature inventory block
    y -= 36   # Ignore the creature name header thing
    x_tile = x // 52
    y_tile = y // 52
    index = x_tile + y_tile * 8
    items = creature.inventory.get_unequipped_items(creature)
    i = None
    if index > -1 and index < len(items):
      i, _ = items[index]
    return i
  
  def get_equipped_item_by_mouse(self, x, y):
    x_min = EQUIPMENT_START_X + 12
    y_min = 42
    if x < x_min or x > x_min + 52:
      return None
    if y < y_min or y > y_min + (len(EQUIPMENT_ORDER)) * 58:
      return None

    for slot in EQUIPMENT_ORDER:
      if y >= y_min and y < y_min + 52:
        self.mouse_player = self.creature
        return self.creature.equipment.slot(slot)
      y_min += 58

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
        elif event.key == K_d:
          i = self.mouse_item
          p = self.mouse_player
          if not i:
            i = self.clicked_item
            p = self.clicked_player
          p.remove_item(i)
          p.world.add_item(i, (p.x, p.y))
      elif event.type == MOUSEBUTTONDOWN:
        x,y = pygame.mouse.get_pos()

        if x > INVENTORIES_START_X:
          for b in self.player_buttons:
            if b.in_bounds(x,y):
              b.click()

          self.clicked_player, player_base_height = self.get_player_by_mouse(y)
          if self.clicked_player:
            self.clicked_item = self.get_inventory_item_by_mouse(self.clicked_player, x - INVENTORIES_START_X, y - player_base_height)

            # For now, if we right clicked it then "use" the item immediately
            # Left click simply selects it
            # The creature using the item is the current selected one, so you can use items from other inventories
            if self.clicked_item and pygame.mouse.get_pressed()[2]:
              self.use_item(self.clicked_player, self.creature, self.clicked_item)
        elif x > EQUIPMENT_START_X:
          self.clicked_item = self.get_equipped_item_by_mouse(x,y)
          if self.clicked_item and pygame.mouse.get_pressed()[2]:
              self.use_item(self.creature, self.creature, self.clicked_item)
    return self

  def use_item(self, owner: Creature, creature: Creature, item):
    if item.is_equipment():
      if creature.is_equipped(item):
        creature.unequip(item)
      else:
        if owner != creature:
          owner.remove_item(item)
          creature.add_item(item)
        creature.equip(item)
    elif item.is_consumable():
      owner.remove_item(item)
      creature.add_item(item)
      item.consume(creature)
    if owner.inventory.get_quantity(item) <= 0:
      self.clicked_item = None
      self.clicked_player = None
    self.update_player_stats(self.tileset)
