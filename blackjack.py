import copy

# To do :
# -Create a list to store the suit, rank, and point value for each card

# <<<<<<<<<<<<DONE>>>>>>>>-Use a list of lists to store the cards in the deck. You can use two nested loops to create the deck of cards

# -Use a list of lists to store the dealer's hand and the player's hand

# -When the program starts, it should read the player's money amount from a CSV/txt file named money.txt'

# -The program should write the player's money amount to a file any time the data is changed'

# -Store the functions for writing and reading the moneu amount in a separate module named db.py

# -Handle the exception that occurs if the player can't find the data file

# -Handle the exceptions that occur if the user enters a string where an integer or float value is expected

# -The program should validate the bet amount.
# >>> The minimum bet should be 5
# >>> The maximum bet should be 1,000
# >>> The bet can't be bigger than the player's current amount of money.

# -If the money amount drops below the minimum bet(5), the program should give the player the option to buy more chips.


def deck_creator():
    # Function to generate a deck from by combining appending the suit and rank of cards to the point value.
    # Uses enumeration to add point values to ranks then uses a nested loop to add each suits to the ranks + points
    # before combining and flattening the deck to be used throughout the program.

    suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
    points = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [10], [10], [10]]
    ranks = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
    for count, point in enumerate(points):
        point.append(ranks[count])
    deck = []
    i = 0
    while i < 4:
        card_container = copy.deepcopy(points)
        for point in card_container:
            point.append(suits[i])
        deck.append(card_container)
        i += 1
    return [item for sublist in deck for item in sublist]


def main():
    deck = deck_creator()
    print(deck)


if __name__ == "__main__":
    main()
