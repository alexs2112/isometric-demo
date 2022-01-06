from items.item import Equipment

# A way to store and easily search all the equipped items on a creature
class EquipmentList:
  def __init__(self):
    # Stored by slot: item
    self.items = {
      # Armor
      "Chest" : None,
      "Head" : None,
      "Feet" : None,
      "Hands" : None,
      "Cloak" : None,

      # Trinkets
      "Ring" : None,   # Eventually let creatures equip up to two rings
      # Eventually add amulets if we want, but Im not sure how to make them unique from rings yet

      # Main Hand + Off Hand
      "Main" : None,
      "Off" : None     # Eventually let creatures equip weapons in the off hand to dual wield
    }

  def equip(self, item: Equipment):
    self.items[item.slot] = item
  
  def remove(self, item: Equipment):
    # Just remove whatever is at that slot
    self.items[item.slot] = None
  
  def is_equipped(self, item: Equipment):
    if self.items[item.slot] == item:
      return True
    else:
      return False
  
  def slot(self, slot):
    return self.items[slot]

  def get_bonus(self, bonus):
    v = 0
    for _, item in self.items.items():
      if item:
        v += item.get_bonus(bonus)
    return v
