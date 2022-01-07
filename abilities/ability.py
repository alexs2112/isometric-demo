class Ability:
  def __init__(self, name, cost, cooldown):
    self.name = name
    self.ap_cost = cost
    self.cooldown = cooldown

  def is_spell(self):
    return False

class Spell(Ability):
  def __init__(self, name, ap_cost, mana_cost, cooldown):
    super().__init__(name, ap_cost, cooldown)
    self.mana_cost = mana_cost

  def is_spell(self):
    return True
