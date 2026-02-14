"""
Simple command-line client for the TCG room server.
- Run: python client.py

Usage flow:
- Enter server host/port (defaults provided)
- JOIN <room_id>|<player_name>
- When in a room, type `play <payload>` to send a PLAY command (payload can be e.g. PLAY CARD index)
- Type `leave` to leave, `quit` to disconnect

This client prints server messages and forwards simple `play` commands typed by the user.
"""

import socket
import threading
import sys
import os
import random
from deckFire.fireCards import Flamestrike, Imp
from deckFire.fireCards import Drake, Wildfire
from deckFire.fireCards import Fireball, Cerberus, SpiiritOfFire
from deckWater.waterCards import Crash, Monsoon, WaterSpirite, WaterSerpent
from deckWater.waterCards import WaterSpout, Mino, TidalWave
from player.card import Card


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def playCardWithMutation(card, lifeCount):
    """Play a card and mutate the lifeCount variable"""
    lifeCount = card.playCard(lifeCount)
    return lifeCount


def createFireDeck(fireDeck):
    for i in range(3):
        fireDeck.append(Imp())
        fireDeck.append(Drake())
        fireDeck.append(Fireball())
        fireDeck.append(Flamestrike())
        fireDeck.append(Wildfire())
        fireDeck.append(Cerberus())
        fireDeck.append(SpiiritOfFire())
    return fireDeck


def createWaterDeck(waterDeck):
    for i in range(3):
        waterDeck.append(WaterSerpent())
        waterDeck.append(WaterSpout())
        waterDeck.append(Monsoon())
        waterDeck.append(WaterSpirite())
        waterDeck.append(Crash())
        waterDeck.append(Mino())
        waterDeck.append(TidalWave())
    return waterDeck


def shuffleDeck(deck):
    for i in range(len(deck)):
        count = random.randint(0, len(deck) - 1)
        deck.append(deck.pop(count))
    return deck


def createHand(deck):
    hand = []
    for i in range(3):
        hand.append(deck.pop(i))
        print(f"drew card: {hand[i].cardName}")
    return hand


def drawCard(deck, hand):
    hand.append(deck.pop(0))
    print(f"drew card: {hand[-1].cardName}")
    return hand


def handMenu(hand, field):
    """Show a numbered menu for the given hand and return the selected card or None for End Turn.
    
    0 -> End Turn
    1..N -> select corresponding card in hand
    """
    while True:
        print("Select a card to play (type the number). 0 = End Turn\n")
        for i, card in enumerate(hand, start=1):
            cost = getattr(card, "cost", "?")
            print(f"{i}: {card.cardName} (Mana: {cost})")
        print("9: Show Field")
        print("0: End Turn")

        choice = input("Choice: ").strip()
        if not choice:
            continue
        if not choice.isdigit():
            print("Please enter a number.")
            input("Press Enter to continue...")
            continue
        idx = int(choice)
        if idx == 0:
            return None
        if idx == 9:
            print("field: %s" % field)
            continue
        if 1 <= idx <= len(hand):
            return hand[idx - 1]
        print("Invalid selection.")
        input("Press Enter to continue...")


def attackPhase(field, opponentLife, sock=None, state=None):
    if not field:
        print("No creatures to attack with.")
        return opponentLife
    print("\n:::Attack phase displaying field:::")
    if state and 'opponent_health' in state:
        print(f"Opponent Health: {state['opponent_health']}")
    print("Select a creature to attack with (type the number). 0 = Skip Attack\n")
    for i, card in enumerate(field, start=1):
        print(f"{i}: {card.cardName} (Attack: {card.attack})")
    choice = input("Choice: ").strip()
    if not choice or not choice.isdigit():
        print("Skipping attack.")
        return opponentLife
    idx = int(choice)
    if idx == 0:
        print("Skipping attack.")
        return opponentLife
    if 1 <= idx <= len(field):
        attacker = field[idx - 1]
        damage = attacker.attack
        opponentLife -= damage
        print(f"\n{attacker.cardName} attacks for {damage} damage!")
        print(f"Opponent health: {opponentLife}")
        
        # Send attack damage to opponent via server
        if sock:
            try:
                sock.sendall((f"ATTACK {damage}\n").encode())
            except Exception as e:
                print(f"Error sending attack: {e}")
        
        # Update opponent health in state
        if state:
            state['opponent_health'] = opponentLife
        
        return opponentLife
    print("Invalid selection.")
    return opponentLife


