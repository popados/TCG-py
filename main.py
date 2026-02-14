from ast import While
import sys
import os
import random
from unittest import case
from deckFire.fireCards import Flamestrike, Imp
from deckFire.fireCards import Drake, Wildfire
from deckFire.fireCards import Fireball, Cerberus, SpiiritOfFire
from deckWater.waterCards import Crash, Monsoon, WaterSpirite, WaterSerpent
from deckWater.waterCards import WaterSpout, Mino, TidalWave

from player.card import Card


""" 
checklist
---
turns
- Turn Counter Object
    - Player bool
    - switch turns
    - Turn one playerOne == True

- mana system [x]
- draw phase [x]
- main phases [x]
- attack phase [x]
- end phase [x]

turn--
commander object
card object
select card
play card
end turn


add a draw phase and return to the hand and ask for another selection when the does not select a card to play. Allow player to play cards until they select to end their turn.
---
decks
cards
hand
field
"""
p1LifeCount = 20
p2LifeCount = 20
fireDeck = []
waterDeck = []
fireHand = []
waterHand = []
fireField = []
waterField = []
field = []
# shuffledDeck = []
def clear():
    os.system("cls" if os.name == "nt" else "clear")



def playCardWithMutation(card, lifeCount):
    """Play a card and mutate the global lifeCount variable"""
    # global p1LifeCount
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
    import random
    for i in range(len(deck)):
        count = random.randint(0, len(deck) - 1)
        deck.append(deck.pop(count))
        # print("card: %s" %(deck[i].cardName))
        # print("swapping %s and %s" %(i, count))
        # print("card: %s" %(deck[count].cardName))
        # print("**")
        # input("")
        # deck.pop(i)
        # deck.append(count)
        # random.shuffle(deck)        # deck.pop(i)
        # # deck.insert(random.randint(0, len(deck)-1), len(deck[i]))
        # deck.append(random.randint(0, len(deck)-1))
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


def selectCard(hand):
    try:
        for i in range(len(hand)):
            print("cards in hand: %s %s" %(i + 1, hand[i].cardName))
            selection = input ("play card %s: %s? (y/n) " %(i + 1, hand[i].cardName))
            if selection == "y":
                # print("card %s: %s" %(i + 1, hand[i].cardName))
                if hand[i].cardType == "Creature":
                    field.append(hand[i])
                elif hand[i].cardType == "Spell":
                    print("")
                    print("spell %s: %s played" %(i + 1, hand[i].cardName))
                    playCardWithMutation(hand[i], p2LifeCount)  # Assuming for fire player
                    hand.pop(i)
                    continue
                hand.pop(i)
                print("")
            if selection == "n":
                print("")
                print("card %s: %s not played" %(i + 1, hand[i].cardName))
                continue
            if selection != "y":
                print("card %s: %s not played" %(i + 1, hand[i].cardName))
                print("")
                continue
    except ValueError:
        print("Invalid input. Please enter 'y' or 'n'.")
    except IndexError:
        selectCard(hand)

def cardToPlay(hand, lifeCount, field):
    while True:
        print("cards in hand: ")
        for i in range(len(hand)):
            print(f"{i + 1}: {hand[i].cardName} (Mana: {hand[i].cost})")
        selection = input("Select a card to play (type the number). 0 = End Turn\n").strip()
        if not selection.isdigit():
            print("Please enter a number.")
            continue
        idx = int(selection)
        if idx == 0:
            print("Ending turn.")
            return lifeCount
        if 1 <= idx <= len(hand):
            card = hand[idx - 1]
            if card.cardType == "Creature":
                field.append(card)
                print(f"Played creature: {card.cardName}")
            elif card.cardType == "Spell":
                print(f"Played spell: {card.cardName}")
                lifeCount = playCardWithMutation(card, lifeCount)
            hand.pop(idx - 1)
            return lifeCount
        print("Invalid selection. Please try again.")

def handMenu(hand):
    """Show a numbered menu for the given hand and return the selected card or None for End Turn.

    0 -> End Turn
    1..N -> select corresponding card in hand
    """
    while True:
        # clear()
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
            print("field: %s" %field)
        if 1 <= idx <= len(hand):
            return hand[idx - 1]
        print("Invalid selection.")
        input("Press Enter to continue...")

def attackPhase(field, opponentLife):
    if not field:
        print("No creatures to attack with.")
        return opponentLife
    print(":::Attack phase displaying field:::")
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
        print(f"{attacker.cardName} attacks for {damage} damage! Opponent life: {opponentLife}")
        return opponentLife
    print("Invalid selection.")
    return opponentLife

def turnCounter(fireDeck, waterDeck):
    createFireDeck(fireDeck)
    createWaterDeck(waterDeck)
    
    shuffleDeck(fireDeck)
    shuffleDeck(waterDeck)
    global p1LifeCount, p2LifeCount
    turnCount = 0
    manaCount = 1
    gameStart = True
    fireHand = createHand(fireDeck)
    print("fire hand created")
    print("")
    waterHand = createHand(waterDeck)
    print("water hand created")
    print("")
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
    # return lifeCount
        # lifeCount -= 1

try:
    print("")
    print("******************************")
    print("")
    print("hello")
    input("press enter")
    # print("")
    # handMenu(fireHand)
    print("")
    turnCounter(fireDeck, waterDeck)
    # print("deck size: %s" %len(deck))
except KeyboardInterrupt:
    print("")
    print("")
    print("Game interrupted by user.")
    sys.exit(0)
# print("life count: %s" %lifeCount)
# print("deck card 1: %s" %deck[0].cardName)


# deck[0].printCard()
# deck[1].printCard()
# deck[2].printCard()

# obj = Card()
# ourImp = Imp()
# ourImp.printCard()
# ourDrake = Drake()
# ourDrake.printCard()
# ourFireball = Fireball()
# ourFireball.printCard()
# obj.printCard()