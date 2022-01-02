import random, sys
import world.world_builder as world_builder
from creatures.creature_factory import CreatureFactory

def create_world(args):
  world_width = 30
  world_height = 40
  if "--small" in args:
    world_width = 25
    world_height = 25

  if "--no_paths" in args:
    world = world_builder.place_rooms(6, world_width, world_height)
  elif "--maze" in args:
    world = world_builder.generate_maze(world_width, world_height)
  elif "--no_walls" in args:
    world = world_builder.only_floors(world_width, world_height)
  else: # Default to --dungeon
    world = world_builder.generate_dungeon(world_width, world_height, 15)

  if '-v' in args:
    world.print_world()
  
  return world

def create_players(world: world_builder.World, cf: CreatureFactory):
  if world.start_room:
    room = world.start_room
  elif world.rooms:
    room = random.choice(world.rooms)
  else:
    room = None

  if '--solo' in sys.argv:
    player_num = 1
  else:
    player_num = 4
  for i in range(player_num):
    if room:
      x, y = world.get_random_floor_in_room(room)
    else:
      x, y = world.get_floor_coordinate()
    if i == 0:
      cf.new_edward(x,y)
    elif i == 1:
      cf.new_goobert(x,y)
    elif i == 2:
      cf.new_wizard(x,y)
    elif i == 3:
      cf.new_harold(x,y)

def create_creatures(world: world_builder.World, cf: CreatureFactory):
  create_players(world, cf)
  for room in world.rooms:
    if room == world.start_room:
      continue

    for _ in range(3):
      x, y = world.get_random_floor_in_room(room)
      if random.random() < 0.3:
        c = cf.new_mushroom(x,y)
      else:
        c = cf.new_skeleton(x,y)
      c.set_home_room(room)