from spells.effect import Effect
from spells.target import Target
from creatures.creature import Creature

class Spell:
  def __init__(self, name, ap_cost, mana_cost, cooldown):
    self.name = name
    self.ap_cost = ap_cost
    self.cooldown = cooldown
    self.downtime = 0
    self.target_type = Target(0)
    self.mana_cost = mana_cost
    self.caster_effect = None
    self.target_effect = None
    self.friendly_fire = False

  def set_target_type(self, target_type: Target):
    self.target_type = target_type

  def get_target_tiles(self, sx, sy, dx, dy):
    return self.target_type.get_points(sx, sy, dx, dy)

  def get_target_type(self):
    return self.target_type

  def set_caster_effect(self, effect: Effect):
    self.caster_effect = effect
  
  def set_target_effect(self, effect: Effect):
    self.target_effect = effect

  def cast(self, caster: Creature, target_list):
    if self.ap_cost > caster.ap:
      caster.notify(caster.name + " does not have enough action points to cast " + self.name + ".")
      return
    if self.mana_cost > caster.mana:
      caster.notify(caster.name + " does not have enough mana to cast " + self.name + ".")
      return
    if self.downtime > 0:
      caster.notify(self.name + " is still on cooldown.")
      return
    
    caster.notify_player(caster.name + " casts " + self.name)
    caster.ap -= self.ap_cost
    caster.mana -= self.mana_cost
    self.downtime = self.cooldown
    caster.add_effect(self.caster_effect)
    for c in target_list:
      c.add_effect(self.target_effect)

  def clone(self):
    new = Spell(self.name, self.ap_cost, self.mana_cost, self.cooldown)
    new.set_target_type(self.get_target_type())
    new.set_caster_effect(self.caster_effect)
    new.set_target_effect(self.target_effect)
    return new
