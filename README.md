<!-- markdownlint-disable MD031 -->
<!-- markdownlint-disable MD032 -->
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD041 -->
<div id="top-of-doc"></div>

# Readme File |  | January-15-2026 |

[Github](https://github.com/popados) | [Jump to End](#end-of-doc)

***

## Specifications

### File Structure

```bash
tcg_game/
├── client.py                 # Client application entry point
├── server.py                 # Server application entry point
├── main.py                   # Main application launcher
├── menuEx.py                 # Menu interface
├── cursesMenuEx.py           # Curses-based menu interface
├── fireCards.py              # Fire cards module
├── waterCards.py             # Water cards module
├── README.md                 # This file
├── functions/                # Refactored client function modules
│   ├── __init__.py           # Functions package init
│   ├── deck_functions.py     # Deck creation and shuffling
│   ├── hand_functions.py     # Hand and draw helpers
│   ├── ui_functions.py       # Menus and input helpers
│   ├── game_functions.py     # Game phase logic
│   └── network_functions.py  # Client networking flow
├── _img/                     # Image assets
├── _logic/
│   ├── card_logic.py        # Card game logic
│   └── game_logic.py        # General game logic
├── deckFire/
│   ├── fireCards.py         # Fire deck definition
│   └── cards/
│       ├── allCards.py      # All fire cards registry
│       ├── drake.py         # Drake card
│       ├── fireball.py      # Fireball card
│       └── imp.py           # Imp card
├── deckWater/
│   ├── waterCards.py        # Water deck definition
│   └── cards/               # Water cards definitions
├── field/
│   ├── field.py             # Field game area
│   └── graveyard.py         # Graveyard logic
├── player/
│   ├── card.py              # Card class definition
│   ├── deck.py              # Deck management
│   └── hand.py              # Player hand management
├── server_logs/             # Server log files
└── server-client-test/      # Testing directory
    ├── client.py
    └── server.py
```

### Commands

#### Starting the Server

```bash
python server.py
```
Starts the TCG game server on localhost:12345. The server manages game rooms and player connections.

#### Starting the Client

```bash
python client.py
```
Launches the client application to connect to the running server.

#### Running Main Application

```bash
python main.py
```
Runs the main application launcher.

***

## DayNum | x/x/20xx - Today

***

### Day 001 | 01/16/2026 - Thursday

Starting my trading card game. This is a game that is based off Magic: The Gathering and includes Hearthstone elements.

Such elements are:
- Mana
- Turns gain mana
- 7 cards each 3 times in a deck
- commander card
- abilities with the commander a -2/0 mana cost

TODO:
- Mana
- Player hand
- Graveyard
- Field
- Abilities
- Cards
- Deck

![Card Game Flow Chart](../tcg_game/_img/card-flowchart.png)

This flowchart shows the attributes and where they are placed within objects. I need to find the design pattern for creating a bucket. I have singleton objects for each card(which could possibily turned into a factory pattern). This allows each card to have an ability such as a shield or extra damage.

![Card Field](../tcg_game/_img/field-markup.png)

***

### Day 002 | 01/26/2026 - Monday

Got some new cards coded in. Added the deck.

Need random number for a shuffle or hand function.

Shuffle function important
draw hand
play card
field

***

### Day 003 | 02/12/2026 - Thursday

In order the steps

- Shuffle
- First Hand
- Draw
- Main Phase(play spell or creature cards)
- Attack Phase(attack with cards on field)
- End Phase

maybe set up client-server interactions

clean up the selection process for cards

remove/add mana

card abilities

```Markdown
I'll add a small plan (todo list) then create two files: server.py and client.py implementing a simple TCP room server (max 2 players) and a command-line client.

Created server.py and client.py files
Progress update: created a simple TCP room server and a CLI client; next I can add README instructions and polish the protocol.

What I added

File: server.py — multithreaded TCP server hosting rooms (max 2 clients). Commands: JOIN room|name, PLAY payload, LEAVE, QUIT. Forwards PLAY to the other player in the room and sends room/ready notifications.
File: client.py — interactive CLI client. Use join <room_id> <name>, play <payload>, leave, quit.
How to try it

Start the server:

python server.py
In two different terminals run the client:

python client.py# then at the prompt, e.g.:join room1 Alice# in the other client:join room1 Bob# when both ready, send:play CARD 1
Next steps I can do (pick any):

Finish TODO item: add README usage notes and examples.
Integrate the client with your existing game code so the client sends actual game actions (draw, play card) and server relays game state.
Use WebSockets or higher-level networking for reliability and easier message handling.
Which should I do next
```

***

### Day 004 | 02/14/2026 - Saturday

```Markdown
I've implemented a simple server-client system in Python using sockets. The server manages rooms that can hold up to 2 clients, and clients can send commands to join or leave rooms.

Key Features:
Server (server.py): Listens on localhost:12345, handles multiple clients with threading, and manages rooms as dictionaries.
Client (client.py): Connects to the server, allows sending commands via input, and receives messages in a separate thread.
Commands:
join <room_id>: Join a room (creates if doesn't exist).
leave: Leave the current room.
list: List available rooms.
Room Logic: Rooms hold up to 2 clients. When the second client joins, all clients in the room receive a "Room <id> is full" message.
Main (main.py): Runs the server.
To test:

Run python main.py to start the server.
Run python client.py in separate terminals to connect clients and send commands.
The code is ready and should work as described. If you need modifications or additional features, let me know!
```

server.py

client.py

main.py

clean up the files and folders

***

### Day 005 | 04/25/2026 - Saturday

Restrctured the functions so there are specific files for the types of functions.

The client is now a clean `main()` loop.

So far I need to set the turns correctly so it displays who won the game next after the life total goes to 0 or less.

Need to add main gameplay loop that goes through each phase(draw, main, attack) are the three main phases after attack phase the turn is passed to the next player.

Main phase is done as a choice menu with `commander-ability` and `hand` as options as well as the final step which is `attack`. Other commands are `field` which displays what monsters are in play.

Each hand has two types of cards `creature` and `spell`. They both cost mana points, which is gained each turn as the game progresses to a max of 10.


```markdown
What changed:

Added server-side game state per room:
- game_active
- current_turn
- commander_health for both players
- fields for both players
- round and mana
Added server functions to run turn-based flow:
- room/player helpers
- status broadcasting for both commanders + both fields
- game-over check (<= 0 health ends game)
- game start when both players choose decks
Updated command handling in server.py:
- DECK <fire|water> now properly handled as its own command
- PLAY only allowed on active player’s turn; creature plays update server field state
- ATTACK <damage> applies damage to opponent commander on server
- ENDTURN passes turn on server (and advances round/mana appropriately)
Added server status outputs to clients:
- SERVER:STATUS ... shows commander health, fields, round/mana, and current turn
- SERVER:TURN ... shows whose turn it is
- SERVER:GAMEOVER ... sent when either commander reaches 0 or less
- Updated protocol comments in server.py to match new behavior.
```




***

## End of Document

***

[Jump to Top](#top-of-doc)

<div id="end-of-doc"></div>

<details>
<summary>
Notes :
</summary>
</details>

