import helpers
from tileset import TileSet
from pygame import Surface

# A simple object to hold a bunch of useful information for the screen
class Screen:
  def __init__(self, width, height, display: Surface, tileset: TileSet):
    self.width = width
    self.height = height
    self.display = display
    self.tileset = tileset
    self.offset_x = 0
    self.offset_y = 0
  
  def center_offset_on_creature(self, creature):
    self.offset_x, self.offset_y = helpers.get_tile_position((self.width / 2), (self.height / 2), creature.x * 32, creature.y * 32)
    self.offset_x += 32
  
  def blit(self, image, coords):
    # A simple wrapper so we don't need to call screen.display.blit(...)
    self.display.blit(image, coords)

  def write(self, text, coords, font, colour=(255,255,255)):
    text_surface = font.render(text, False, colour)
    self.display.blit(text_surface, coords)
  
  def write_centered(self, text, coords, font, colour=(255,255,255)):
    width, _ = font.size(text)
    (x,y) = coords
    x -= width / 2
    self.write(text, (x,y), font, colour)