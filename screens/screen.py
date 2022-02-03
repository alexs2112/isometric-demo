from msilib.schema import TextStyle
import helpers
from sprites.tileset import TileSet
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
    if image == None:
      return
    self.display.blit(image, coords)

  def write(self, text, coords, font, colour=(255,255,255)):
    write(self.display, text, coords, font, colour)

  def write_centered(self, text, coords, font, colour=(255,255,255)):
    write_centered(self.display, text, coords, font, colour)
  
  def write_right_aligned(self, text, coords, font, colour=(255,255,255)):
    write_right_aligned(self.display, text, coords, font, colour)
  
  def write_list(self, text_list, coords, font, colour=(255,255,255)):
    x, y = coords
    if not text_list:
      return y
    _, height = font.size(text_list[0])
    for line in text_list:
      self.write(line, (x,y), font, colour)
      y += height
    return y

def write(surface, text, coords, font, colour=(255,255,255)):
  text_surface = font.render(text, False, colour)
  surface.blit(text_surface, coords)

def write_centered(surface, text, coords, font, colour=(255,255,255)):
  width, _ = font.size(text)
  (x,y) = coords
  x -= width / 2
  write(surface, text, (x,y), font, colour)

def write_right_aligned(surface, text, coords, font, colour=(255,255,255)):
  width, _ = font.size(text)
  (x,y) = coords
  x -= width
  write(surface, text, (x,y), font, colour)

def split_text_to_list(text, width, font):
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

class Button:
  def __init__(self, rect, default_image, mouse_image=None, click_image=None, func=None):
    self.rect = rect
    self.x = rect[0]
    self.y = rect[1]
    self.width = rect[2]
    self.height = rect[3]

    self.default_image = default_image
    self.mouse_image = mouse_image
    self.click_image = click_image

    self.func = func

    # How many frames we want to show the click_image for after being clicked
    self.click_frames = 0

    self.tooltip = None
    self.tooltip_delay = 0
    self.tooltip_size = 0
    self.tooltip_frames = 0
    self.active = True

    self.text = None
    self.text_size = 0

  def in_bounds(self, mouse_x, mouse_y):
    return mouse_x >= self.x and mouse_y >= self.y and mouse_x < self.x + self.width and mouse_y < self.y + self.height

  def get_image(self, mouse_x, mouse_y):
    if self.click_frames > 0 and self.click_image:
      self.click_frames -= 1
      return self.click_image
    if self.in_bounds(mouse_x, mouse_y) and self.mouse_image:
      return self.mouse_image
    return self.default_image

  def set_tooltip(self, text, delay=0, size=16):
    self.tooltip = text
    self.tooltip_delay = delay
    self.tooltip_size = size
  
  def set_text(self, text, size=24):
    self.text = text
    self.text_size = size

  def click(self, *args):
    if not self.active:
      return

    if self.click_image:
      self.click_frames = 2
    if self.func:
      return self.func(*args)
  
  def click_if_in_bounds(self, mouse_x, mouse_y, *args):
    if self.in_bounds(mouse_x, mouse_y):
      self.click(*args)

  def draw(self, screen: Screen, mouse_x, mouse_y):
    if not self.active:
      return

    screen.blit(self.get_image(mouse_x, mouse_y), (self.x, self.y))

    if self.text:
      screen.write_centered(self.text, (self.x + self.width // 2, self.y + (self.height - self.text_size) // 2), screen.tileset.get_font(self.text_size))

    if self.tooltip:
      bounds = self.in_bounds(mouse_x, mouse_y)
      if self.tooltip_delay > 0:
        if bounds:
          self.tooltip_frames += 1
        else:
          self.tooltip_frames = 0

      if bounds and self.tooltip_frames >= self.tooltip_delay:
        screen.write_centered(self.tooltip, (self.x + self.width // 2, self.y - self.tooltip_size - 2), screen.tileset.get_font(self.tooltip_size))
