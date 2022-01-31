class Item:
  def __init__(self, name, icon, unique=False):
    self.name = name
    self.icon = icon

    # If the item can be stacked in inventory or not
    # Unique items are all individual objects, non-unique items are all pointers to the same object
    self.unique = unique

    self.description = "This item doesn't have a description yet"
  
  def is_equipment(self):
    return False
  
  def is_weapon(self):
    return False

  def is_consumable(self):
    return False

  def set_description(self, desc):
    self.description = desc

class Equipment(Item):
  def __init__(self, name, icon, sprite, slot):
    super().__init__(name, icon)
    self.sprite = sprite
    self.slot = slot
    self.tags = []

    # Let the bonuses the item provides be a hash where we can search for
    # bonus type by key
    # Example: { "p_armor" : 1 } to add an additional 1 to the p_armor cap
    self.bonuses = {}
  
  def set_bonus(self, name, value):
    self.bonuses[name] = value
  
  def get_bonus(self, name):
    if name in self.bonuses:
      return self.bonuses[name]
    return 0
  
  def all_bonuses(self):
    return list(self.bonuses.items())
  
  def is_equipment(self):
    return True

  def add_tag(self, tag):
    self.tags.append(tag)
  
  def has_tag(self, tag):
    if tag in self.tags:
      return True
    else:
      return False

  def get_tags(self):
    return self.tags

class Weapon(Equipment):
  VALID_TYPES = [
    "Light Blade",
    "Heavy Blade",
    "Crushing",
    "Cleaving",
    "Polearm",
    "Ranged"
  ]

  def __init__(self, name, icon, sprite, type):
    super().__init__(name, icon, sprite, "Main")  # For now weapons can only be equipped in the main hand
    self.set_stats(0,1)
    self.projectile = None

    if type in Weapon.VALID_TYPES:
      self.type = type
    else:
      raise ValueError(type + " is not a valid weapon type!")
  
  def set_stats(self, attack_min, attack_max, damage_type="crushing", range=1, cost=2):
    self.attack_min = attack_min
    self.attack_max = attack_max
    self.damage_type = damage_type
    self.range = range
    self.cost = cost
  
  def get_type(self):
    return self.type

  def is_weapon(self):
    return True

  def weapon_string(self):
    return str(self.attack_min) + "-" + str(self.attack_max) + " " + self.damage_type + " damage. " + "[RANGE=" + str(self.range) + "] [COST=" + str(self.cost) + "]"
  
  def set_projectile(self, projectile):
    self.projectile = projectile

class Potion(Item):
  def __init__(self, name, icon):
    super().__init__(name, icon)
  
  def set_effect(self, effect):
    self.effect = effect

  def is_consumable(self):
    return True

  def consume(self, creature):
    creature.notify_player(creature.name + " drinks the " + self.name)
    creature.add_effect(self.effect)
    return True

class Tome(Item):
  def __init__(self, name, icon, skill):
    super().__init__(name, icon)
    self.skill = skill

  def is_consumable(self):
    return True

  def consume(self, creature):
    if creature.knows_skill(self.skill.name):
      creature.notify(creature.name + " already knows " + self.skill.name + ".")
      return False
    else:
      creature.notify_player(creature.name + " absorbs the magical knowledge of " + self.name + "!")
      creature.add_skill(self.skill.clone())
      return True
