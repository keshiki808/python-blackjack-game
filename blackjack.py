import copy
import db
import random

# To do :
# <<<<<<<<<<<<DONE>>>>>>>>-Create a list to store the suit, rank, and point value for each card

# <<<<<<<<<<<<DONE>>>>>>>>-Use a list of lists to store the cards in the deck. You can use two nested loops to create the deck of cards

# -Use a list of lists to store the dealer's hand and the player's hand

# <<<<<<<<<<<<DONE>>>>>>>>-When the program starts, it should read the player's money amount from a CSV/txt file named money.txt'

# <<<<<<<<<<<<DONE>>>>>>>>-The program should write the player's money amount to a file any time the data is changed'

# <<<<<<<<<<<<DONE>>>>>>>>-Store the functions for writing and reading the moneu amount in a separate module named db.py

# <<<<<<<<<<<<DONE>>>>>>>>-Handle the exception that occurs if the player can't find the data file

# -Handle the exceptions that occur if the user enters a string where an integer or float value is expected

# -The program should validate the bet amount.
# >>> The minimum bet should be 5
# >>> The maximum bet should be 1,000
# >>> The bet can't be bigger than the player's current amount of money.

# -If the money amount drops below the minimum bet(5), the program should give the player the option to buy more chips.


def title():
    print("Welcome to blackjack")
    print()


def card_picker(deck):
    random_card = random.choice(deck)
    deck.remove(random_card)
    return random_card


def card_value_tabulator(player_cards):
    value = 0
    for card in player_cards:
        value += card[0]
    return value


def user_bet_input(player_money):
    while True:
        try:
            bet = float(input("Please enter an amount to be between 5 and 1000: "))
            if bet < 5 or bet > 1000:
                raise ValueError(
                    "Invalid entry, you must enter a value between 5 and 1000"
                )
            elif bet > player_money:
                raise ValueError("You can't bet more money than you have")
            else:
                player_money -= bet
                db.money_writer(player_money)
                return bet, player_money
        except ValueError as e:
            print(e)


def money_updator(player_money, bet_amount, result):
    if result == "player win":
        player_money += bet_amount * 1.5
        return player_money
    elif result == "player loss":



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
    for suit in suits:
        card_container = copy.deepcopy(points)
        for point in card_container:
            point.append(suit)
        deck.append(card_container)
    return [item for sublist in deck for item in sublist]


def main():
    deck = deck_creator()
    player_money = db.money_reader()
    player_money = 200
    db.money_writer(player_money)
    bet, player_money = user_bet_input(player_money)
    print("Player money", player_money)
    print(deck)


if __name__ == "__main__":
    main()
