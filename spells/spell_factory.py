from spells.spell import Spell
from spells.effect_factory import EffectFactory
from spells.target import *

class SpellFactory:
  def __init__(self, effect_factory: EffectFactory):
    self.effects = effect_factory

  def embers(self):
    name = "Embers"
    spell = Spell(name, 2, 2, 0)
    spell.set_target_type(Target(8))
    spell.set_target_effect(self.effects.burning())
    return spell

  def flame_lash(self):
    name = "Flame Lash"
    spell = Spell(name, 2, 2, 0)
    spell.set_target_type(LineTarget(4))
    spell.set_target_effect(self.effects.burning())
    spell.friendly_fire = True
    return spell