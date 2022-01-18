import pygame
from screens.screen import Screen
from screens.subscreen import Subscreen
from creatures.creature import Creature
from creatures.skills_helper import ATTRIBUTE_LIST, SKILL_LIST
from pygame.locals import (
  KEYDOWN,
  K_ESCAPE
)

class CharacterScreen(Subscreen):
  def __init__(self, creature: Creature):
    self.creature = creature

    # Don't cache this rather large image in tileset
    self.stats_block = pygame.image.load("assets/screens/player_stats_block.png")
  
  def draw(self, screen: Screen):
    # Left: All stats, attributes, and skills. Increase them on level up here
    screen.blit(self.stats_block, (0,0))
    font = screen.tileset.get_font()
    screen.write_centered("Stats (Temporary)", (210, 12), font)
    text = [
      "HP: " + str(self.creature.hp) + "/" + str(self.creature.get_max_hp()),
      "Mana: " + str(self.creature.mana) + "/" + str(self.creature.get_max_mana()),
      "Physical Armor: " + str(self.creature.p_armor) + "/" + str(self.creature.get_p_armor_cap()),
      "Magical Armor: " + str(self.creature.m_armor) + "/" + str(self.creature.get_m_armor_cap()),
      "Action Points: " + str(self.creature.ap) + "/" + str(self.creature.max_ap),
      "Initiative: " + str(self.creature.get_initiative()) + "      Speed: " + str(self.creature.get_speed()),
      "",
      "Basic Attack:",
      "   " + str(self.creature.get_attack_min()) + "-" + str(self.creature.get_attack_max()) + " damage",
      "   Cost: " + str(self.creature.get_attack_cost()) + " AP",
      "Attributes"
    ]
    for attribute in ATTRIBUTE_LIST.keys():
      text.append("   " + attribute + ": " + str(self.creature.get_attribute(attribute)))
    text.append("Skills:")
    for skill in SKILL_LIST.keys():
      text.append("   " + skill + ": " + str(self.creature.get_skill(skill)))

    x = 12
    y = 28
    line_height = 24
    for line in text:
      if line == "":
        y += int(line_height / 2)
      else:
        screen.write(line, (x,y), font)
        y += line_height

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
    return self
