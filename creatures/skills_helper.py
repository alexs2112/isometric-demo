# A place to organize all skills and attributes and how they affect creature stats

ATTRIBUTE_LIST = {
  "Brawn": "Increases HP, !NOT IMPLEMENTED! Inventory Limit, Minor Melee Damage",
  "Agility": "Increases Initiative, !NOT IMPLEMENTED! Evasion, Accuracy, Minor Ranged and Light Weapon Damage",
  "Will": "Increases Mana, !NOT IMPLEMENTED! Spell Slots, Resistance to Magical Effects, Minor Magical Damage"
}
SKILL_LIST = {
  # Generic
  "Endurance": "!NOT IMPLEMENTED! Increases inventory limit",
  "Awareness": "Increases Initiative",
  "Memory": "!NOT IMPLEMENTED! Increases spell slots",

  # Physical
  "Light Blades": "!NOT IMPLEMENTED! Adds critical chance for light blades",
  "Heavy Blades": "!NOT IMPLEMENTED! Additional base damage when using heavy blades",
  "Crushing": "!NOT IMPLEMENTED! A percentage of damage ignores physical armor by using crushing weapons",
  "Cleaving": "!NOT IMPLEMENTED! Deal a percentage of damage to each enemy creature adjacent to both you and the target",
  "Throwing": "!NOT IMPLEMENTED! Deal bonus base damage when throwing weapons and potions at enemies",
  "Accuracy": "!NOT IMPLEMENTED! Increases accuracy when using bows and crossbows",

  # Magical
  "Fire": "!NOT IMPLEMENTED! Burning effects deal more damage",
  "Cold": "!NOT IMPLEMENTED! A percentage of cold magic damage is also applied to physical armor",
  "Air": "!NOT IMPLEMENTED! A percentage of air magic damage is dealt to creatures adjacent to each target of the spell",
  "Poison": "!NOT IMPLEMENTED! A percentage of poison magic damage ignores magical armor",
  "Light": "!NOT IMPLEMENTED! Healing spells restore a percentage of magic armor",
  "Dark": "!NOT IMPLEMENTED! You heal for a percentage of dark magic damage dealt to health"
}

def get_hp_bonus(creature):
  x = creature.get_attribute("Brawn")
  return round(creature.max_hp * x * 0.1)

def get_initiative_bonus(creature):
  return creature.get_attribute("Agility") + creature.get_skill("Awareness")

def get_mana_bonus(creature):
  x = creature.get_attribute("Will")
  return round(creature.max_mana * x * 0.1)
