import pygame
from creatures.creature import Creature
from world.world_builder import World
from screens.screen import Screen
from tileset import TileSet
from helpers import get_tile_position, is_ne_wall, is_nw_wall, is_outer_corner

def initialize_screen(width, height):
  display = pygame.display.set_mode((width, height))
  tileset = TileSet()
  return Screen(width, height, display, tileset)

def write_active_player(screen: Screen, active: Creature):
  x = 12
  y = 2
  screen.write(active.name + "'s Turn", (x, y), screen.tileset.get_font())
  if active.ap == 0 and active.free_movement == 0:
    y += 26
    screen.write("Out of AP, press Enter to end turn", (x, y), screen.tileset.get_font())
  if active.loaded_spell:
    y += 26
    screen.write("Casting " + active.loaded_spell.name, (x, y), screen.tileset.get_font())
  
  if not active.world.no_active_enemies():
    screen.write_centered("Combat!", (screen.width/2, 2), screen.tileset.get_font(), screen.tileset.HP_RED)

def draw_player_stats(screen: Screen, active: Creature, path=[], target: Creature = None):
  x, y = screen.width - 256, 0
  x, y = draw_player_name_box(screen, active, x, y)
  x, y = draw_player_health_mana_armor(screen, active, x, y)

  screen.blit(screen.tileset.get_ui("player_action_points"), (x, y))

  if active.world.in_combat():
    if active.loaded_spell:
      cost = active.loaded_spell.ap_cost
      free_movement = active.free_movement
    elif target:
      cost = active.get_attack_cost()
      free_movement = active.free_movement
    else:
      cost, free_movement = active.cost_of_path(path)
  else:
    cost = 0
    free_movement = active.free_movement

  leftover_ap = active.ap - cost
  for i in range(leftover_ap):
    screen.blit(screen.tileset.get_ui("ap_active"), (x + 3 + i * 25, y + 4))
  for i in range(cost):
    screen.blit(screen.tileset.get_ui("ap_cost"), (x + 3 + leftover_ap * 25 + i * 25, y + 4))
  for i in range(active.max_ap - active.ap):
    screen.blit(screen.tileset.get_ui("ap_inactive"), (x + 3 + active.ap * 25 + i * 25, y + 4))
  
  if free_movement == active.free_movement:
    colour = screen.tileset.WHITE
  else:
    colour = screen.tileset.HP_RED
  screen.write_centered(str(free_movement), (x + 238, y + 4), screen.tileset.get_font(20), colour)

def display_messages(screen: Screen, messages):
  y = screen.height - 30
  message_height = 20
  y -= message_height * len(messages)
  for i in range(len(messages)):
    message = messages[i]
    screen.write(message, (12, y + i * message_height), screen.tileset.get_font(18))

def draw_world(screen: Screen, world: World):
  width, height = world.dimensions()
  creature_locations = world.creature_location_dict()
  for x in range(width):
    for y in range(height):
      if not world.has_seen(x,y):
        continue
      sx, sy = get_tile_position(screen.offset_x, screen.offset_y, x * 32, y * 32)
      if sx < -96 or sy < -64 or sx > screen.width or sy > screen.height:
        continue

      tileset_id = world.tile(x,y).tileset_id
      if world.is_floor(x,y):
        screen.blit(screen.tileset.get_floor(tileset_id), (sx, sy))

        feature = world.get_feature(x,y)
        if feature:
          screen.blit(feature.get_image(), (sx + feature.get_tile_blit_x_mod(), sy + feature.get_tile_blit_y_mod()))
          if not world.can_see(x,y):
            screen.blit(feature.get_shadow(), (sx + feature.get_tile_blit_x_mod(), sy + feature.get_tile_blit_y_mod()))
        items = world.get_inventory(x,y)
        if items:
          screen.blit(screen.tileset.get_misc("satchel"), (sx + 16, sy - 4))

        if world.can_see(x,y):
          if (x,y) in creature_locations:
            creature = creature_locations[(x,y)]
            screen.blit(creature.sprite, (sx + 16, sy - 16))
            draw_healthbar(screen, creature, sx, sy)
        else:
          screen.blit(screen.tileset.get_ui("floor_highlight_dark"), (sx, sy))
      else:
        # These need to be if statements in case its both NW and NE wall (corners)
        nw_wall = is_nw_wall(world, x, y)
        ne_wall = is_ne_wall(world, x, y)
        if is_outer_corner(world, x, y):
          corner_x, corner_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32 + 4, y * 32 - 20)
          screen.blit(screen.tileset.get_corner(tileset_id), (corner_x, corner_y))
        if nw_wall:
          screen.blit(screen.tileset.get_nw_wall(tileset_id), (sx + 24, sy - 20))
        if ne_wall:
          screen.blit(screen.tileset.get_ne_wall(tileset_id), (sx, sy - 20))
        if nw_wall and ne_wall:
          corner_x, corner_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32 + 4, y * 32 - 20)
          screen.blit(screen.tileset.get_corner(tileset_id), (corner_x, corner_y))

        if not world.can_see(x,y):
          if nw_wall or ne_wall:
            screen.blit(screen.tileset.get_ui("wall_highlight_dark"), (sx, sy - 16))

