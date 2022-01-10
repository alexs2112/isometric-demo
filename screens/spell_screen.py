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

class SpellScreen(Subscreen):
  def __init__(self, creature: Creature):
    self.creature = creature
    self.index = 0
    self.spells = creature.get_spells()

  def draw(self, screen: Screen):
    s = self.spells[self.index]
    if not s.is_castable(self.creature):
      s = None
    draw_player_stats(screen, self.creature)
    
    x1 = 12
    y = 12
    line_height = 28
    screen.write("Spells Screen (Temporary)", (x1, y), screen.tileset.get_font())
    x1 += 12
    x2 = 400
    x3 = 600
    x4 = 800
    screen.write("AP Cost", (x2, y), screen.tileset.get_font())
    screen.write("Mana Cost", (x3, y), screen.tileset.get_font())
    screen.write("Cooldown", (x4, y), screen.tileset.get_font())
    y += line_height
    
    for i in range(len(self.spells)):
      s = self.spells[i]
      if i == self.index:
        if s.is_castable(self.creature):
          colour = screen.tileset.EQUIPPED_GREEN
        else:
          colour = screen.tileset.ORANGE
      else:
        if s.is_castable(self.creature):
          colour = screen.tileset.WHITE
        else:
          colour = screen.tileset.HP_RED

      name = s.name
      ap = str(s.ap_cost)
      mana = str(s.mana_cost)

      if s.cooldown > 0:
        cd = str(s.cooldown)
      else:
        cd = "None"

      screen.write(name, (x1, y), screen.tileset.get_font(), colour)
      screen.write(ap, (x2, y), screen.tileset.get_font(), colour)
      screen.write(mana, (x3, y), screen.tileset.get_font(), colour)
      screen.write(cd, (x4, y), screen.tileset.get_font(), colour)

      y += line_height

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
        elif event.key == K_UP:
          self.index = max(0, self.index - 1)
        elif event.key == K_DOWN:
          self.index = min(len(self.spells) - 1, self.index + 1)
        elif event.key == K_RETURN:
          if self.spells[self.index].is_castable(self.creature):
            self.creature.load_spell(self.spells[self.index])
            return None
    return self