## Prototype:
A simple prototype to learn the basics of an isometric viewpoint for a dungeon crawling game

`python main.py` to run with the default dungeon generation algorithm
`-h` for options, and `[h]` in game to view the controls

### Dependencies:
The only external library in use is Pygame. https://www.pygame.org/wiki/GettingStarted

`python3 -m pip install -U pygame --user`

### Screenshots (as of 2022-01-16)
Combat!
![combat](https://i.imgur.com/pD63dQ8.png)

Map Screen to fast travel and rest
![map](https://i.imgur.com/F3QT76U.png)

Basic Character Screen
![inventory](https://i.imgur.com/xqLpyJw.png)

### End Goal:
The basic combat and exploration model is complete. Eventually you will be able to select up to 4 of several different characters to form a party, and select from a handful of different dungeon themes to explore. The goal of the game will to delve through up to 3 dungeon levels of increasing difficulty to retrieve an object of power in the furthest room from the start.
As the base is a turn based party RPG, there will be many different types of enemies and items. Equipped items change the character sprites used to easily identify which creature is using what. Skills and abilities will be unique to your starting characters, but can also be learned from skill tomes scattered around the dungeon.

Combat will be close to deterministic to encourage tactical play. Creatures will have an amount of physical and magical armor that absorbs damage of those types and can be replenished on rest.
