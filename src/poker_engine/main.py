from Cards import Card

if __name__ == "__main__":
    card = Card("H", "3")
    card_str = card.__str__()
    print(card_str)
    suit = card.__getattribute__("suit")
    print(suit)
    number = card.hierarchy()
    print(number)


