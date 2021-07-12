import copy
import random

# Converts suit as a string to corresponding unicode image
def card_stylizer(card_suit):
    card_styles = {"Spades": "♠", "Hearts": "♥", "Diamonds": "♦", "Clubs": "♣"}
    return card_styles[card_suit]


# Builds an ascii image of the hand of cards
def card_image_builder(cards):
    card_images = ["", "", "", "", ""]
    for card in cards:
        symbol = card_stylizer(card[2])
        if type(card[1]) is str:
            abbreviation = card[1][0]
        else:
            abbreviation = card[1]
        card_images[0] += "-" * 9 + " "
        card_images[1] += f"|{symbol}      |" + " "
        card_images[2] += "|   {:<2}  |".format(abbreviation) + " "
        card_images[3] += f"|      {symbol}|" + " "
        card_images[4] += f"-" * 9 + " "
    for part in card_images:
        print(part)


# Picks a random card from the deck
def card_picker(deck, hand):
    random_card = random.choice(deck)
    deck.remove(random_card)
    hand.append(random_card)


# Displays the cards in a player's hand
def card_display(hand, hand_owner):
    if len(hand) == 1:
        print(f"{hand_owner} CARD:")
    else:
        print(f"{hand_owner} CARDS:")
    for card in hand:
        print(f"{card[1]} of {card[2]}")


# Function to generate a deck from by combining appending the suit and rank of cards to the point value.
def deck_creator():
    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
    points = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [10], [10], [10]]
    ranks = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
    for count, point in enumerate(points):
        point.append(ranks[count])
    deck = []
    for suit in suits:
        card_container = copy.deepcopy(points)
        for point in card_container:
            point.append(suit)
        deck.append(card_container)
    return [item for sublist in deck for item in sublist]
