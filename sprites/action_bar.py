import pygame
from pygame.locals import ( K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0 )
from screens.screen import Screen, Button

# A way to store and update the buttons and icons for abilities and items for each player character
class ActionBar:
  def __init__(self, creature, screen_x, screen_y):
    self.creature = creature
    self.buttons = [None] * 10   # A list of tuples of [(Button: Skill/Item) | None]

    # Some hardcoded values when it is initialized in case we want to shift it around on the screen later in development
    self.screen_x, self.screen_y = screen_x, screen_y

    button_full = pygame.image.load("assets/ui/main_buttons.png")
    self.button_default = button_full.subsurface((0,0,52,52))
    self.button_select = button_full.subsurface((52,0,52,52))
    self.button_click = button_full.subsurface((104,0,52,52))
    self.dark_highlight = button_full.subsurface((156,0,52,52))

  def update(self):
    # Update is slow and should only be called when necessary
    # - When a player is initialized
    # - When a player adds or removes a consumable
    # - When a player prepares or unprepares a skill
    self.buttons = [None] * 10  # A bit of a lazy solution, we won't bother with letting unchanged buttons persist through updates
    x, y = self.screen_x, self.screen_y

    index = 0
    for s in self.creature.get_prepared_skills():
      b = Button((x,y,52,52), self.button_default, self.button_select, self.button_click, self.get_skill_function(s))
      self.buttons[index] = (b,s)
      index += 1
      x += 52

    for i, _ in self.creature.inventory.get_items():
      if i.is_consumable():
        b = Button((x,y,52,52), self.button_default, self.button_select, self.button_click, self.get_consumable_function(i))
        self.buttons[index] = (b,i)
        index += 1
        x += 52

  def set_button(self, element, index):
    # Element: Item | Skill
    if element.is_skill():
      f = self.get_skill_function(element)
    else:
      f = self.get_consumable_function(element)
    b = Button((self.screen_x + index * 52, self.screen_y, 52, 52), self.button_default, self.button_select, self.button_click, f)
    self.buttons[index] = (b, element)
  
  # Add a button to the first available spot
  def add_button(self, element):
    for i in range(10):
      if self.buttons[i] == None:
        self.set_button(element, i)
        return True
    return False

  def remove_button(self, element):
    for i in range(10):
      if self.buttons[i][1] == element:
        self.buttons[i] = None
        return i
    return -1

  def get_skill_function(self, skill):
    def func():
      if skill.cast_check(self.creature):
        self.creature.load_skill(skill)
    return func
  
  def get_consumable_function(self, item):
    def func():
      item.consume(self.creature)
    return func

  def draw(self, screen: Screen, mouse_x, mouse_y):
    x, y = self.screen_x, self.screen_y
    for i in range(10):
      if self.buttons[i]:
        b,o = self.buttons[i]
        screen.blit(o.icon, (x+2, y+2))
        screen.blit(b.get_image(mouse_x, mouse_y), (x,y))

        if o.is_skill():
          if not o.is_castable(self.creature):
            screen.blit(self.dark_highlight, (x,y))
          if o.downtime > 0:
            screen.write_centered(str(o.downtime), (x + 26, y + 6), screen.tileset.get_font(32))
        else:
          q = self.creature.inventory.get_quantity(o)
          if q > 1:
            screen.write(str(q), (x + 6, y + 6), screen.tileset.get_font(16))

        if b.in_bounds(mouse_x, mouse_y):
          screen.write_centered(o.name, (x + 26, y - 18), screen.tileset.get_font(16))
      else:
        screen.blit(self.button_default, (x,y))

      if i == 9: key = 0
      else: key = i+1
      screen.write(str(key), (x + 36, y + 32), screen.tileset.get_font(16))
      x += 52
  
  def activate(self, key):
    if key == K_1: i = 0
    elif key == K_2: i = 1
    elif key == K_3: i = 2
    elif key == K_4: i = 3
    elif key == K_5: i = 4
    elif key == K_6: i = 5
    elif key == K_7: i = 6
    elif key == K_8: i = 7
    elif key == K_9: i = 8
    elif key == K_0: i = 9
    else: return

    if self.buttons[i]:
      self.buttons[i][0].click()

  def mouse_click(self, mouse_x, mouse_y):
    for i in range(10):
      if self.buttons[i]:
        b, _ = self.buttons[i]
        b.click_if_in_bounds(mouse_x, mouse_y)
