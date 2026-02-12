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