from skills.skill import Skill
from skills.effect_factory import EffectFactory
from skills.target import *

class SkillFactory:
  def __init__(self, effect_factory: EffectFactory):
    self.effects = effect_factory

  def embers(self):
    name = "Embers"
    skill = Skill(name, 1, "Fire", 2, 2, 0)
    skill.set_target_type(Target(8))
    skill.set_target_effect(self.effects.burning())
    return skill

  def flame_lash(self):
    name = "Flame Lash"
    skill = Skill(name, 1, "Fire", 2, 2, 0)
    skill.set_target_type(LineTarget(4))
    skill.set_target_effect(self.effects.burning())
    skill.friendly_fire = True
    return skill

  def stun(self):
    name = "Stun"
    skill = Skill(name, 0, "Accuracy", 3, 0, 3)
    skill.set_target_type(Target(5))
    skill.set_target_effect(self.effects.stunned(1))
    return skill
