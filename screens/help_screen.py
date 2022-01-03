from screens.subscreen import Subscreen
from screens.screen import Screen
from pygame.locals import (
  KEYDOWN,
  K_ESCAPE
)

class HelpScreen(Subscreen):
  def draw(self, screen: Screen):
    screen.write_centered("Welcome to my prototype!", (screen.width / 2, 4), screen.tileset.get_font())
    y = 32
    line_height = 24
    for line in [
      "Controls:",
      "Arrow keys to scroll the screen",
      "Spacebar to center screen on active player",
      "Enter to end turn",
      "Left click to move and attack",
      "[h] to view this menu",
      "[m] to show the map view to travel and rest",
      "[i] to show the inventories of your party members",
      "[s] to show the stats of your party members",
      "Escape to close this menu",
    ]:
      if line:
        screen.write(line, (32, y), screen.tileset.get_font(20))
      y += line_height
  
  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
    return self