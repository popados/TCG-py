from ast import While
import sys
import time
import random
from unittest import case
from deckFire.fireCards import Flamestrike, Imp
from deckFire.fireCards import Drake, Wildfire
from deckFire.fireCards import Fireball, Cerberus, SpiiritOfFire
from deckWater.waterCards import Crash, Monsoon, WaterSpirite, WaterSerpent
from deckWater.waterCards import WaterSpout, WaterSerpent, Mino

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

add a draw phase and return to the hand and ask for another selection when the does not select a card to play. Allow player to play cards until they select to end their turn.
---
decks
cards
hand
field
"""
lifeCount = 20
fireDeck = []
waterDeck = []
fireHand = []
waterHand = []
field = []
# shuffledDeck = []


def playCardWithMutation(card):
    """Play a card and mutate the global lifeCount variable"""
    global lifeCount
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
        waterDeck.append(Monsoon())
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
                    playCardWithMutation(hand[i])
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

def turnCounter(fireDeck, waterDeck):
    createFireDeck(fireDeck)
    createWaterDeck(waterDeck)
    
    shuffleDeck(fireDeck)
    shuffleDeck(waterDeck)
    global lifeCount
    turnCount = 0
    manaCount = 1
    playerTwoTurn = False
    playerOneTurn = True
    gameStart = True
    fireHand = createHand(fireDeck)
    print("fire hand created")
    print("")
    waterHand = createHand(waterDeck)
    print("water hand created")
    print("")
    # hand = createHand(deck)
    # if lifeCount > 0:
    while gameStart == True:
        if lifeCount >= 0:
            if playerOneTurn == True:
                print("p1 turn: %s" %(turnCount + 1))
                input("1 mana added: %s mana total" %(manaCount))
                print("")
                # card selection function 
                selectCard(fireHand)
                drawCard(fireDeck, fireHand)
                # lifeCount = playCardWithMutation(hand[0])
                print("")
                # print("player one")
                # input("press enter to next player")
                playerOneTurn = False
                playerTwoTurn = True
                # return lifeCount
            if playerTwoTurn == True:
                # p2manaCount = turnCount + 1
                print("p2 turn: %s" %(turnCount + 1))
                input("1 mana added: %s mana total" %(manaCount))
                print("")
                selectCard(waterHand)
                drawCard(waterDeck, waterHand)
                print("")
                # print("player two")
                # input("press enter")
                playerTwoTurn = False
                playerOneTurn = True
            manaCount += 1
            turnCount += 1
        # return lifeCount
        if lifeCount <= 0:
            gameStart = False
            print("game over")
    # return lifeCount
        # lifeCount -= 1

try:
    print("")
    print("******************************")
    print("")
    print("hello")
    input("press enter")
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