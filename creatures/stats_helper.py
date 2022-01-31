# A place to organize all stats and attributes and how they affect creatures

ATTRIBUTE_LIST = {
  "Brawn": "Increases HP (2 HP per point), !NOT IMPLEMENTED! Inventory Limit, Minor Melee Damage",
  "Agility": "Increases Initiative (1 Initiative per point), !NOT IMPLEMENTED! Evasion, Accuracy, Minor Ranged and Light Weapon Damage",
  "Will": "Increases Mana (2 Mana per point), Skill Slots (1 slot per point), !NOT IMPLEMENTED! Resistance to Magical Effects, Minor Magical Damage"
}
STAT_LIST = {
  # Generic
  "Endurance": "Minorly Increases HP (1 HP per point), !NOT IMPLEMENTED! Increases inventory limit",
  "Awareness": "Increases Initiative (1 Initiative per point)",
  "Memory": "Increases skill slots (1 slot per point)",

  # Physical
  "Light Blades": "Adds critical chance for light blades (10% per point)",
  "Heavy Blades": "Additional base damage when using heavy blades (1 damage per point)",
  "Crushing": "A guaranteed amount of damage ignores physical armor by using crushing weapons (1 damage per point)",
  "Cleaving": "!NOT IMPLEMENTED! Deal a percentage of damage to each enemy creature adjacent to both you and the target when using cleaving weapons",
  "Polearms": "!NOT IMPLEMENTED!",
  "Accuracy": "!NOT IMPLEMENTED! Increases accuracy when using bows and crossbows",
  "Unarmed": "Increases damage with unarmed strikes (1 damage per point)",

  # Magical
  "Fire": "!NOT IMPLEMENTED! Burning effects deal more damage",
  "Cold": "!NOT IMPLEMENTED! A percentage of cold magic damage is also applied to physical armor",
  "Air": "!NOT IMPLEMENTED! A percentage of air magic damage is dealt to creatures adjacent to each target of the spell",
  "Poison": "!NOT IMPLEMENTED! A percentage of poison magic damage ignores magical armor",
  "Light": "!NOT IMPLEMENTED! Healing spells restore a percentage of magic armor",
  "Dark": "!NOT IMPLEMENTED! You heal for a percentage of dark magic damage dealt to health",
  "Summoning": "!NOT IMPLEMENTED! Magically summoned creatures have better stats"
}

def get_hp_bonus(creature):
  x = creature.get_attribute("Brawn")
  y = creature.get_stat("Endurance")
  return x * 2 + y

def get_initiative_bonus(creature):
  return creature.get_attribute("Agility") + creature.get_stat("Awareness")

def get_mana_bonus(creature):
  x = creature.get_attribute("Will")
  return x * 2

def get_skill_slots_bonus(creature):
  x = creature.get_attribute("Will")
  y = creature.get_stat("Memory")
  return x + y

PHYSICAL_DAMAGE = [
  "slashing",
  "piercing",
  "crushing"
]
MAGICAL_DAMAGE = [
  "fire",
  "cold",
  "air",
  "poison",
  "light",
  "dark"
]
def is_damage_physical(type):
  return type in PHYSICAL_DAMAGE
def is_damage_magical(type):
  return type in MAGICAL_DAMAGE