def get_healthbar(tileset: TileSet, creature: Creature):
  quarter = creature.get_max_hp() / 4
  if creature.hp == creature.get_max_hp():
    return None
  elif creature.hp > 3 * quarter:
    return tileset.get_ui("health_full")
  elif creature.hp > 2 * quarter:
    return tileset.get_ui("health_most")
  elif creature.hp > quarter:
    return tileset.get_ui("health_half")
  else:
    return tileset.get_ui("health_quarter")

def draw_healthbar(screen: Screen, creature: Creature, x, y):
  healthbar = get_healthbar(screen.tileset, creature)
  p_arm = screen.tileset.get_ui("armor_physical_bar")
  m_arm = screen.tileset.get_ui("armor_magical_bar")
  ax = x + 16  
  ay = y + 14
  for i in range(creature.p_armor):
    screen.blit(p_arm, (ax + 5 * i, ay))

  # Start layering the p_armor and m_armor
  if creature.p_armor + creature.m_armor > 6:
    ay -= 6
  
  # Otherwise show p_armor to the left and m_armor to the right
  else:
    ax += 34 - 5 * creature.m_armor
    
  for i in range(creature.m_armor):
    screen.blit(m_arm, (ax + 5 * i, ay))

  if healthbar:
    screen.blit(healthbar, (x + 16, y + 20))
  
  # For debugging a creatures active state
  if not creature.is_active() and creature.can_be_activated():
    ay -= 10
    screen.blit(screen.tileset.get_ui("inactive_icon"), (x + 16, ay))

def draw_player_name_box(screen: Screen, creature: Creature, x, y):
  screen.blit(screen.tileset.get_ui("player_name"), (x + 7, y))
  screen.write_centered(creature.name, (x + 128, y + 5), screen.tileset.get_font(20))
  return (x, y + 32)

def draw_player_health_mana_armor(screen: Screen, creature: Creature, start_x, start_y):
  screen.blit(screen.tileset.get_ui("player_health_and_armor"), (start_x, start_y))

  hp_x = start_x
  hp_y = start_y
  percentage = creature.hp / creature.get_max_hp()
  pygame.draw.rect(screen.display, screen.tileset.HP_RED, (hp_x + 5, hp_y + 5, int(246 * percentage), 23))
  hp_string = str(creature.hp) + "/" + str(creature.get_max_hp())
  screen.write_centered(hp_string, (hp_x + 128, hp_y + 6), screen.tileset.get_font(20))

  mana_x = hp_x
  mana_y = hp_y + 31
  if creature.mana > 0:
    percentage = creature.mana / creature.get_max_mana()
    pygame.draw.rect(screen.display, screen.tileset.MANA_BLUE, (mana_x + 5, mana_y + 6, int(246 * percentage), 23))
  mana_string = str(creature.mana) + "/" + str(creature.get_max_mana())
  screen.write_centered(mana_string, (mana_x + 128, mana_y + 6), screen.tileset.get_font(20))

  p_armor_x = mana_x
  armor_y = mana_y + 32
  p_armor = creature.p_armor
  rem = creature.get_p_armor_cap() - p_armor
  for i in range(p_armor):
    screen.blit(screen.tileset.get_ui("armor_physical"), (p_armor_x + 5 + i * 20, armor_y + 4))
  for i in range(rem):
    screen.blit(screen.tileset.get_ui("armor_used"), (p_armor_x + 5 + p_armor * 20 + i * 20, armor_y + 4))
  m_armor_x = mana_x + 128
  m_armor = creature.m_armor
  rem = creature.get_m_armor_cap() - m_armor
  for i in range(m_armor):
    screen.blit(screen.tileset.get_ui("armor_magical"), (m_armor_x + 3 + i * 20, armor_y + 4))
  for i in range(rem):
    screen.blit(screen.tileset.get_ui("armor_used"), (m_armor_x + 3 + m_armor * 20 + i * 20, armor_y + 4))
  
  # Return the bottom left coordinate of this UI element so we can stack more underneath it
  return (p_armor_x, armor_y + 32)

