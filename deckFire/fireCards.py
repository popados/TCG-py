from player.card import Card


class Imp(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Imp"
        self.attack = 1
        self.health = 2
        self.cost = 1
        self.cardType = "Creature"

    def printCard(self):
        print("---")
        print (self.cardName)
        print ("card type: %s" %self.cardType)
        print ("attack: %s" %self.attack)
        print ("health: %s" %self.health)
        print ("cost: %s" %self.cost)
        print("---")

    def playCard(self, lifeCount):
        lifeCount -= 5
        input("Imp played!")
        print("Life: %s" %lifeCount)
        return lifeCount

class Drake(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Drake"
        self.attack = 2
        self.health = 3
        self.cost = 3
        self.cardType = "Creature"

    def printCard(self):
        print("---")
        print (self.cardName)
        print ("card type: %s" %self.cardType)
        print ("attack: %s" %self.attack)
        print ("health: %s" %self.health)
        print ("cost: %s" %self.cost)

    def playCard(self, lifeCount):
        lifeCount -= 3
        input("Drake played!")
        print("Life: %s" %lifeCount)
        return lifeCount

class Fireball(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Fireball"
        self.attack = 2
        self.health = 0
        self.cost = 1
        self.cardType = "Spell"

    def printCard(self):
        print("---")
        print (self.cardName)
        print ("card type: %s" %self.cardType)
        print ("attack: %s" %self.attack)
        print ("health: %s" %self.health)
        print ("cost: %s" %self.cost)

    def playCard(self, lifeCount):
        lifeCount -= 3
        input("Fireball played!")
        print("Life: %s" %lifeCount)
        return lifeCount

class Flamestrike(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Flamestrike"
        self.attack = 2
        self.health = 0
        self.cost = 5
        self.cardType = "Spell"

    def printCard(self):
        print("---")
        print (self.cardName)
        print ("card type: %s" %self.cardType)
        print ("attack: %s" %self.attack)
        print ("health: %s" %self.health)
        print ("cost: %s" %self.cost)

    def playCard(self, lifeCount):
        lifeCount -= 3
        input("Flamestrike played!")
        print("Life: %s" %lifeCount)
        return lifeCount

class SpiiritOfFire(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Spirit of Fire"
        self.attack = 4
        self.health = 3
        self.cost = 3
        self.cardType = "Creature"

    def printCard(self):
        print("---")
        print (self.cardName)
        print ("card type: %s" %self.cardType)
        print ("attack: %s" %self.attack)
        print ("health: %s" %self.health)
        print ("cost: %s" %self.cost)

    def playCard(self, lifeCount):
        lifeCount -= 3
        input("Spirit of Fire played!")
        print("Life: %s" %lifeCount)
        return lifeCount

class Wildfire(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Wildfire"
        self.attack = 4
        self.health = 0
        self.cost = 3
        self.cardType = "Spell"

    def printCard(self):
        print("---")
        print (self.cardName)
        print ("card type: %s" %self.cardType)
        print ("attack: %s" %self.attack)
        print ("health: %s" %self.health)
        print ("cost: %s" %self.cost)

    def playCard(self, lifeCount):
        lifeCount -= 3
        input("Wildfire played!")
        print("Life: %s" %lifeCount)
        return lifeCount

class Cerberus(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Cerberus"
        self.attack = 8
        self.health = 6
        self.cost = 5
        self.cardType = "Creature"

    def printCard(self):
        print("---")
        print (self.cardName)
        print ("card type: %s" %self.cardType)
        print ("attack: %s" %self.attack)
        print ("health: %s" %self.health)
        print ("cost: %s" %self.cost)

    def playCard(self, lifeCount):
        lifeCount -= 3
        input("Cerberus played!")
        print("Life: %s" %lifeCount)
        return lifeCount