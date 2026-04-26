"""
Network and socket handling functions for TCG Game Client

Imports Required:
- socket (Python standard library)
- ui_functions: deckSelectionMenu, selectCardMenu
- deck_functions: createFireDeck, createWaterDeck, shuffleDeck
- hand_functions: createHand, drawCard
- game_functions: attackPhase
"""

import socket
import threading
from .ui_functions import deckSelectionMenu, selectCardMenu
from .deck_functions import createFireDeck, createWaterDeck, shuffleDeck
from .hand_functions import createHand, drawCard
from .game_functions import attackPhase


def initialize_player_cards(deck_choice, state):
    deck = []
    if deck_choice == 'fire':
        createFireDeck(deck)
    elif deck_choice == 'water':
        createWaterDeck(deck)

    shuffleDeck(deck)
    state['deck_cards'] = deck
    state['hand'] = createHand(deck)
    state['field'] = []
    state['has_seen_turn_start'] = False


def recv_thread(sock, state):
    """Receive thread that listens for server messages and updates game state.
    
    Args:
        sock (socket): The server socket connection
        state (dict): Game state dictionary to update based on server messages
    """
    buf = b""
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print("Disconnected from server")
                # clear room state
                state['room'] = None
                return
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                try:
                    line = line.decode().strip()
                except Exception:
                    line = ''
                if not line:
                    continue
                
                # Handle different message types
                if line.startswith("SERVER:FORWARD CARD"):
                    # Format: SERVER:FORWARD CARD <idx> <name> <type> <attack> <health> <cost>
                    parts = line.split(" ", 5)
                    if len(parts) >= 6:
                        card_name = parts[3]
                        card_type = parts[5]
                        # print ("parts: %s" %line.split(" ", 5))
                        print(f"\n>>> OPPONENT PLAYED: {card_name} ({card_type}) <<<\n")
                    else:
                        print(f"SERVER> {line}")
                elif line.startswith("SERVER:FORWARD"):
                    # Other forwarded messages
                    msg = line.replace("SERVER:FORWARD ", "")
                    print(f"[OPPONENT] {msg}")
                else:
                    print(f"SERVER> {line}")
                
                # Update client state based on server messages
                if line.startswith("SERVER:OK Joined room"):
                    # format: SERVER:OK Joined room <room_id>
                    parts = line.split()
                    if parts:
                        state['room'] = parts[-1]
                        print("\n*** You have joined the room! ***")
                        # Show menu and flag main loop to handle input
                        deckSelectionMenu()
                        state['pending_deck_selection'] = True
                elif line.startswith("SERVER:INFO Left room") or line.startswith("SERVER:INFO Opponent left"):
                    state['room'] = None
                    state['deck'] = None
                    state['field'] = []
                    state['hand'] = []
                    state['deck_cards'] = []
                    state['active_turn'] = False
                elif line.startswith("SERVER:READY"):
                    print("\n*** Game started! Opponent is ready. ***\n")
                elif line.startswith("SERVER:STATUS Round"):
                    parts = line.split()
                    if len(parts) >= 5:
                        try:
                            state['round'] = int(parts[2])
                            state['mana_total'] = int(parts[4])
                            if not state.get('active_turn'):
                                state['mana_available'] = 0
                        except ValueError:
                            pass
                elif line.startswith("SERVER:TURN "):
                    turn_name = line.replace("SERVER:TURN ", "", 1).strip()
                    is_my_turn = turn_name == state.get('player_name')
                    state['active_turn'] = is_my_turn
                    if is_my_turn:
                        state['mana_available'] = state.get('mana_total', 0)
                        deck_cards = state.get('deck_cards', [])
                        hand = state.get('hand', [])
                        if state.get('has_seen_turn_start') and deck_cards:
                            drawCard(deck_cards, hand)
                        state['has_seen_turn_start'] = True
                    else:
                        state['mana_available'] = 0
                elif line.startswith("SERVER:GAMEOVER"):
                    state['active_turn'] = False
                    state['mana_available'] = 0
                elif line.startswith("SERVER:INFO Server shutting down"):
                    print("Server is shutting down — exiting client.")
                    state['running'] = False
                    try:
                        sock.shutdown(socket.SHUT_RDWR)
                    except Exception:
                        pass
                    return
    except Exception as e:
        print("Receive error:", e)


