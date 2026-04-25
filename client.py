"""
Simple command-line client for the TCG room server.
- Run: python client.py

Usage flow:
- Enter server host/port (defaults provided)
- JOIN <room_id>|<player_name>
- When in a room, type `play <payload>` to send a PLAY command (payload can be e.g. PLAY CARD index)
- Type `leave` to leave, `quit` to disconnect

This client prints server messages and forwards simple `play` commands typed by the user.

Functions imported from:
- functions/network_functions.py: main() — Main client orchestration function
- functions/deck_functions.py: createFireDeck(), createWaterDeck(), shuffleDeck()
- functions/hand_functions.py: createHand(), drawCard(), cardToPlay()
- functions/ui_functions.py: clear(), handMenu(), deckSelectionMenu(), selectCardMenu()
- functions/game_functions.py: playCardWithMutation(), attackPhase(), turnCounter()
"""

from functions.network_functions import main

if __name__ == '__main__':
    main()
