from spells.spell import Spell
from spells.effect_factory import EffectFactory
from spells.target import *

class SpellFactory:
  def __init__(self, effect_factory: EffectFactory):
    self.effects = effect_factory

  def embers(self):
    name = "Embers"
    spell = Spell(name, 1, "Fire", 2, 2, 0)
    spell.set_target_type(Target(8))
    spell.set_target_effect(self.effects.burning())
    return spell

  def flame_lash(self):
    name = "Flame Lash"
    spell = Spell(name, 1, "Fire", 2, 2, 0)
    spell.set_target_type(LineTarget(4))
    spell.set_target_effect(self.effects.burning())
    spell.friendly_fire = True
    return spell

  def stun(self):
    name = "Stun"
    spell = Spell(name, 0, "Accuracy", 3, 0, 3)
    spell.set_target_type(Target(5))
    spell.set_target_effect(self.effects.stunned(1))
    return spell
