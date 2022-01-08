from spells.spell import Spell
from spells.effect_factory import EffectFactory
from spells.target import LineTarget

class SpellFactory:
  def __init__(self, effect_factory: EffectFactory):
    self.effects = effect_factory

  def flame_lash(self):
    name = "Flame Lash"
    spell = Spell(name, 2, 2, 0)
    spell.set_target_type(LineTarget(5))
    spell.set_target_effect(self.effects.burning())
    spell.friendly_fire = True
    print(spell.target_type)
    return spell