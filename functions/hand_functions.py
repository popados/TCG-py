"""
Hand management functions for TCG Game Client

Imports Required:
- None (uses basic Python)
"""


def createHand(deck):
    """Create a starting hand of 3 cards from the deck.
    
    Args:
        deck (list): The deck to draw from
        
    Returns:
        list: A hand with 3 cards drawn from the deck
    """
    hand = []
    for i in range(3):
        hand.append(deck.pop(i))
        print(f"drew card: {hand[i].cardName}")
    return hand


def drawCard(deck, hand):
    """Draw a single card from the deck and add it to the hand.
    
    Args:
        deck (list): The deck to draw from
        hand (list): The hand to add the card to
        
    Returns:
        list: The updated hand with the new card
    """
    hand.append(deck.pop(0))
    print(f"drew card: {hand[-1].cardName}")
    return hand


def cardToPlay(hand, lifeCount, field):
    """Player selects a card to play from their hand.
    
    Args:
        hand (list): The player's hand
        lifeCount (int): Current life count
        field (list): The field (play area)
        
    Returns:
        int: Updated life count after playing card
    """
    from .ui_functions import handMenu
    from .game_functions import playCardWithMutation
    
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
