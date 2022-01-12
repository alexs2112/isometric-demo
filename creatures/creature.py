import math, random
import helpers
from items.equipment_list import EquipmentList
from items.inventory import Inventory
import world.fov as fov
from creatures.pathfinder import Path
from creatures.creature_sprite import get_sprite
from creatures.skills_helper import *
from world.world_builder import World

class Creature:
  # The absolute max amount of some expendable stats
  P_ARMOR_MAX = 6
  M_ARMOR_MAX = 6
  AP_MAX = 8

  def __init__(self, name, base_sprite, faction, world: World):
    self.name = name
    self.base_sprite = base_sprite
    self.sprite = base_sprite
    self.faction = faction
    self.world = world
    self.ai = None
    self.home_room = None
    self.messages = None
    self.effects = []
    self.inventory = Inventory()
    self.equipment = EquipmentList()
    self.spells = {}  # Spells are stored in a hash of {Spell: Prepared}
    self.spell_slots = 0
    self.loaded_spell = None
    self.attributes = {}
    self.skills = {}

  def set_ai(self, ai):
    self.ai = ai

  def set_home_room(self, room):
    self.home_room = room
  
  def set_messages(self, messages):
    self.messages = messages

  def set_base_stats(self, max_hp, max_mana, p_armor, m_armor):
    self.max_hp = max_hp
    self.hp = max_hp
    self.max_mana = max_mana
    self.mana = max_mana
    self.p_armor_cap = p_armor
    self.m_armor_cap = m_armor
    self.p_armor = p_armor
    self.m_armor = m_armor
    self.set_unarmed_stats()

  def set_misc_stats(self, max_ap=3, speed=3, vision_radius=5, initiative=3):
    self.max_ap = max_ap
    self.ap = max_ap
    self.speed = speed
    self.vision_radius = vision_radius
    self.free_movement = 0  # The remaining moves after moving, so moves arent "wasted"
    self.base_initiative = initiative
  
  def set_unarmed_stats(self, min=0, max=1, type="physical", cost=2, range=1):
    self.unarmed_min = min
    self.unarmed_max = max
    self.unarmed_type = type
    self.unarmed_cost = cost
    self.unarmed_range = range

  def is_player(self):
    if self.faction == "Player":
      return True
    else:
      return False
  
  def update_sprite(self):
    self.sprite = get_sprite(self)


#######################
# GETTERS AND SETTERS #
#######################
  def set_attributes(self, brawn, agility, will):
    self.attributes["Brawn"] = brawn
    self.attributes["Agility"] = agility
    self.attributes["Will"] = will

  def modify_attribute(self, attribute, value):
    if attribute not in ATTRIBUTE_LIST:
      raise ValueError(attribute + " is not a attribute")
    self.attributes[attribute] += value

  def get_attribute(self, attr):
    # Dont need to check if attr exists since we should always call set_attributes() on a new creature
    return self.attributes[attr]

  def modify_skill(self, skill, value):
    if skill not in SKILL_LIST:
      raise ValueError(skill + " is not a skill")
    if skill in self.skills:
      self.skills[skill] += value
    else:
      self.skills[skill] = value

  def get_skill(self, skill):
    if skill not in SKILL_LIST:
      raise ValueError(skill + " is not a skill")
    if skill in self.skills:
      return self.skills[skill]
    return 0

  def get_max_hp(self):
    return self.max_hp + self.equipment.get_bonus("MAX_HP") + get_hp_bonus(self)

  def get_max_mana(self):
    return self.max_mana + self.equipment.get_bonus("MAX_MANA") + get_mana_bonus(self)

  def get_speed(self):
    return self.speed + self.equipment.get_bonus("SPEED")
  
  def get_initiative(self):
    return self.base_initiative + self.equipment.get_bonus("INITIATIVE") + get_initiative_bonus(self)
  
  def get_spell_slots(self):
    return self.spell_slots + self.equipment.get_bonus("SPELL_SLOTS") + get_spell_slots_bonus(self)

  def get_attack_min(self):
    i = self.get_main_hand()
    if i:
      if i.is_weapon():
        return i.attack_min
    
    return self.unarmed_min + self.equipment.get_bonus("UNARMED_DAMAGE")
  
  def get_attack_max(self):
    i = self.get_main_hand()
    if i:
      if i.is_weapon():
        return i.attack_max
    
    return self.unarmed_max + self.equipment.get_bonus("UNARMED_DAMAGE")
  
  def get_attack_cost(self):
    i = self.get_main_hand()
    if i:
      if i.is_weapon():
        return i.cost
    
    return self.unarmed_cost
  
  def get_damage_type(self):
    i = self.get_main_hand()
    if i:
      if i.is_weapon():
        return i.damage_type
    
    return self.unarmed_type

  def get_attack_range(self):
    i = self.get_main_hand()
    if i:
      if i.is_weapon():
        return i.range
    
    return self.unarmed_range

  def get_p_armor_cap(self):
    return min(self.p_armor_cap + self.equipment.get_bonus("P_ARMOR"), self.P_ARMOR_MAX)
  
  def get_m_armor_cap(self):
    return min(self.m_armor_cap + self.equipment.get_bonus("M_ARMOR"), self.M_ARMOR_MAX)


