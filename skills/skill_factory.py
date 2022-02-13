from skills.skill import Skill
from skills.effect_factory import EffectFactory
from skills.target import *
from sprites.tileset import TileSet
from sprites.projectile import Projectile

ALL_SKILLS = [
# Comment hashes denote icons used from https://game-icons.net/ for temporary use
  "Stun",                 #
  "Rapid Slashes",        #
  "Fire Vulnerability",   #
  "Cleave",               #
  "Embers",               #
  "Flame Lash"            #
]

class SkillFactory:
  def __init__(self, tileset: TileSet, effect_factory: EffectFactory):
    self.tileset = tileset
    self.effects = effect_factory

  def stun(self):
    name = "Stun"
    skill = Skill(name, self.tileset.get_skill_icons(name), 0, "Accuracy", 2, 0, 3)
    skill.set_target_type(Target(5))
    skill.set_target_effect(self.effects.stunned(1))
    skill.set_description("Target creature in range becomes stunned for their next turn, unable to take actions.")
    return skill
  
  def rapid_slashes(self):
    name = "Rapid Slashes"
    skill = Skill(name, self.tileset.get_skill_icons(name), 0, "Unarmed", 0, 0, 2)
    skill.set_target_type(SelfTarget())
    skill.set_target_effect(self.effects.rapid_slashes(1))
    skill.set_description("You fly into a frenzy, unarmed attacks with your claws only cost 1 AP this turn.")
    skill.friendly_fire = True
    return skill

  def fire_vulnerability(self):
    name = "Fire Vulnerability"
    skill = Skill(name, self.tileset.get_skill_icons(name), 0, "Fire", 1, 1, 4)
    skill.set_target_type(Target(6))
    skill.set_target_effect(self.effects.modify_resistance("fire", -2, 3))
    skill.set_description("Target creature becomes vulnerable to fire damage, taking 2 additional damage from fire sources for 3 turns.")
    return skill
  
  def cleave(self):
    name = "Cleave"
    skill = Skill(name, self.tileset.get_skill_icons(name), 0, "Cleaving", 2, 0, 2)
    skill.set_target_type(AdjacentTarget(1))
    skill.basic_attack = True
    skill.set_description("Swing your weapon in an arc around you, making an attack against each adjacent enemy.")
    return skill

  def embers(self):
    name = "Embers"
    skill = Skill(name, self.tileset.get_skill_icons(name), 0, "Fire", 2, 2, 0)
    skill.set_target_type(Target(6))
    skill.set_target_effect(self.effects.burning())
    skill.set_projectile(self.tileset.get_projectile("fire_cloud"))
    skill.set_description("Ignite target creature. They take some upfront fire damage and catch fire for the next several turns.")
    return skill

  def flame_lash(self):
    name = "Flame Lash"
    skill = Skill(name, self.tileset.get_skill_icons(name), 1, "Fire", 2, 2, 0)
    skill.set_target_type(LineTarget(4))
    skill.set_target_effect(self.effects.burning())
    skill.set_projectile(self.tileset.get_projectile("fire_cloud"))
    skill.friendly_fire = True
    skill.set_description("Lash out with a whip of fire, each creature hit takes fire damage and catches fire for a few turns.")
    return skill  

  def poison_bite(self):
    name = "Bite"
    skill = Skill(name, None, 0, "Unarmed", 2, 0, 2)
    skill.set_target_type(Target(1))
    skill.set_target_effect(self.effects.poisoned(3))
    skill.basic_attack = True
    skill.set_description("Bite target adjacent enemy with your venomous fangs, making a basic attack and poisoning them for 3 turns.")
    return skill
  
  def toxic_spores(self):
    name = "Toxic Spores"
    skill = Skill(name, None, 0, "Poison", 2, 0, 1)
    skill.set_target_type(Target(1))
    skill.set_target_effect(self.effects.toxic_spores(2))
    skill.set_projectile(self.tileset.get_projectile("poison_cloud"))
    skill.set_description("Target creature adjacent to you becomes engulfed in poisonous spores, becoming poisoned for 2 turns.")
    return skill
