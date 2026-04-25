# Client.py Refactoring Summary

## Overview
The `client.py` file has been refactored to modularize all functions into a new `functions/` directory. The original client.py is now a lightweight entry point that imports and calls the main function from the network module.

## Directory Structure

```bash
functions/
├── __init__.py                 # Package initialization
├── deck_functions.py           # Deck management functions
├── hand_functions.py           # Hand management functions
├── ui_functions.py             # User interface and menu functions
├── game_functions.py           # Game logic functions
└── network_functions.py        # Network and socket handling functions
```

## Module Breakdown

### 1. **functions/deck_functions.py**

Contains all deck creation and management functions.

**Functions:**

- `createFireDeck(fireDeck)` - Creates fire deck with 3 copies of each fire card
- `createWaterDeck(waterDeck)` - Creates water deck with 3 copies of each water card
- `shuffleDeck(deck)` - Shuffles a deck by randomly rearranging cards

**Imports Required:**

```python
import random
from deckFire.fireCards import Flamestrike, Imp, Drake, Wildfire, Fireball, Cerberus, SpiiritOfFire
from deckWater.waterCards import Crash, Monsoon, WaterSpirite, WaterSerpent, WaterSpout, Mino, TidalWave
```

---

### 2. **functions/hand_functions.py**

Contains all hand and card play management functions.

**Functions:**

- `createHand(deck)` - Creates starting hand of 3 cards from deck
- `drawCard(deck, hand)` - Draws a single card from deck into hand
- `cardToPlay(hand, lifeCount, field)` - Handles card selection and playing

**Imports Required:**

```python
# Local imports (relative)
from .ui_functions import handMenu
from .game_functions import playCardWithMutation
```

---

### 3. **functions/ui_functions.py**

Contains all user interface and menu-related functions.

**Functions:**

- `clear()` - Clears the console screen
- `handMenu(hand, field)` - Shows numbered menu for card selection
- `deckSelectionMenu()` - Displays deck selection menu (Fire/Water)
- `selectCardMenu(hand, sock, state)` - Displays hand and sends selected card to server

**Imports Required:**

```python
import os
```

---

### 4. **functions/game_functions.py**

Contains core game logic functions.

**Functions:**

- `playCardWithMutation(card, lifeCount)` - Plays a card and updates life count
- `attackPhase(field, opponentLife, sock=None, state=None)` - Handles attack phase logic
- `turnCounter(fireDeck, waterDeck)` - Runs complete local game turn loop

**Imports Required:**

```python
from deckFire.fireCards import Drake, Imp
from deckWater.waterCards import WaterSerpent, WaterSpout
from .deck_functions import createFireDeck, createWaterDeck, shuffleDeck
from .hand_functions import createHand, drawCard, cardToPlay
```

---

### 5. **functions/network_functions.py**

Contains network communication and main client logic.

**Functions:**

- `recv_thread(sock, state)` - Receives and processes server messages
- `main()` - Main client function handling user input and server communication

**Imports Required:**
```python
import socket
import threading
from .ui_functions import deckSelectionMenu, selectCardMenu
from .deck_functions import createFireDeck, createWaterDeck, shuffleDeck
from .hand_functions import createHand
from .game_functions import attackPhase, turnCounter
from deckFire.fireCards import Drake, Imp
from deckWater.waterCards import WaterSerpent, WaterSpout
```

---

### 6. **client.py (Refactored)**

The new client.py is now a simple entry point.

**Content:**

```python
from functions.network_functions import main

if __name__ == '__main__':
    main()
```

**Imports Required:**

```python
from functions.network_functions import main
```

---

## Dependency Graph

```bash
client.py
    └── functions/network_functions.py
        ├── functions/ui_functions.py
        ├── functions/deck_functions.py
        ├── functions/hand_functions.py
        ├── functions/game_functions.py
        ├── deckFire.fireCards
        └── deckWater.waterCards

functions/game_functions.py
    ├── functions/deck_functions.py
    ├── functions/hand_functions.py
    ├── deckFire.fireCards
    └── deckWater.waterCards

functions/hand_functions.py
    ├── functions/ui_functions.py
    ├── functions/game_functions.py
```

---

## Usage

To run the refactored client:

```bash
python client.py
```

The client will work exactly as before, but all functions are now organized in modular files for better maintainability and code organization.

---

## Benefits of This Refactoring

1. **Separation of Concerns** - Each module has a single responsibility
2. **Maintainability** - Easier to find and update specific functions
3. **Reusability** - Functions can be imported independently in other projects
4. **Scalability** - Adding new features is easier with organized code structure
5. **Testing** - Individual modules can be tested in isolation
6. **Readability** - Clear directory structure shows code organization at a glance
