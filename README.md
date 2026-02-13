
<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD036 -->
<!-- markdownlint-disable MD041 -->
<div id="top-of-doc"></div>

# Readme File |  | January-15-2026 |

[Github](https://github.com/popados) | [Jump to End](#end-of-doc)

***

## Specifications 

***

### DayNum | x/x/20xx - Today

***

### Day 001 | 01/16/2026 - Thursday

Starting my trading card game. This is a game that is based off Magic: The Gathering and includes Hearthstone elements.

Such elements are:

- Mana
- Turns gain mana
- 7 cards each 3 times in a deck
- commander card
- abilities with the commander a -2/0 mana cost

TODO:

- Mana
- Player hand
- Graveyard
- Field
- Abilities
- Cards
- Deck

![Card Game Flow Chart](../tcg_game/_img/card-flowchart.png)

This flowchart shows the attributes and where they are placed within objects. I need to find the design pattern for creating a bucket. I have singleton objects for each card(which could possibily turned into a factory pattern). This allows each card to have an ability such as a shield or extra damage.

![Card Field](../tcg_game/_img/field-markup.png)


***

### Day 002 | 01/26/2026 - Monday

Got some new cards coded in. Added the deck.

Need random number for a shuffle or hand function.

Shuffle function important
draw hand
play card
field

***

### Day 003 | 02/12/2026 - Thursday

In order the steps

- Shuffle
- First Hand
- Draw
- Main Phase(play spell or creature cards)
- Attack Phase(attack with cards on field)
- End Phase

maybe set up client-server interactions

clean up the selection process for cards

remove/add mana

card abilities

***

## End of Document

***

[Jump to Top](#top-of-doc)

<div id="end-of-doc"></div>

<details>
<summary>
Notes :
</summary>
</details>

