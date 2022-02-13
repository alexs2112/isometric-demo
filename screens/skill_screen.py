import pygame
from screens.screen import Screen, split_text_to_list
from screens.subscreen import Subscreen
from creatures.creature import Creature
from pygame.locals import (
  MOUSEBUTTONDOWN,
  KEYDOWN,
  K_ESCAPE
)

class SkillScreen(Subscreen):
  def __init__(self, creature: Creature, selected_skill=None):
    self.creature = creature
    self.skills = self.creature.skill_list()
    self.screen_x, self.screen_y = 190, 100
    self.background = pygame.image.load("assets/screens/skills_block.png")

    self.selected_skill = selected_skill
    self.mouse_skill = None   # If we are dragging a skill around to the action bar

  def is_overlay(self):
    return True
  
  def draw(self, screen: Screen):
    screen.blit(self.background, (self.screen_x, self.screen_y))
    screen.write(self.creature.name + "'s Skills", (self.screen_x + 12, self.screen_y + 10), screen.tileset.get_font(28))
    self.draw_skill_icons(screen)
    
    if self.selected_skill:
      skill = self.selected_skill
    else:
      skill = self.get_skill_by_mouse()
    self.draw_skill_description(screen, skill)

    if self.mouse_skill:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      screen.blit(self.mouse_skill.icon, (mouse_x - 24, mouse_y - 24))

  # Eventually sort skills by main type with little headers to specify
  def draw_skill_icons(self, screen: Screen):
    sx, sy = self.screen_x + 6, self.screen_y + 54
    for i in range(len(self.skills)):
      skill = self.skills[i]
      meet_req = self.creature.get_stat(skill.get_type()) >= skill.get_level()
      if skill == self.selected_skill:
        if meet_req:
          box = screen.tileset.get_ui("skill_box_yellow")
        else:
          box = screen.tileset.get_ui("skill_box_orange")
      else:
        if self.creature.skill_prepared(skill):
          if meet_req:
            box = screen.tileset.get_ui("skill_box_blue")
          else:
            box = screen.tileset.get_ui("skill_box_purple")
        else:
          if meet_req:
            box = screen.tileset.get_ui("skill_box_grey")
          else:
            box = screen.tileset.get_ui("skill_box_red")
      
      x = sx + (i % 7) * 60
      y = sy + (i // 7) * 60
      screen.blit(box, (x, y))
      screen.blit(skill.icon, (x + 4, y + 4))

  def get_skill_by_mouse(self):
    sx,sy = pygame.mouse.get_pos()
    x = sx - (self.screen_x + 6)
    y = sy - (self.screen_y + 54)
    
    index = (x // 60) + 7 * (y // 60)
    if index >= 0 and index < len(self.skills):
      return self.skills[index]
    return None

  def draw_skill_description(self, screen: Screen, skill):
    if not skill:
      return
    x = self.screen_x + 436
    y = self.screen_y + 56

    t = skill.name
    if self.creature.skill_prepared(skill):
      t += " (Prepared)"
    screen.write(t, (x, y), screen.tileset.get_font(28))
    y += 32

    lines = split_text_to_list(skill.description, 420, screen.tileset.get_font(22))
    for l in lines:
      screen.write(l, (x,y), screen.tileset.get_font(22))
      y += 24

    y += 18
    l = "AP: " + str(skill.ap_cost)
    if skill.mana_cost > 0:
      l += "    Mana: " + str(skill.mana_cost)
    if skill.cooldown > 0:
      l += "    Cooldown: " + str(skill.cooldown)
    screen.write_centered(l, (x + 210, y), screen.tileset.get_font(22))
    y += 32
    
    l = "Range: "
    if skill.get_range() == 0:
      l += "Self"
    else:
      l += str(skill.get_range())
    screen.write_centered("Range: " + str(skill.get_range()), (x+210, y), screen.tileset.get_font(22))
    y += 32

    screen.write_centered("Stat Requirements:", (x+210, y), screen.tileset.get_font())
    y += 26
    if skill.get_level() == 0:
      l = "None"
    else:
      l = skill.get_type() + ": " + skill.get_level()
    screen.write_centered(l, (x+210, y), screen.tileset.get_font(22))

    screen.write_centered("(Right click to assign this skill to your action bar)", (x + 210, self.screen_y + 570), screen.tileset.get_font(16))

  def in_action_bar(self, mouse_x, mouse_y):
    return mouse_x > self.creature.action_bar.screen_x and mouse_y > self.creature.action_bar.screen_y
  
  def pop_action_bar_skill(self, mouse_x):
    index = (mouse_x - self.creature.action_bar.screen_x) // 52
    element = self.creature.action_bar.element_at_index(index)
    if element and element.is_skill():
      self.creature.action_bar.pop_element(index)
      self.selected_skill = element
      self.mouse_skill = element

  def respond_to_events(self, events):
    super().respond_to_events(events)
    for event in events:
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          return None
      elif event.type == MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        left, _, right = pygame.mouse.get_pressed()

        if self.in_action_bar(x,y):
          if self.mouse_skill:
            self.creature.action_bar.set_button(self.mouse_skill, (x - self.creature.action_bar.screen_x) // 52)
            self.mouse_skill = None
          else:
            self.pop_action_bar_skill(x)

        elif left:
          self.mouse_skill = None
          self.selected_skill = self.get_skill_by_mouse()

        elif right:
          s = self.get_skill_by_mouse()
          if s:
            self.selected_skill = s
            self.mouse_skill = s
          elif self.selected_skill:
            self.selected_skill = None
          else:
            return None
    return self
