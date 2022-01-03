import pygame, sys
from pygame.locals import (
  QUIT, 
  KEYDOWN,
  K_RETURN
)
from screens.screen import Screen

class Subscreen:
  def draw(self, screen: Screen):
    pass

  def respond_to_events(self, events):
    for event in events:
        if event.type == QUIT:
          pygame.quit()
          sys.exit(0)
    return self

class StartScreen(Subscreen):
  def draw(self, screen: Screen):
    screen.write_centered("Press ENTER to start the game", (screen.width / 2, screen.height / 2), screen.tileset.get_font(48))

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_RETURN:
          return None
    return self

class GameOverScreen(Subscreen):
  def draw(self, screen: Screen):
    screen.write_centered("Game Over!", (screen.width / 2, screen.height / 2 - 30), screen.tileset.get_font(48))
    screen.write_centered("Press ENTER to quit", (screen.width / 2, screen.height / 2 + 30), screen.tileset.get_font(48))
  
  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_RETURN:
          pygame.quit()
          sys.exit(0)
    return self