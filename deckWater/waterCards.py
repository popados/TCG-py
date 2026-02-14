from player.card import Card


class WaterSerpent(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Water Serpent"
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

    def playCard(self, lifeCount):
        lifeCount -= 5
        input("Water Serpent played!")
        print("Life: %s" %lifeCount)
        print("---")
        return lifeCount

class Mino(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Mino"
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
        input("Mino played!")
        print("Life: %s" %lifeCount)
        print("---")
        return lifeCount

class WaterSpout(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Water Spout"
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
        input("Water Spout played!")
        print("Life: %s" %lifeCount)
        print("---")
        return lifeCount

class Monsoon(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Monsoon"
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
        input("Monsoon played!")
        print("Life: %s" %lifeCount)
        print("---")
        return lifeCount

class WaterSpirite(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Spirit of Water"
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
        input("Water Sprite played!")
        print("Life: %s" %lifeCount)
        print("---")
        return lifeCount

class TidalWave(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Tidal Wave"
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
        input("Tidal Wave played!")
        print("Life: %s" %lifeCount)
        print("---")
        return lifeCount

class Crash(Card):
    def __init__(self):
        super().__init__()
        self.cardName = "Crash"
        self.attack = 8
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
        input("Crash played!")
        print("Life: %s" %lifeCount)
        print("---")
        return lifeCount