######################
# ITEM RELATED STUFF #
######################
  def add_item(self, item, quantity=1):
    self.inventory.add_item(item, quantity)

  def remove_item(self, item, quantity=1):
    remaining = self.inventory.remove_item(item, quantity)
    if item.is_equipment() and self.equipment.is_equipped(item):
      if remaining <= 0:
        self.unequip(item)
  
  def unequip(self, item):
    self.equipment.remove(item)
    self.update_sprite()

  def equip(self, item):
    if self.inventory.get_quantity(item) > 0:
      if item.is_equipment():
        self.equipment.equip(item)
        self.update_sprite()
      else:
        raise ValueError("Trying to equip a non-equipment")

  def add_and_equip(self, item):
    self.inventory.add_item(item)
    self.equip(item)

  def get_main_hand(self):
    return self.equipment.slot("Main")

  def is_equipped(self, item):
    if not item.is_equipment():
      return False
    return self.equipment.is_equipped(item)


######################
# TURN RELATED STUFF #
######################
  def upkeep(self):
    self.loaded_spell = None
    self.ap = self.max_ap
    self.free_movement = 0

    for e in self.effects:
      e.update(self)

  def full_rest(self):
    self.rest()
    self.hp = self.get_max_hp()

  def rest(self):
    self.upkeep()
    self.m_armor = self.get_m_armor_cap()
    self.p_armor = self.get_p_armor_cap()
    self.mana = self.get_max_mana()
    self.notify(self.name + " is feeling refreshed!")

  # Returns if this creatures turn is complete after making this move
  def take_turn(self):
    if self.ai:
      return self.ai.take_turn(self.world)
    return True
  
  def add_effect(self, effect):
    if effect:
      effect.apply(self)


########################
# COMBAT RELATED STUFF #
########################
  # If this creature is actively hunting a player
  def is_active(self):
    if self.ai:
      return self.ai.is_active()
    return False
  
  def can_be_activated(self):
    return self.faction not in ["Player", "Plant"]

  def activate(self, creature=None):
    if self.ai.can_activate():
      self.ai.activate(creature)
      if self.world.in_combat():
        self.world.add_creature_to_combat(self)
      else:
        self.world.start_combat()


##########################
# MOVEMENT RELATED STUFF #
##########################
  def can_enter(self, x, y):
    if self.world.is_floor(x, y) and not self.world.get_creature_at_location(x,y):
      return True

  def move_relative(self, dx, dy):
    if self.world.is_floor(self.x + dx, self.y + dy):
      self.x += dx
      self.y += dy
    
  def move(self, x, y, cost=1):
    if self.free_movement < cost and self.ap <= 0:
      return
    if self.can_enter(x, y):
      self.x = x
      self.y = y

      if self.world.in_combat():
        if self.free_movement < cost:
          self.ap -= 1
          self.free_movement += self.get_speed()
        self.free_movement -= cost

      if self.is_player():
        self.world.update_fov(self)

  def move_to(self, x, y):
    if self.world.is_floor(x, y):
      self.x = x
      self.y = y
      if self.is_player():
        self.world.update_fov(self)

  def get_possible_distance(self):
    if self.world.in_combat():
      return self.get_speed() * self.ap + self.free_movement
    else:
      return 100

  def get_path_to(self, dx, dy):
    if self.world.outside_world(dx,dy) or not (self.world.is_floor(dx,dy) and self.world.has_seen(dx,dy)):
      return []

    path = Path(self, dx, dy).points
    return path

  def move_along_path(self, path):
    self.world.add_player_move(self, path)

  def move_along_path_old(self, path):
    # Still used for party movement, this will be removed when we fix that to work with animated movement
    path = path[:self.get_possible_distance()]
    distance = len(path)
    if distance == 0:
      return
    if self.is_player():
      for (x,y) in path:
        # Probably figure out a better way to handle stopping movement if combat starts
        before = self.world.in_combat()
        self.move_to(x, y)
        if before == False and self.world.in_combat() == True:
          return
    else:
      x,y = path[-1]
      self.move_to(x, y)
    
    if self.world.in_combat():
      ap_cost, free_movement = self.cost_of_path(path)
      self.ap -= ap_cost
      self.free_movement = free_movement
  
  def cost_of_path(self, path):
    distance = len(path)
    if distance == 0:
      return (0, self.free_movement)
    remaining_distance = max(0, distance - self.free_movement)
    leftover_free_movement = max(0, self.free_movement - distance)
    ap_cost = math.ceil(remaining_distance / self.get_speed())
    rem = (remaining_distance % self.get_speed())
    if rem > 0:
      leftover_free_movement += self.get_speed() - rem
    return (ap_cost, leftover_free_movement)


