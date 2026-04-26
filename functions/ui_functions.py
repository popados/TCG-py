"""
UI and menu functions for TCG Game Client

Imports Required:
- os (Python standard library)
"""

import os


def clear():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def handMenu(hand, field):
    """Show a numbered menu for the given hand and return the selected card or None for End Turn.
    
    0 -> End Turn
    1..N -> select corresponding card in hand
    
    Args:
        hand (list): The player's hand
        field (list): The field (play area)
        
    Returns:
        Card or None: Selected card, or None to end turn
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


def deckSelectionMenu():
    """Display the deck selection menu prompt.
    
    Does not take input — the main command loop reads the player's choice
    and sends it to the server. Call this to print the menu, then wait
    for the player to type '1' or '2' at the main prompt.
    """
    print("\n" + "="*40)
    print("SELECT YOUR DECK")
    print("="*40)
    print("1: Fire Deck")
    print("   Cards: Imp, Drake, Fireball, Flamestrike, Wildfire, Cerberus, Spirit of Fire")
    print("\n2: Water Deck")
    print("   Cards: Water Serpent, Water Spout, Monsoon, Water Sprite, Crash, Mino, Tidal Wave")
    print("="*40)
    print("Type 1 or 2 to select your deck.\n")


def selectCardMenu(hand, sock, state):
    """Display hand menu and send selected card to server.
    
    Args:
        hand (list): The player's hand
        sock (socket): The server socket connection
        state (dict): Game state dictionary
    
    Returns:
        bool: True if a card was selected, False if End Turn
    """
    while True:
        available_mana = state.get('mana_available', 0)
        print("\n=== Your Hand ===")
        print(f"Available Mana: {available_mana}")
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
            card_cost = getattr(selected_card, "cost", 0)
            if card_cost > available_mana:
                print(f"Not enough mana to play {selected_card.cardName}. Need {card_cost}, have {available_mana}.")
                continue
            card_info = f"CARD {idx-1} {selected_card.cardName} {selected_card.cardType} {selected_card.attack} {selected_card.health} {selected_card.cost}"
            try:
                sock.sendall((f"PLAY {card_info}\n").encode())
                print(f"[YOU] Played: {selected_card.cardName}")
                state['mana_available'] = max(0, available_mana - card_cost)
                if selected_card.cardType == "Creature":
                    print(f"--> {selected_card.cardName} summoned to the field!")
                    field = state.get('field', [])
                    field.append(selected_card)
                hand.pop(idx - 1)
            except Exception as e:
                print(f"Error sending card selection: {e}")
            return True
        
        print("Invalid selection.")
