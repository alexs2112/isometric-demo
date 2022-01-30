from screens.screen import Screen
from screens.subscreen import Subscreen
from screens.main_graphics import draw_player_stats
from creatures.creature import Creature
from pygame.locals import (
  KEYDOWN,
  K_UP,
  K_DOWN,
  K_RETURN,
  K_ESCAPE
)

class SkillScreen(Subscreen):
  def __init__(self, creature: Creature):
    self.creature = creature
    self.index = 0
    self.section = 0
    self.initialize_lists(creature)
    
  def initialize_lists(self, creature: Creature):
    self.prepared = creature.get_prepared_skills()
    self.unprepared = creature.get_unprepared_skills()
    if self.section == 1 and self.index == 0 and len(self.unprepared) == 0:
      self.section = 0
      self.index = len(self.prepared) - 1
    elif self.section == 0 and self.index > len(self.prepared) - 1:
      self.section = 1
      self.index = 0

  def draw(self, screen: Screen):
    draw_player_stats(screen, self.creature)
    
    x1 = 12
    x2 = x1 + 250
    x3 = x2 + 75
    x4 = x3 + 75
    x5 = x4 + 150
    x6 = x5 + 100
    y = 12
    line_height = 28
    screen.write("Spells Screen (Temporary)", (x1, y), screen.tileset.get_font())
    x1 += 12
    y += line_height

    screen.write("Prepared Spells", (x1, y), screen.tileset.get_font())
    screen.write("AP", (x2, y), screen.tileset.get_font())
    screen.write("Mana", (x3, y), screen.tileset.get_font())
    screen.write("Cooldown", (x4, y), screen.tileset.get_font())
    screen.write("Type", (x5, y), screen.tileset.get_font())
    screen.write("Level", (x6, y), screen.tileset.get_font())
    y += line_height
    x1 += 12
    if self.prepared:
      for i in range(len(self.prepared)):
        s = self.prepared[i]
        if i == self.index and self.section == 0:
          if s.is_castable(self.creature):
            colour = screen.tileset.EQUIPPED_GREEN
          else:
            colour = screen.tileset.ORANGE
        else:
          if s.is_castable(self.creature):
            colour = screen.tileset.WHITE
          else:
            colour = screen.tileset.HP_RED
        y = self.write_spell(screen, s, line_height, y, x1, x2, x3, x4, x5, x6, colour)
    else:
      screen.write(self.creature.name + " has no prepared spells.", (x1, y), screen.tileset.get_font())
      y += line_height
    y += line_height / 2

    if self.unprepared:
      screen.write("Unprepared Spells", (x1-12, y), screen.tileset.get_font())
      y += line_height
      for i in range(len(self.unprepared)):
        s = self.unprepared[i]
        if i == self.index and self.section == 1:
          if self.creature.can_prepare(s):
            colour = screen.tileset.EQUIPPED_GREEN
          else:
            colour = screen.tileset.ORANGE
        else:
          if self.creature.can_prepare(s):
            colour = screen.tileset.WHITE
          else:
            colour = screen.tileset.HP_RED
        y = self.write_spell(screen, s, line_height, y, x1, x2, x3, x4, x5, x6, colour)
    
  def write_spell(self, screen, spell, line_height, y, x1, x2, x3, x4, x5, x6, colour):
    screen.write(spell.name, (x1, y), screen.tileset.get_font(), colour)

    if spell.cooldown > 0:
      cd = str(spell.cooldown)
    else:
      cd = "None"
    screen.write(str(spell.ap_cost), (x2, y), screen.tileset.get_font(), colour)
    screen.write(str(spell.mana_cost), (x3, y), screen.tileset.get_font(), colour)
    screen.write(cd, (x4, y), screen.tileset.get_font(), colour)
    screen.write(spell.get_type(), (x5, y), screen.tileset.get_font(), colour)
    screen.write(str(spell.get_level()), (x6, y), screen.tileset.get_font(), colour)

    return y + line_height

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
        elif event.key == K_UP:
          if self.index == 0 and self.section == 1 and len(self.prepared) > 0:
              self.index = len(self.prepared) - 1
              self.section = 0
          else:
            self.index = max(0, self.index - 1)
        elif event.key == K_DOWN:
          if self.section == 0:
            if self.index == len(self.prepared) - 1:
              self.section = 1
              self.index = 0
            else:
              self.index = min(len(self.prepared) - 1, self.index + 1)
          else:
            self.index = min(len(self.unprepared) - 1, self.index + 1)
        elif event.key == K_RETURN:
          if self.section == 0:
            if self.prepared[self.index].is_castable(self.creature):
              self.creature.load_skill(self.prepared[self.index])
              return None
          else:
            if self.creature.can_prepare(self.unprepared[self.index]):
              self.creature.prepare_skill(self.unprepared[self.index])
              self.initialize_lists(self.creature)
    return self
