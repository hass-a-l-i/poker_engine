from Cards import Card
from Hands import Hand

if __name__ == "__main__":
    card = Card("H3")
    card.show_card()
    suit = card.__getattribute__("suit")
    print(suit)
    number = card.hierarchy()
    print(number)
    card2 = Card("HJ")
    hand = Hand()
    hand.add_card(card2)
    hand.add_card(card)
    hand.show_hand()