def cardToPlay(hand, lifeCount, field):
    """Player selects a card to play from their hand"""
    selectedCard = handMenu(hand, field)
    if selectedCard is None:
        return lifeCount  # End Turn
    # Play the selected card
    if selectedCard.cardType == "Creature":
        field.append(selectedCard)
        print(f"card {hand.index(selectedCard) + 1}: {selectedCard.cardName} played")
        hand.remove(selectedCard)
    elif selectedCard.cardType == "Spell":
        print("")
        print(f"spell {hand.index(selectedCard) + 1}: {selectedCard.cardName} played")
        lifeCount = playCardWithMutation(selectedCard, lifeCount)
        hand.remove(selectedCard)
    return lifeCount


def turnCounter(fireDeck, waterDeck):
    createFireDeck(fireDeck)
    createWaterDeck(waterDeck)
    
    shuffleDeck(fireDeck)
    shuffleDeck(waterDeck)
    
    p1LifeCount = 20
    p2LifeCount = 20
    turnCount = 0
    manaCount = 1
    gameStart = True
    fireHand = createHand(fireDeck)
    print("fire hand created")
    print("")
    waterHand = createHand(waterDeck)
    print("water hand created")
    print("")
    fireField = []
    waterField = []
    
    while gameStart == True:
        if p1LifeCount > 0:
            print("--Round %s: %s mana added" %(turnCount + 1, manaCount))
            print("")
            # Fire player's turn
            while True:
                print("**Fire player's turn**")
                print("")
                print("---Life: %s - Turn %s" %(p1LifeCount, turnCount + 1))
                p2LifeCount = cardToPlay(fireHand, p2LifeCount, fireField)
                p2LifeCount = attackPhase(fireField, p2LifeCount)
                break
            drawCard(fireDeck, fireHand)
            print("")
        if p2LifeCount > 0:
        # Water player's turn
            while True:
                print("**Water player's turn**")
                print("")
                print("---Life: %s - Turn %s" %(p2LifeCount, turnCount + 1))
                p1LifeCount = cardToPlay(waterHand, p1LifeCount, waterField)
                p1LifeCount = attackPhase(waterField, p1LifeCount)
                break
            drawCard(waterDeck, waterHand)
            print("")
        manaCount += 1
        turnCount += 1
        print(f"Round ended. New round: {turnCount + 1}, Mana per player: {manaCount}")
        print("")
        if p1LifeCount <= 0:
            gameStart = False
            print("game over p2 wins")
        if p2LifeCount <= 0:
            gameStart = False
            print("game over p1 wins")


def deckSelectionMenu():
    """Display deck selection menu and return 'fire' or 'water'."""
    while True:
        print("\n" + "="*40)
        print("SELECT YOUR DECK")
        print("="*40)
        print("1: Fire Deck")
        print("   Cards: Imp, Drake, Fireball, Flamestrike, Wildfire, Cerberus, Spirit of Fire")
        print("\n2: Water Deck")
        print("   Cards: Water Serpent, Water Spout, Monsoon, Water Sprite, Crash, Mino, Tidal Wave")
        print("="*40 + "\n")
        
        choice = input("Select your deck (1 or 2): ").strip()
        if choice == '1':
            print("\n✓ You selected FIRE Deck!\n")
            return 'fire'
        elif choice == '2':
            print("\n✓ You selected WATER Deck!\n")
            return 'water'
        else:
            print("Invalid selection. Please enter 1 or 2.")


def selectCardMenu(hand, sock, state):
    """Display hand menu and send selected card to server.
    
    Returns True if a card was selected, False if End Turn
    """
    while True:
        print("\n=== Your Hand ===")
        for i, card in enumerate(hand, start=1):
            attack = getattr(card, "attack", "?")
            health = getattr(card, "health", "?")
            cost = getattr(card, "cost", "?")
            card_type = getattr(card, "cardType", "?")
            print(f"{i}: {card.cardName} | Type: {card_type} | Cost: {cost} | ATK: {attack} | HP: {health}")
        print("0: End Turn")
        print("================\n")
        
        choice = input("Select a card (number): ").strip()
        if not choice.isdigit():
            print("Please enter a number.")
            continue
        
        idx = int(choice)
        if idx == 0:
            print("Ending turn...")
            return False
        
        if 1 <= idx <= len(hand):
            selected_card = hand[idx - 1]
            card_info = f"CARD {idx-1} {selected_card.cardName} {selected_card.cardType} {selected_card.attack} {selected_card.health} {selected_card.cost}"
            try:
                sock.sendall((f"PLAY {card_info}\n").encode())
                print(f"[YOU] Played: {selected_card.cardName}")
                if selected_card.cardType == "Creature":
                    print(f"--> {selected_card.cardName} summoned to the field!")
                    field = state.get('field', [])
                    state['field'] = field
                    field.append(selected_card)
            except Exception as e:
                print(f"Error sending card selection: {e}")
                return False
        
        print("Invalid selection.")