def main():
    """Main client function that handles user input and server communication."""
    ROOMS = ['room1', 'room2', 'room3']

    host = input("Server host [localhost]: ").strip() or 'localhost'
    port_s = input("Server port [9000]: ").strip() or '9000'
    try:
        port = int(port_s)
    except Exception:
        port = 9000

    state = {
        'room': None,
        'running': True,
        'deck': None,
        'player_name': None,
        'player_health': 20,
        'opponent_health': 20,
        'pending_deck_selection': False,
        'deck_cards': [],
        'hand': [],
        'field': [],
        'round': 0,
        'mana_total': 0,
        'mana_available': 0,
        'active_turn': False,
        'has_seen_turn_start': False,
    }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
        except Exception as e:
            print("Could not connect:", e)
            return
        t = threading.Thread(target=recv_thread, args=(s, state), daemon=True)
        t.start()

        print("Connected.")
        print("Available rooms:")
        for r in ROOMS:
            print(f" - {r}")
        print("Commands: rooms | join <room_id> <name> | selectcard | attack | play <payload> | end | leave | game | quit | exit")
        try:
            while state['running']:
                try:
                    cmd = input('> ').strip()
                except EOFError:
                    cmd = 'quit'
                if not cmd:
                    continue
                # Handle pending deck selection before any other command
                if state['pending_deck_selection']:
                    if cmd == '1':
                        deck_choice = 'fire'
                    elif cmd == '2':
                        deck_choice = 'water'
                    else:
                        print("Invalid selection. Please type 1 (Fire) or 2 (Water).")
                        continue
                    state['deck'] = deck_choice
                    state['pending_deck_selection'] = False
                    print(f"\n✓ You selected {deck_choice.upper()} Deck!")
                    print(f"Your deck has been set to: {deck_choice.upper()}")
                    initialize_player_cards(deck_choice, state)
                    try:
                        s.sendall((f"DECK {deck_choice}\n").encode())
                    except Exception as e:
                        print(f"Error sending deck choice: {e}")
                    continue
                parts = cmd.split(' ', 2)
                action = parts[0].lower()
                if action in ('rooms', 'list'):
                    print("Available rooms:")
                    for r in ROOMS:
                        print(f" - {r}")
                # elif action == 'game':
                #     # Start a local game using turnCounter
                #     from .game_functions import turnCounter
                #     print("Starting a local game...")
                #     fireDeck = []
                #     waterDeck = []
                #     try:
                #         turnCounter(fireDeck, waterDeck)
                #     except KeyboardInterrupt:
                #         print("")
                #         print("Game interrupted by user.")
                #         print("")
                elif action == 'join' and len(parts) >= 3:
                    rid = parts[1]
                    name = parts[2]
                    if rid not in ROOMS:
                        print(f"Room {rid} is not available. Use 'rooms' to list options.")
                        continue
                    state['player_name'] = name
                    s.sendall((f"JOIN {rid}|{name}\n").encode())
                elif action == 'selectcard' and state['room'] and state['deck']:
                    if not state.get('active_turn'):
                        print("You cannot play a card during the other player's turn.")
                        continue
                    if not state.get('hand'):
                        print("No cards available in hand.")
                        continue
                    selectCardMenu(state['hand'], s, state)
                elif action == 'attack' and state['room']:
                    if not state.get('active_turn'):
                        print("You cannot attack during the other player's turn.")
                        continue
                    print(f"\nYour Health: {state['player_health']} | Opponent Health: {state['opponent_health']}")
                    attackPhase(state.get('field', []), state['opponent_health'], s, state)
                elif action == 'selectcard' and state['room'] and not state['deck']:
                    print("Error: You must select a deck first. Please rejoin the room.")
                elif action == 'play' and len(parts) >= 2:
                    payload = parts[1] if len(parts) == 2 else parts[1] + ' ' + parts[2]
                    s.sendall((f"PLAY {payload}\n").encode())
                elif action == 'end':
                    s.sendall(("ENDTURN\n").encode())
                elif action == 'leave':
                    s.sendall(("LEAVE\n").encode())
                    state['room'] = None
                elif action in ('quit', 'exit'):
                    # allow clean quit
                    try:
                        s.sendall(("QUIT\n").encode())
                    except Exception:
                        pass
                    break
                else:
                    print("Unknown command. Examples: join room1 Alice | selectcard | attack | play CARD 1 | end | leave | quit")
        except KeyboardInterrupt:
            print("\nKeyboard interrupt detected. Closing client...")
            state['running'] = False
            try:
                s.sendall(("QUIT\n").encode())
            except Exception:
                pass
            try:
                s.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
