import random
import time
import menu

# Major Arcana Card Titles
majorArcana = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant",
               "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man",
               "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement",
               "The World"]
drawnCards = []


class Card:  # Card class, assigns it Suit and Rank
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, other):  # Redefines 'equals' to mean having the same suit and rank.
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        else:
            return NotImplemented

    def __ne__(self, other):  # Redefines 'not equals' to match 'equals'
        return not self.__eq__(other)

    def __hash__(self):  # Redefining hash to be assigned by suit and rank, to make up for modifying the equality
        return hash((self.suit, self.rank))

    def show(self):  # Show method, prints Card Suit and Rank
        print("{} of {}".format(self.rank, self.suit))


class Deck:  # Creates Deck class and a cards[] array to act as the deck
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):  # Build method builds deck one card at a time
        for x in range(len(majorArcana)):
            self.cards.append(Card("The Major Arcana", majorArcana[x]))
        for s in ["Swords", "Wands", "Coins", "Cups"]:
            for r in range(1, 14):
                if r == 1:
                    self.cards.append(Card(s, "Ace"))
                elif 14 >= r >= 11:
                    for r2 in ["Page", "Knight", "Queen", "King"]:
                        self.cards.append(Card(s, r2))
                else:
                    self.cards.append(Card(s, r))

    def show(self):  # Method to show entire deck, not just one card
        for c in self.cards:
            c.show()

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def drawCard(self):
        return self.cards.pop()

    def removeCard(self, drawnCard):
        self.cards.remove(drawnCard)


class Reader:
    def __init__(self):
        self.hand = set()

    def dailyDraw(self, deck):
        drawnCard = deck.drawCard()
        if drawnCard in drawnCards:  # Checks if card is already in hand, if so draws another card
            newCard = deck.drawCard()
            self.hand.add(newCard)

            drawnCards.append(drawnCard)
            drawnCards.append(newCard)
        else:
            self.hand.add(drawnCard)

            drawnCards.append(drawnCard)

    def draw(self, deck):
        drawnCard = deck.drawCard()
        if drawnCard in self.hand:  # Checks if card is already in hand, if so draws another card
            deck.remove(drawnCard)
            newCard = deck.drawCard()
            self.hand.add(newCard)
        else:
            self.hand.add(drawnCard)

    def deal(self):
        print("Dealing...")
        time.sleep(.5)
        for card in self.hand:
            card.show()
            print()

    def threeCardDeal(self):
        print("Shuffling... \n")
        time.sleep(.5)
        print("Dealing... \n")
        time.sleep(.5)

        cardNum = 0
        for card in self.hand:
            print(menu.threeCard[cardNum])
            time.sleep(.5)
            cardNum += 1
            card.show()
            print('\n')
            time.sleep(.5)

    def horseShoeDeal(self):
        print("Shuffling... \n")
        time.sleep(.5)
        print("Dealing... \n")
        time.sleep(.5)

        cardNum = 0
        for card in self.hand:
            print(menu.horseShoe[cardNum])
            time.sleep(.5)
            cardNum += 1
            card.show()
            print('\n')
            time.sleep(.5)

    def celticCrossDeal(self):
        print("Shuffling... \n")
        time.sleep(.5)
        print("Dealing... \n")
        time.sleep(.5)

        cardNum = 0
        for card in self.hand:
            print(menu.celticCross[cardNum])
            time.sleep(.5)
            cardNum += 1
            card.show()
            print('\n')
            time.sleep(.5)

    def read(self):
        for card in self.hand:
            cardRank = getattr(card, "rank")
            cardSuit = getattr(card, "suit")
            return cardRank, cardSuit

    def clear(self):
        self.hand.clear()

    def clearHistory(self):
        drawnCards.clear()
        print("History Cleared")

    def checkHistory(self):
        print("Drawn Cards: ", drawnCards)