from items.item import Item

# Store all items available in an inventory
# Can be on a tile, in a chest, on a creature, etc
class Inventory:
  def __init__(self):
    # Stored by item: quantity
    self.items = {}
  
  def add_item(self, item: Item, quantity=1):
    if item in self.items:
      self.items[item] += quantity
    else:
      self.items[item] = quantity

  def remove_item(self, item: Item, quantity=1):
    if item in self.items:
      if self.items[item] < quantity:
        raise ValueError("Trying to remove more items than an inventory has!")
      self.items[item] -= quantity
      rem = self.items[item]
      if self.items[item] <= 0:
        self.items.pop(item)
      return rem
    else:
      return 0
    
  def get_quantity(self, item: Item):
    if item in self.items:
      return self.items[item]
    else:
      return 0
    
  def get_items(self):
    return list(self.items.items())

  def number_of_different_items(self):
    return len(self.items.keys())

  def get_item_at_index(self, index):
    i = 0
    for item, quantity in self.get_items():
      if i == index:
        return item, quantity
    return (None, 0)
