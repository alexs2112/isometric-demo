from screens.screen import Screen
from screens.subscreen import Subscreen
from creatures.creature import Creature
from pygame.locals import (
  KEYDOWN,
  K_ESCAPE
)

class StatsScreen(Subscreen):
  def __init__(self, party):
    self.party = party

  def draw(self, screen: Screen):
    line_height = 24
    y = 4
    x0 = 20
    x1 = 240
    x2 = 460
    screen.write_centered("Stats Screen (Debugging)", (screen.width / 2, y), screen.tileset.get_font())
    y += 28
    for c in self.party:
      screen.write(c.name, (12, y), screen.tileset.get_font(20))
      y += line_height
      screen.write("HP: " + str(c.hp) + "/" + str(c.get_max_hp()), (x0, y), screen.tileset.get_font(20))
      screen.write("Mana: " + str(c.mana) + "/" + str(c.get_max_mana()), (x1, y), screen.tileset.get_font(20))
      y += line_height
      screen.write("Physical Armor: " + str(c.p_armor) + "/" + str(c.get_p_armor_cap()), (x0, y), screen.tileset.get_font(20))
      screen.write("Magical Armor: " + str(c.m_armor) + "/" + str(c.get_m_armor_cap()), (x1, y), screen.tileset.get_font(20))
      y += line_height
      screen.write("Action Points: " + str(c.ap) + "/" + str(c.max_ap), (x0, y), screen.tileset.get_font(20))
      screen.write("Speed: " + str(c.get_speed()), (x1, y), screen.tileset.get_font(20))
      screen.write("Free Movement: " + str(c.free_movement), (x2, y), screen.tileset.get_font(20))
      y += line_height
      screen.write("Attack: " + str(c.get_attack_min()) + "-" + str(c.get_attack_max()), (x0, y), screen.tileset.get_font(20))
      screen.write("Cost: " + str(c.get_attack_cost()), (x1, y), screen.tileset.get_font(20))
      y += line_height

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
    return self