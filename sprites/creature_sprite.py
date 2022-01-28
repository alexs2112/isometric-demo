import pygame

# A simple way to take a creature and their equipment, stack all the images and return a
# new image to be used as a sprite
def get_sprite(creature):
  e = creature.equipment
  res = pygame.Surface((32, 32), pygame.SRCALPHA)

  # Cloaks go first
  i = e.slot("Cloak")
  if i:
    res.blit(i.sprite, (0,0))
  
  # Then the body base
  res.blit(creature.base_sprite, (0,0))

  # Then head, feet, hands, chest, main
  i = e.slot("Head")
  if i:
    res.blit(i.sprite, (0,0))
  i = e.slot("Feet")
  if i:
    res.blit(i.sprite, (0,16))
  i = e.slot("Hands")
  if i:
    res.blit(i.sprite, (0,10))
  i = e.slot("Chest")
  if i:
    res.blit(i.sprite, (0,0))
  i = e.slot("Main")
  if i:
    res.blit(i.sprite, (0,0))
  
  return res
  