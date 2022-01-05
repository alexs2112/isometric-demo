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

  def clear(self):
    self.display.fill((0,0,0))

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
  
  def split_text_to_list(self, text, width, font):
    # Take a string and split it into a list of strings, where each list element is no wider than width
    # This is to cache the text to write it afterwards so we don't recalculate it every time
    words = text.split(' ')
    output = []
    current = words[0]
    for word in words[1:]:
      new_word = " " + word
      if font.size(current + new_word)[0] > width:
        output.append(current)
        current = word
      else:
        current += new_word
    output.append(current)
    return output
  
  def write_list(self, text_list, coords, font, colour=(255,255,255)):
    x, y = coords
    if not text_list:
      return y
    _, height = font.size(text_list[0])
    for line in text_list:
      self.write(line, (x,y), font, colour)
      y += height
    return y
