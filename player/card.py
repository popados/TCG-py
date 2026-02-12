"""

    //variables for cards
    public string CardName { get; set; }
    public string CardDescription { get; set; }
    public string AbilityDescription { get; set; }
    public string CardType { get; set; }
    public int Attack { get; set; }
    public int Health { get; set; }
    public int Cost { get; set; }
    public int maxMana { get; set; }
    public int currentMana { get; set; }
    public int playerTurnCount { get; set; }
    public bool playerTurn { get; set; }
    public bool isDead { get; set; }
    public bool summonSickness { get; set; }
    public bool isCreature { get; set; }

    
    create a file for each card using the card class as an a parent
    - have the names and costs
    - create a deck with 3 copies of each card in it
    - play hand logic

"""

class Card:
    # def __init__(self, cardName, attack, health, cost, cardType):
    #     self._cardName = cardName
    #     self._attack = attack
    #     self._health = health
    #     self._cost = cost
    #     self._cardType = cardType
    def __init__(self):
        self.cardName = "Placeholder Card"
        self.attack = 99
        self.health = 99
        self.cost = 99
        self.cardType = "Creature/Magic"

    def printCard(self):               
        print("---")
        print(self.cardName)
        print("card type: %s" % self.cardType)
        print("attack: %s" % self.attack)
        print("health: %s" % self.health)
        print("cost: %s" % self.cost)


# card = Card()
# card.printCard()