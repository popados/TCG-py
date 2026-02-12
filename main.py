from ast import While
import random
from unittest import case
from deckFire.cards.allCards import Flamestrike, Imp
from deckFire.cards.allCards import Drake, Wildfire
from deckFire.cards.allCards import Fireball, Cerberus, SpiiritOfFire

from player.card import Card
print("")
print("******************************")
print("")
print("hello")
input("press enter")

""" 
checklist
---
turns
- Turn Counter Object
    - Player bool
    - switch turns
    - Turn one playerOne == True

- mana system [x]
- draw phase
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
deck = []
# shuffledDeck = []
hand = []


def playCardWithMutation(card):
    """Play a card and mutate the global lifeCount variable"""
    global lifeCount
    lifeCount = card.playCard(lifeCount)
    return lifeCount


def createDeck(deck):
    for i in range(3):
        deck.append(Imp())
        deck.append(Drake())
        deck.append(Fireball())
        deck.append(Flamestrike())
        deck.append(Wildfire())
        deck.append(Cerberus())
        deck.append(SpiiritOfFire())
    return deck

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
    for i in range(3):
        hand.append(deck.pop(i))
        print("drew card: %s" %hand[i].cardName)
        print("card: %s" %hand[i].printCard())

    return hand

def turnCounter(deck):
    createDeck(deck)
    shuffleDeck(deck)
    global lifeCount
    turnCount = 0
    playerTwoTurn = False
    playerOneTurn = True
    gameStart = True
    hand = createHand(deck)
    # hand = createHand(deck)
    # if lifeCount > 0:
    while gameStart == True:
        if lifeCount > 0:
            if playerOneTurn == True:
                print("p1 turn: %s" %(turnCount + 1))
                input("1 mana added, press enter")
                # card selection function 
                for i in range(len(hand)):
                    print("cards in hand: %s %s" %(i + 1, hand[i].cardName))
                    selection = input ("play card %s: %s? (y/n) " %(i + 1, hand[i].cardName))
                    if selection == "y":
                        print("card %s: %s" %(i + 1, hand[i].cardName))
                        lifeCount = playCardWithMutation(hand[i])
                        print("")
                # lifeCount = playCardWithMutation(hand[0])
                print("")
                # print("player one")
                # input("press enter to next player")
                playerOneTurn = False
                playerTwoTurn = True
                # return lifeCount
            if playerTwoTurn == True:
                print("p2 turn: %s" %(turnCount + 1))
                input("1 mana added, press enter")
                print("")
                # print("player two")
                # input("press enter")
                playerTwoTurn = False
                playerOneTurn = True
            turnCount += 1
        # return lifeCount
        if lifeCount <= 0:
            gameStart = False
            print("game over")
    # return lifeCount
        # lifeCount -= 1
turnCounter(deck)
# print("life count: %s" %lifeCount)
print("deck size: %s" %len(deck))
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