from skills.effect import Effect
from skills.target import Target

class Skill:
  def __init__(self, name, icon, level, type, ap_cost, mana_cost, cooldown):
    self.name = name
    self.icon = icon
    self.level = level
    self.type = type
    self.ap_cost = ap_cost
    self.cooldown = cooldown
    self.downtime = 0
    self.target_type = Target(0)
    self.mana_cost = mana_cost
    self.caster_effect = None
    self.target_effect = None
    self.friendly_fire = False
    self.basic_attack = False     # For now if this is true just call attack on each target

  def get_type(self):
    return self.type
  
  def get_level(self):
    return self.level

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

  def tick_downtime(self):
    self.downtime = max(0, self.downtime - 1)
  
  def reset_downtime(self):
    self.downtime = 0

  def is_castable(self, caster):
    if not caster.skill_prepared(self) or \
       self.ap_cost > caster.ap or \
       self.mana_cost > caster.mana or \
       self.downtime > 0:
       return False
    return True

  def cast(self, caster, target_list):
    if not self.cast_check(caster):
      return
    if caster.world.in_combat():
      caster.ap -= self.ap_cost
    caster.mana -= self.mana_cost
    self.downtime = self.cooldown
    caster.notify_player(caster.name + " uses " + self.name)
    caster.add_effect(self.caster_effect)
    for c in target_list:
      c.add_effect(self.target_effect)
      if self.basic_attack:
        caster.force_attack(c)
  
  def cast_check(self, caster):
    if self.ap_cost > caster.ap:
      caster.notify(caster.name + " does not have enough action points to cast " + self.name + ".")
      return False
    elif self.mana_cost > caster.mana:
      caster.notify(caster.name + " does not have enough mana to cast " + self.name + ".")
      return False
    elif self.downtime > 0:
      caster.notify(self.name + " is still on cooldown.")
      return False
    elif not self.is_castable(caster):
      caster.notify(self.name + " cannot be activated.")
      return False
    return True

  def clone(self):
    new = Skill(self.name, self.icon, self.level, self.type, self.ap_cost, self.mana_cost, self.cooldown)
    new.set_target_type(self.get_target_type())
    new.set_caster_effect(self.caster_effect)
    new.set_target_effect(self.target_effect)
    return new
