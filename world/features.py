class Feature:
  def __init__(self, image, shadow=None):
    self.image = image
    self.shadow = shadow

  def interact(self, creature):
    pass

  def get_image(self):
    return self.image
  
  def get_shadow(self):
    return self.shadow

  def see_through(self):
    return True
  
  def move_through(self):
    return True

  def get_tile_blit_x_mod(self):
    return 0
  
  def get_tile_blit_y_mod(self):
    return 0

class Door(Feature):
  def __init__(self, orientation, close_image, open_image, shadow):
    super().__init__(close_image, shadow)
    self.orientation = orientation  # 0 is east, 1 is west
    self.close_image = close_image
    self.open_image = open_image
    self.opened = False
  
  def get_image(self):
    if self.opened:
      return self.open_image
    else:
      return self.close_image

  def interact(self, creature):
    self.opened = not self.opened
    creature.world.update_fov(creature)
  
  def see_through(self):
    return self.opened
  
  def move_through(self):
    return self.opened

  def get_tile_blit_x_mod(self):
    return 12
  
  def get_tile_blit_y_mod(self):
    return -26