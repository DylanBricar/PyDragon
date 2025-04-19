# PyDragon

## 🎮 Game Concept

**PyDragon** is a 2D adventure game inspired by the *Dragon Ball* universe, developed in Python using the PyGame
library. The game lets you explore a 2D world filled with characters you can interact with, hidden items to find, and
missions to complete.

---

## 🖼️ Screenshots

Here are some in-game screenshots showing different stages of the game:

![Start Screen](https://github.com/DylanBricar/PyDragon/blob/master/ressources/images/screens/start.png "Start Screen")
![Gameplay](https://github.com/DylanBricar/PyDragon/blob/master/ressources/images/screens/game.png "Gameplay")
![Main Menu](https://github.com/DylanBricar/PyDragon/blob/master/ressources/images/screens/menu.png "Main Menu")

---

## ✨ Features

- 2D map system
- Interactions with NPCs
- Startup menu
- Character animations
- Simple storyline
- Background music during gameplay
- Item discovery system
- **NEW 2025**: Escape menu to switch characters
- **NEW 2025**: Hold SHIFT to run
- **NEW 2025**: Movement support for both ZQSD and arrow keys
- **NEW 2025**: Fixed compatibility issues and improved virtual environment setup

---

## ⚠️ Development Challenges

- Limited initial knowledge of PyGame
- Collision detection on the map
- Saving character progression
- Character animation system
- Transition between maps
- Maintaining PyGame code effectively
- Creating character interaction logic
- Interface placement and management

---

## ✅ Achievements

- Collected sprite animations
- Implemented background music
- Designed a custom 2D map using a map editor

---

## 🧪 Technology Used

- Python
- PyGame

---

## 🚀 Getting Started

1. Define a story and objectives
2. Learn PyGame and how to import maps from Tiled Map Editor
3. Design your maps:

- Main world
- Kame House

4. Add collisions
5. Import maps and characters
6. Implement character dialogue
7. Add music
8. Create and integrate the storyline
9. Add item discovery mechanics
10. Build the start menu

---

## 📅 Development Timeline

> A detailed log of project milestones:

- **11/10/2018**: Project goal defined
- **18/10/2018**: TMX module tested, initial collision experiments, PyGame research
- **25/10/2018**: PyGame exercises and basic tutorials completed
- **31/10/2018**: First map created with basic collisions and player event handling
- **08/11/2018**: Functionality verified and adapted for Windows
- **15/11/2018**: Socket research
- **18/11/2018**: Map redesign, added comments, collisions v0.1
- **22/11/2018**: CPU processing behavior and OS differences researched
- **27/11/2018**: Collision system overhaul, TMX library customized
- **28/11/2018**: Major code refactor (OOP), collision handling, FPS control
- **09/01/2019**: Fully functional collisions, optimized and cleaned codebase
- **16/01/2019**: Improved Windows-specific import logic
- **23/01/2019**: FPS management issues on Windows resolved
- **30/01/2019**: Research on map transitions
- **06/02/2019**: Sought coding guidance from Python developers
- **13/02/2019**: Diagram planning for entity transitions
- **20/02/2019**: Redesign of processing systems (on inaccessible shared drive)
- **27/02/2019**: Finished work on the new systems (still inaccessible)
- **03/03/2019**: Animated walking sprites, house interior with collisions
- **06/03/2019**: Fixed sprite import issues on Windows
- **13/03/2019**: Multimap management strategy planning
- **20/03/2019**: Fixed global path issues in second map
- **27/03/2019**: Requested help for implementing map transfers
- **24/04/2019**: Follow-up request for support
- **08/05/2019**: Game revamp, new development direction
- **15/05/2019**: UI system added, code split into classes, new collisions
- **16/05/2019**: Interface loop, coordinate saving, character sprite adjustments
- **17/05/2019**: Music and dialogue system implemented, first mission added
- **20/05/2019**: Code optimization, character interaction, map transparency
- **21/05/2019**: New map + mission 1 house, interactions, inventory system
- **22/05/2019**: Start menu, collision tweaks, comments, Windows checks, PEP8 compliance
- **18/04/2025**: New features: character switch menu, sprinting, ZQSD/arrow keys, environment fixes

---

## 🏫 Background

This project was developed during the final year of secondary school as part of the computer science course taught by
Mr. Bertocchi at Collège Roi Baudouin.
Website: [http://explore-photo.com/](http://explore-photo.com/)

---

## 🛠️ Installation

### Requirements

- Python 3.8 or later
- pip (Python package installer)

### Virtual Environment Setup

1. **Clone the repository**

 ```bash
 git clone git@github.com:DylanBricar/PyDragon.git
 cd PyDragon
 ```

2. **Create a virtual environment**

 ```bash
 python -m venv venv
 ```

3. **Activate the virtual environment**

- On **Windows**:

 ```bash
 venv\Scripts\activate
 ```

- On **Windows with Git Bash**:

 ```bash
 source venv/Scripts/activate
 ```

- On **macOS/Linux**:

 ```bash
 source venv/bin/activate
 ```

4. **Install the dependencies**

 ```bash
 pip install -r requirements.txt
 ```

5. **Run the game**

 ```bash
 python main.py
 ```