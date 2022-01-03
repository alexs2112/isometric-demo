import pygame
from creatures.creature import Creature
from world.world_builder import World
from screens.screen import Screen
from tileset import TileSet
from helpers import get_tile_position, is_ne_wall, is_nw_wall, is_outer_corner

def initialize_screen(width, height):
  tileset = TileSet()
  display = pygame.display.set_mode((width, height))
  return Screen(width, height, display, tileset)

def draw_interface(screen: Screen, active: Creature, path):
  start_x = screen.width - 256
  start_y = 0
  screen.blit(screen.tileset.get_ui("player_base_stats"), (start_x, start_y))

  hp_x = start_x
  hp_y = start_y
  percentage = active.hp / active.max_hp
  pygame.draw.rect(screen.display, screen.tileset.HP_RED, (hp_x + 6, hp_y + 6, int(244 * percentage), 36))
  hp_string = str(active.hp) + "/" + str(active.max_hp)
  screen.write_centered(hp_string, (hp_x + 128, hp_y + 10), screen.tileset.get_font())

  mana_x = hp_x
  mana_y = hp_y + 46
  if active.mana > 0:
    percentage = active.mana / active.max_mana
    pygame.draw.rect(screen.display, screen.tileset.MANA_BLUE, (mana_x + 5, mana_y + 6, int(246 * percentage), 23))
  mana_string = str(active.mana) + "/" + str(active.max_mana)
  screen.write_centered(mana_string, (mana_x + 128, mana_y + 6), screen.tileset.get_font(20))

  p_armor_x = mana_x
  armor_y = mana_y + 32
  p_armor = active.p_armor
  rem = active.p_armor_cap - p_armor
  for i in range(p_armor):
    screen.blit(screen.tileset.get_ui("armor_physical"), (p_armor_x + 5 + i * 20, armor_y + 4))
  for i in range(rem):
    screen.blit(screen.tileset.get_ui("armor_used"), (p_armor_x + 5 + p_armor * 20 + i * 20, armor_y + 4))
  m_armor_x = mana_x + 128
  m_armor = active.m_armor
  rem = active.m_armor_cap - m_armor
  for i in range(m_armor):
    screen.blit(screen.tileset.get_ui("armor_magical"), (m_armor_x + 3 + i * 20, armor_y + 4))
  for i in range(rem):
    screen.blit(screen.tileset.get_ui("armor_used"), (m_armor_x + 3 + m_armor * 20 + i * 20, armor_y + 4))

  ap_x = p_armor_x
  ap_y = armor_y + 32
  cost, free_movement = active.cost_of_path_with_attacks(path)
  leftover_ap = active.ap - cost
  for i in range(leftover_ap):
    screen.blit(screen.tileset.get_ui("ap_active"), (ap_x + 3 + i * 25, ap_y + 5))
  for i in range(cost):
    screen.blit(screen.tileset.get_ui("ap_cost"), (ap_x + 3 + leftover_ap * 25 + i * 25, ap_y + 5))
  for i in range(active.max_ap - active.ap):
    screen.blit(screen.tileset.get_ui("ap_inactive"), (ap_x + 3 + active.ap * 25 + i * 25, ap_y + 5))
  
  if free_movement == active.free_movement:
    colour = screen.tileset.WHITE
  else:
    colour = screen.tileset.HP_RED
  screen.write_centered(str(free_movement), (ap_x + 238, ap_y + 6), screen.tileset.get_font(20), colour)

  screen.write(active.name + "'s Turn", (12, 2), screen.tileset.get_font())
  if active.ap == 0 and active.free_movement == 0:
    screen.write("Out of AP, press Enter to end turn", (12, 28), screen.tileset.get_font())

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
        screen.blit(screen.tileset.get_floor(tileset_id), (get_tile_position(screen.offset_x, screen.offset_y, x * 32, y * 32)))
        if (x,y) in creature_locations:
          creature = creature_locations[(x,y)]
          p_x, p_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32, y * 32)
          screen.blit(creature.icon, (p_x + 16, p_y - 16))
          healthbar = get_healthbar(screen.tileset, creature)
          for i in range(creature.p_armor):
            screen.blit(screen.tileset.get_ui("armor_physical_bar"), (p_x + 16 + 4 * i, p_y + 16))
          for i in range(creature.m_armor):
            screen.blit(screen.tileset.get_ui("armor_magical_bar"), (p_x + 48 - 4 * (i+1), p_y + 16))
          if healthbar:
            screen.blit(healthbar, (p_x + 16, p_y + 20))
      else:
        # These need to be if statements in case its both NW and NE wall (corners)
        nw_wall = is_nw_wall(world, x, y)
        ne_wall = is_ne_wall(world, x, y)
        iso_x, iso_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32, y * 32)
        if is_outer_corner(world, x, y):
          corner_x, corner_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32 + 4, y * 32 - 20)
          screen.blit(screen.tileset.get_corner(tileset_id), (corner_x, corner_y))
        if nw_wall:
          screen.blit(screen.tileset.get_nw_wall(tileset_id), (iso_x + 32 - 8, iso_y - 16 - 4))
        if ne_wall:
          screen.blit(screen.tileset.get_ne_wall(tileset_id), (iso_x, iso_y - 16 - 4))
        if nw_wall and ne_wall:
          corner_x, corner_y = get_tile_position(screen.offset_x, screen.offset_y, x * 32 + 4, y * 32 - 20)
          screen.blit(screen.tileset.get_corner(tileset_id), (corner_x, corner_y))
        # We probably want to handle corners on the left and right so that it looks like a corner when only one wall is shown
        # This might be a massive pain in the ass to how we are drawing walls, maybe redo it

def get_healthbar(tileset: TileSet, creature: Creature):
  quarter = creature.max_hp / 4
  if creature.hp == creature.max_hp:
    return None
  elif creature.hp > 3 * quarter:
    return tileset.get_ui("health_full")
  elif creature.hp > 2 * quarter:
    return tileset.get_ui("health_most")
  elif creature.hp > quarter:
    return tileset.get_ui("health_half")
  else:
    return tileset.get_ui("health_quarter")

def draw_path_to_mouse(screen: Screen, creature: Creature, x, y):
  path = creature.get_path_to(x, y)[:creature.get_possible_distance()]
  if len(path) > 0:
    # If we cannot afford to make an attack at the end of the move, remove the last tile
    ap_cost, _ = creature.cost_of_path_with_attacks(path)
    if ap_cost <= creature.ap:
      c = creature.world.get_creature_at_location(path[-1][0], path[-1][1])
    else:
      c = None
      path = path[:-1]
  for tile in path:
    tile_x, tile_y = tile
    iso_x, iso_y = get_tile_position(screen.offset_x, screen.offset_y, tile_x * 32, tile_y * 32)

    if c:
      highlight = screen.tileset.get_ui("floor_highlight_red")
    else:
      highlight = screen.tileset.get_ui("floor_highlight_green")
    screen.blit(highlight, (iso_x, iso_y))
  return path
