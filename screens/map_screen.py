import pygame
from screens.subscreen import Subscreen
from screens.screen import Screen
from screens.main_graphics import draw_player_name_box, draw_player_health_mana_armor
from world.world_builder import Room, World
from creatures.creature import Creature
from helpers import get_tile_position, get_cartesian_position
from pygame.locals import (
  MOUSEBUTTONDOWN,
  KEYDOWN,
  K_RIGHT,
  K_LEFT,
  K_UP,
  K_DOWN,
  K_ESCAPE,
  K_r
)

class MapScreen(Subscreen):
  def __init__(self, world: World, screen: Screen, active: Creature):
    self.world = world
    self.clicked_room = None
    self.message = ""

    # Figure out a better way to do these parameters
    self.map_offset_x, self.map_offset_y = self.center_map_offset(screen, active)

  def draw(self, screen: Screen):
    self.draw_world(screen)
    if self.clicked_room:
      self.highlight_room(screen, self.clicked_room)

    x, y = screen.width - 256, 24
    for p in self.world.players:
      x, y = draw_player_name_box(screen, p, x, y)
      x, y = draw_player_health_mana_armor(screen, p, x, y)
      y += 24
    
    screen.write_centered("Press [r] to rest", (x + 128, y), screen.tileset.get_font())

    if self.message:
      screen.write_centered(self.message, (screen.width / 2, screen.height - 64), screen.tileset.get_font())
    screen.write_centered("Double click a room to travel there", (screen.width / 2, screen.height - 32), screen.tileset.get_font())
  
  def center_map_offset(self, screen, creature):
    return get_tile_position((screen.width / 2), (screen.height / 2), creature.x * 16, creature.y * 16)

  def draw_world(self, screen: Screen):
    width, height = self.world.dimensions()
    creature_locations = self.world.creature_location_dict()
    for x in range(width):
      for y in range(height):
        if not self.world.has_seen(x,y):
          continue
        sx, sy = get_tile_position(self.map_offset_x, self.map_offset_y, x * 16, y * 16)
        if sx < -48 or sy < -32 or sx > screen.width + 48 or sy > screen.height + 32:
          continue
        
        tileset_id = self.world.tile(x,y).tileset_id
        if self.world.is_floor(x,y):
          sx, sy = get_tile_position(self.map_offset_x, self.map_offset_y, x * 16, y * 16)
          screen.blit(screen.tileset.get_floor_small(tileset_id), (sx, sy))
          if (x,y) in creature_locations:
            c = creature_locations[(x,y)]
            if c.is_player():
              icon = screen.tileset.get_ui("map_player_dot")
            else:
              icon = screen.tileset.get_ui("map_enemy_dot")
            screen.blit(icon, (sx + 4, sy + 4))
        """
        # For now going to see how this goes without displaying the walls
        else:
          nw_wall = is_nw_wall(self.world, x, y)
          ne_wall = is_ne_wall(self.world, x, y)
          iso_x, iso_y = get_tile_position(self.map_offset_x, self.map_offset_y, x * 16, y * 16)
          if is_outer_corner(self.world, x, y):
            corner_x, corner_y = get_tile_position(self.map_offset_x, self.map_offset_y, x * 16 + 2, y * 16 - 10)
            screen.blit(screen.tileset.get_corner_small(tileset_id), (corner_x, corner_y))
          if nw_wall:
            screen.blit(screen.tileset.get_nw_wall_small(tileset_id), (iso_x + 16 - 4, iso_y - 8 - 2))
          if ne_wall:
            screen.blit(screen.tileset.get_ne_wall_small(tileset_id), (iso_x, iso_y - 8 - 2))
          if nw_wall and ne_wall:
            corner_x, corner_y = get_tile_position(self.map_offset_x, self.map_offset_y, x * 16 + 2, y * 16 - 10)
            screen.blit(screen.tileset.get_corner_small(tileset_id), (corner_x, corner_y))
        """
  
  def highlight_room(self, screen: Screen, room: Room):
    tiles = room.get_tiles()
    for tile in tiles:
      x, y = tile
      sx, sy = get_tile_position(self.map_offset_x, self.map_offset_y, x * 16, y * 16)
      if sx < -48 or sy < -32 or sx > screen.width + 48 or sy > screen.height + 32:
        continue
      screen.blit(screen.tileset.get_ui("map_floor_orange"), (sx,sy))

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          if self.clicked_room:
            self.clicked_room = None
          else:
            return None
        elif event.key == K_r:
          if self.world.no_active_enemies():
            for p in self.world.players:
              p.rest()
              return None
          else:
            self.message = "Cannot rest, there are enemies nearby!"
      if event.type == MOUSEBUTTONDOWN:
        self.message = ""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        new_clicked_room = self.get_room_by_click(mouse_x, mouse_y)
        if new_clicked_room != self.clicked_room:
          self.clicked_room = new_clicked_room
        else: # They are the same, try to move the players there
          if self.world.no_active_enemies():
            if self.clicked_room:
              self.move_party_to_room(self.clicked_room)
              return None
          else:
            self.message = "Cannot travel, there are active enemies!"
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
      self.map_offset_x += 15
    if keys[K_LEFT]:
      self.map_offset_x -= 15
    if keys[K_UP]:
      self.map_offset_y -= 15
    if keys[K_DOWN]:
      self.map_offset_y += 15
    return self
    
  def get_room_by_click(self, mouse_x, mouse_y):
    mouse_x += self.map_offset_x
    mouse_y += self.map_offset_y
    mouse_x -= 16
    tile_x, tile_y = get_cartesian_position(mouse_x / 16, mouse_y / 16)
    if self.world.outside_world(tile_x, tile_y) or not self.world.has_seen(tile_x, tile_y):
      self.message = "You have not seen this tile"
      return
    room = self.world.get_room_by_tile(tile_x, tile_y)
    if not room:
      return
    if not room.is_explored(self.world):
      self.message = "You have not fully explored this room!"
      room = None
      return
    return room
  
  def move_party_to_room(self, room):
    for p in self.world.players:
      x, y = self.world.get_random_floor_in_room(room)
      p.move_to(x,y)
      p.upkeep()