########################
# MEMORY RELATED STUFF #
########################
  def can_see(self, to_x, to_y):
    return fov.can_see(self.world, self.x, self.y, to_x, to_y, self.vision_radius)
  
  def has_seen(self, to_x, to_y):
    return self.world.has_seen(to_x, to_y)

  def notify(self, message):
    if self.messages != None:
      print(message)
      self.messages.append(message)
    
  def notify_player(self, message):
    for p in self.world.players:
      if p.can_see(self.x, self.y):
        p.notify(message)
        break


########################
# ATTACK RELATED STUFF #
########################
  def heal(self, amount):
    self.hp = min(self.get_max_hp(), self.hp + random.randint(3, 8))
    self.notify_player(self.name + " heals " + str(amount) + " HP!")

  def take_damage(self, damage, type, piercing=0):
    if piercing > 0:  # Ignores armor
      self.hp -= min(damage, piercing)
      damage -= min(damage, piercing)
    if type == "physical":
      amount = max(0, damage - self.p_armor)
      self.p_armor = max(0, self.p_armor - damage)
    elif type == "magical":
      amount = max(0, damage - self.m_armor)
      self.m_armor = max(0, self.m_armor - damage)
    self.hp -= amount
    if self.hp <= 0:
      self.die()
  
  def die(self):
    self.notify_player(self.name + " dies!")
    for item, quantity in self.inventory.get_items():
      self.world.add_item(item, (self.x, self.y), quantity)
    self.world.remove_creature(self)

  # Get a line constrained by our range that stops before a wall or at another creature
  def get_attack_line(self, tile_x, tile_y):
    path = []
    l = helpers.get_line(self.x, self.y, tile_x, tile_y)
    for (x,y) in l[1:self.get_attack_range() + 1]:
      if not self.world.is_floor(x,y):
        return path, None
      path.append((x,y))
      c = self.world.get_creature_at_location(x,y)
      if c:
        return path, c
    return path, None

  def attack_creature(self, target):
    if self.is_player() and target.is_player():
      self.notify("Are you sure you want to attack a party member?")
      return

    r = self.get_attack_range()
    if abs(self.x - target.x) > r or abs(self.y - target.y) > r:
      self.notify("The " + target.name + " is out of range!")
      return

    if self.ap < self.get_attack_cost():
      self.notify(self.name + " does not have enough AP to attack!")
      return

    if self.world.in_combat():
      self.ap -= self.get_attack_cost()

    # Damage will be weighted towards the average, biased to be rounded up because of .5s
    atk_min = self.get_attack_min()
    atk_max = self.get_attack_max()
    damage = random.randint(atk_min, atk_max) + random.randint(atk_min, atk_max)
    damage = round(damage/2)
    damage_type = self.get_damage_type()

    w = self.get_main_hand()

    critical = False
    piercing = 0
    if w and w.is_weapon():
      source = w.name
      if w.get_type() == "Light Blade":
        if random.random() * 10 < self.get_skill("Light Blades"):
          critical = True
          damage = damage * 2
      if w.get_type() == "Heavy Blade":
        damage += self.get_skill("Heavy Blades")
      if w.get_type() == "Crushing":
        piercing = self.get_skill("Crushing")
    else:
      source = "Unarmed"
      damage += self.get_skill("Unarmed")

    self_string = self.name + " attacks " + target.name + " for " + str(damage) + " " + damage_type + " damage!"
    target_string = target.name + " gets attacked by " + self.name + " for " + str(damage) + " " + damage_type + " damage!"

    self_string += " [" + source + "]"
    target_string += " [" + source + "]"

    if critical:
      self_string += " (CRITICAL)"
      target_string += " (CRITICAL)"

    self.notify(self_string)
    target.notify(target_string)
    target.take_damage(damage, damage_type, piercing)


#######################
# SPELL RELATED STUFF #
#######################
  def spell_list(self):
    return list(self.spells.keys())

  def get_prepared_spells(self):
    out = []
    for s in self.spell_list():
      if self.spell_prepared(s):
        out.append(s)
    return out
  
  def get_unprepared_spells(self):
    out = []
    for s in self.spell_list():
      if not self.spell_prepared(s):
        out.append(s)
    return out
  
  def add_spell(self, spell):
    if spell not in self.spells:
      self.spells[spell] = False

  def get_remaining_spell_slots(self):
    v = self.get_spell_slots()
    for spell in self.get_prepared_spells():
      v -= spell.get_level()
    return v

  def can_prepare(self, spell):
    if spell in self.spells and not self.spells[spell]:
      if self.get_skill(spell.get_type()) >= spell.get_level():
        if self.get_remaining_spell_slots() >= spell.get_level():
          return True
    return False

  def prepare_spell(self, spell):
    if spell in self.spells:
      self.spells[spell] = True

  def unprepare_spell(self, spell):
    if spell in self.spells:
      self.spells[spell] = False

  def spell_prepared(self, spell):
    if spell in self.spells:
      return self.spells[spell]
    return False

  def load_spell(self, spell):
    self.loaded_spell = spell

  def knows_spell(self, spell_name):
    return spell_name in self.spells