def recv_thread(sock, state):
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
                        # Prompt player to select a deck
                        print("\n*** You have joined the room! ***")
                        deck_choice = deckSelectionMenu()
                        state['deck'] = deck_choice
                        print(f"Your deck has been set to: {deck_choice.upper()}")
                        # Send deck choice to server
                        try:
                            sock.sendall((f"DECK {deck_choice}\n").encode())
                        except Exception as e:
                            print(f"Error sending deck choice: {e}")
                elif line.startswith("SERVER:INFO Left room") or line.startswith("SERVER:INFO Opponent left"):
                    state['room'] = None
                    state['deck'] = None
                elif line.startswith("SERVER:READY"):
                    print("\n*** Game started! Opponent is ready. ***\n")
                elif line.startswith("SERVER:ATTACK"):
                    # Handle damage from opponent
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            damage = int(parts[1])
                            state['player_health'] -= damage
                            print(f"\n>>> OPPONENT ATTACKS FOR {damage} DAMAGE! YOUR HEALTH: {state['player_health']} <<<\n")
                        except ValueError:
                            pass
                    try:
                        sock.sendall((f"DECK {state['deck']}\n").encode())
                    except Exception as e:
                        print(f"Error sending deck choice: {e}")
                    # print("opponend has %s deck" %line)
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
    ROOMS = ['room1', 'room2', 'room3']

    host = input("Server host [localhost]: ").strip() or 'localhost'
    port_s = input("Server port [9000]: ").strip() or '9000'
    try:
        port = int(port_s)
    except Exception:
        port = 9000

    state = {'room': None, 'running': True, 'deck': None, 'player_health': 20, 'opponent_health': 20}

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

        while state['running']:
            try:
                cmd = input('> ').strip()
            except EOFError:
                cmd = 'quit'
            if not cmd:
                continue
            parts = cmd.split(' ', 2)
            action = parts[0].lower()
            if action in ('rooms', 'list'):
                print("Available rooms:")
                for r in ROOMS:
                    print(f" - {r}")
            elif action == 'game':
                # Start a local game using turnCounter
                print("Starting a local game...")
                fireDeck = []
                waterDeck = []
                try:
                    turnCounter(fireDeck, waterDeck)
                except KeyboardInterrupt:
                    print("")
                    print("Game interrupted by user.")
                    print("")
            elif action == 'join' and len(parts) >= 3:
                rid = parts[1]
                name = parts[2]
                if rid not in ROOMS:
                    print(f"Room {rid} is not available. Use 'rooms' to list options.")
                    continue
                s.sendall((f"JOIN {rid}|{name}\n").encode())
            elif action == 'selectcard' and state['room'] and state['deck']:
                # Interactive card selection from hand based on selected deck
                deck = []
                if state['deck'] == 'fire':
                    createFireDeck(deck)
                elif state['deck'] == 'water':
                    createWaterDeck(deck)
                shuffleDeck(deck)
                hand = createHand(deck)
                selectCardMenu(hand, s, state)
            elif action == 'attack' and state['room']:
                # Networked attack phase
                deck = []
                if state['deck'] == 'fire':
                    createFireDeck(deck)
                elif state['deck'] == 'water':
                    createWaterDeck(deck)
                shuffleDeck(deck)
                # For demo, use a sample field
                if state['deck'] == 'fire':
                    field = [Drake(), Imp()]
                if state['deck'] == 'water':                    
                    field = [WaterSerpent(), WaterSpout()]
                # This will prompt card selection and return updated health

                print(f"\nYour Health: {state['player_health']} | Opponent Health: {state['opponent_health']}")
                attackPhase(field, state['opponent_health'], s, state)
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


if __name__ == '__main__':
    main()
