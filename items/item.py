class Item:
  def __init__(self, name, icon, unique=False):
    self.name = name
    self.icon = icon

    # If the item can be stacked in inventory or not
    # Unique items are all individual objects, non-unique items are all pointers to the same object
    self.unique = unique
  
  def is_equipment(self):
    return False

class Equipment(Item):
  def __init__(self, name, icon, slot):
    super().__init__(name, icon)
    self.slot = slot

    # Let the bonuses the item provides be a hash where we can search for
    # bonus type by key
    # Example: { "p_armor" : 1 } to add an additional 1 to the p_armor cap
    self.bonuses = {}

    # In case we are attacking with this item and we need to check the damage type
    self.damage_type = "physical"
  
  def set_bonus(self, name, value):
    self.bonuses[name] = value
  
  def get_bonus(self, name):
    if name in self.bonuses:
      return self.bonuses[name]
    return 0
  
  def is_equipment(self):
      return True