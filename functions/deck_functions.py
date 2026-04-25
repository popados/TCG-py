"""
Deck management functions for TCG Game Client

Imports Required:
- random (Python standard library)
- deckFire.fireCards: Flamestrike, Imp, Drake, Wildfire, Fireball, Cerberus, SpiiritOfFire
- deckWater.waterCards: Crash, Monsoon, WaterSpirite, WaterSerpent, WaterSpout, Mino, TidalWave
"""

import random
from deckFire.fireCards import Flamestrike, Imp, Drake, Wildfire, Fireball, Cerberus, SpiiritOfFire
from deckWater.waterCards import Crash, Monsoon, WaterSpirite, WaterSerpent, WaterSpout, Mino, TidalWave


def createFireDeck(fireDeck):
    """Create a fire deck by adding 3 copies of each fire card.
    
    Args:
        fireDeck (list): Empty list to populate with fire cards
        
    Returns:
        list: The populated fire deck
    """
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
    """Create a water deck by adding 3 copies of each water card.
    
    Args:
        waterDeck (list): Empty list to populate with water cards
        
    Returns:
        list: The populated water deck
    """
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
    """Shuffle a deck by randomly rearranging cards.
    
    Args:
        deck (list): The deck to shuffle
        
    Returns:
        list: The shuffled deck
    """
    for i in range(len(deck)):
        count = random.randint(0, len(deck) - 1)
        deck.append(deck.pop(count))
    return deck