def draw_path_to_mouse(screen: Screen, creature: Creature, x, y):
  # If we are not in combat and we mouse over an inventory or feature, highlight it in yellow
  i = creature.world.get_inventory(x,y)
  f = creature.world.get_feature(x,y)
  if not creature.world.in_combat():
    if (i or f) and creature.simple_distance_to(x,y) <= 1:
      iso_x, iso_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32, y * 32)
      screen.blit(screen.tileset.get_ui("floor_highlight_yellow"), (iso_x, iso_y))
      return [], None

  # If we mouse over a creature and are able to attack it, show the attack interface
  c = creature.world.get_creature_at_location(x, y)
  if c:
    # If we aren't in combat and mouse over a player, highlight them in purple to select them
    if c.is_player() and not creature.world.in_combat():
        iso_x, iso_y = get_tile_position(screen.offset_x, screen.offset_y, c.x * 32, c.y * 32)
        screen.blit(screen.tileset.get_ui("floor_highlight_purple"), (iso_x, iso_y))
        return [], None

    attack_path, target = creature.get_attack_line(x,y)
    if target and creature.ap >= creature.get_attack_cost():
      for (dx,dy) in attack_path:
        iso_x, iso_y = get_tile_position(screen.offset_x, screen.offset_y, dx * 32, dy * 32)
        screen.blit(screen.tileset.get_ui("floor_highlight_red"), (iso_x, iso_y))
      return [], target

  path = creature.get_path_to(x, y)

  # If we mouse over something and are not in range to attack/interact with it, show movement next to it
  if c or i or f:
    path = path[:-1]

  # Highlight the tiles in green to move to the location
  path = path[:creature.get_possible_distance()]
  for tile in path:
    tile_x, tile_y = tile
    iso_x, iso_y = get_tile_position(screen.offset_x, screen.offset_y, tile_x * 32, tile_y * 32)
    screen.blit(screen.tileset.get_ui("floor_highlight_green"), (iso_x, iso_y))
  return path, None

def highlight_ability_target(screen: Screen, creature: Creature, tile_x, tile_y):
  tiles = creature.loaded_spell.get_target_tiles(creature.x, creature.y, tile_x, tile_y)
  creatures = creature.world.creature_location_dict()
  for x,y in tiles:
    if creature.world.is_floor(x,y):
      if (x,y) in creatures:
        if not creature.loaded_spell.friendly_fire:
          if creatures[(x,y)].faction == creature.faction:
            continue
        highlight = screen.tileset.get_ui("floor_highlight_red")
      else:
        highlight = screen.tileset.get_ui("floor_highlight_blue")
      iso_x, iso_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32, y * 32)
      screen.blit(highlight, (iso_x, iso_y))
  return tiles

def show_mouse_tooltips(screen: Screen, world: World, mouse_x, mouse_y, tile_x, tile_y):
  if world.outside_world(tile_x, tile_y) or not world.has_seen(tile_x, tile_y):
    return
  lines = []
  
  # Showing creature names in tooltips gets cluttered quickly
  # c = world.get_creature_at_location(tile_x, tile_y)
  # if c:
  #   lines.append(c.name)
  
  i = world.get_inventory(tile_x, tile_y)
  if i:
    c = i.number_of_different_items()
    if c > 3:
      lines.append(str(c) + " different items...")
    for item, quantity in i.get_items():
      s = ""
      if quantity > 1:
        s += str(quantity) + " "
      s += item.name
      if quantity > 1:
        s += "s"
      lines.append(s)

  font = screen.tileset.get_font(16)
  if lines:
    line_height = 18
    line_width = 0
    for line in lines:
      new_width, _ = font.size(line)
      if new_width > line_width:
        line_width = new_width
    x = mouse_x
    y = mouse_y - line_height * len(lines)
    i = 0
    for line in lines:
      pygame.draw.rect(screen.display, screen.tileset.DARK_GREY, (x, y + i * line_height, line_width + 4, line_height))
      screen.write(line, (x+2, y + i * line_height), font)
      i += 1
