"""
Game logic functions for TCG Game Client

Imports Required:
- deckFire.fireCards: Drake, Imp
- deckWater.waterCards: WaterSerpent, WaterSpout
- deck_functions: createFireDeck, createWaterDeck, shuffleDeck
- hand_functions: createHand, drawCard, cardToPlay
"""

from deckFire.fireCards import Drake, Imp
from deckWater.waterCards import WaterSerpent, WaterSpout
from .deck_functions import createFireDeck, createWaterDeck, shuffleDeck
from .hand_functions import createHand, drawCard, cardToPlay


def playCardWithMutation(card, lifeCount):
    """Play a card and mutate the lifeCount variable.
    
    Args:
        card: The card to play
        lifeCount (int): Current life count
        
    Returns:
        int: Updated life count after card effect
    """
    lifeCount = card.playCard(lifeCount)
    return lifeCount


def attackPhase(field, opponentLife, sock=None, state=None):
    """Handle the attack phase where player selects a creature to attack with.
    
    Args:
        field (list): List of creatures on the field
        opponentLife (int): Current opponent life
        sock (socket, optional): Server socket for sending attacks
        state (dict, optional): Game state dictionary
        
    Returns:
        int: Updated opponent life count after attack
    """
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


def turnCounter(fireDeck, waterDeck):
    """Run a complete local game turn counter loop.
    
    Args:
        fireDeck (list): The fire deck
        waterDeck (list): The water deck
    """
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
