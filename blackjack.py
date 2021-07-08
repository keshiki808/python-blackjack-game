import copy
import db
import random

# To do :
# <<<<<<<<<<<<DONE>>>>>>>>-Create a list to store the suit, rank, and point value for each card

# <<<<<<<<<<<<DONE>>>>>>>>-Use a list of lists to store the cards in the deck. You can use two nested loops to create the deck of cards

# <<<<<<<<<<<<DONE>>>>>>>>-Use a list of lists to store the dealer's hand and the player's hand

# <<<<<<<<<<<<DONE>>>>>>>>-When the program starts, it should read the player's money amount from a CSV/txt file named money.txt'

# <<<<<<<<<<<<DONE>>>>>>>>-The program should write the player's money amount to a file any time the data is changed'

# <<<<<<<<<<<<DONE>>>>>>>>-Store the functions for writing and reading the moneu amount in a separate module named db.py

# <<<<<<<<<<<<DONE>>>>>>>>-Handle the exception that occurs if the player can't find the data file

# <<<<<<<<<<<<DONE>>>>>>>>-Handle the exceptions that occur if the user enters a string where an integer or float value is expected

# <<<<<<<<<<<<DONE>>>>>>>>-The program should validate the bet amount.
# <<<<<<<<<<<<DONE>>>>>>>>>>> The minimum bet should be 5
# <<<<<<<<<<<<DONE>>>>>>>>>>> The maximum bet should be 1,000
# <<<<<<<<<<<<DONE>>>>>>>>>>> The bet can't be bigger than the player's current amount of money.

# -If the money amount drops below the minimum bet(5), the program should give the player the option to buy more chips.


def title():
    print("Welcome to blackjack")
    print()


def card_picker(deck, hand):
    random_card = random.choice(deck)
    deck.remove(random_card)
    hand.append(random_card)


def hand_value_tabulator(player_cards):
    value = 0
    for card in player_cards:
        value += card[0]
    return value


def ace_checker(player_cards, value):
    flattened_hand = [item for sublist in player_cards for item in sublist]
    ace_count = flattened_hand.count("Ace")
    for n in range(ace_count):
        while True:
            if value <= 11:
                try:
                    ace_response = int(
                        input("Please enter 1 or 11 to state your ace value: ")
                    )
                    if ace_response == 11:
                        value += 10
                        break
                    elif ace_response == 1:
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Please enter 1 or 11")
            else:
                break
    return value


def dealer_ace_checker(player_cards, value):
    flattened_hand = [item for sublist in player_cards for item in sublist]
    ace_count = flattened_hand.count("Ace")
    for n in range(ace_count):
        while True:
            if value <= 11:
                value += 10
                break
            else:
                break
    return value


def bust_checker(hand_value):
    return True if hand_value > 21 else False


def card_display(hand, hand_owner):
    print(f"{hand_owner} CARDS:")
    for card in hand:
        print(f"{card[1]} of {card[2]}")


def user_bet_input(player_money):
    while True:
        try:
            bet = float(input("Please enter an amount to be between 5 and 1000: "))
            if bet < 5 or bet > 1000:
                raise Exception(
                    "Invalid entry: It must be a numerical value between 5 and 1000"
                )
            elif bet > player_money:
                raise Exception("You can't bet more money than you have")
            else:
                player_money -= bet
                db.money_writer(player_money)
                return bet, player_money
        except ValueError:
            print("The entry must be a valid integer or float between 5 and 1000")
        except Exception as e:
            print(e)


def money_updator(player_money, bet_amount, result):
    if result == "player win":
        player_money += bet_amount * 1.5
        return player_money
    elif result == "player loss":
        return


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


def hit_or_stand_declaration():
    while True:
        try:
            user_response = input("Hit or Stand? (hit/stand): ").lower()
            if user_response == "hit" or user_response == "stand":
                return True if user_response == "hit" else False
            else:
                raise Exception
        except Exception:
            print("You must enter hit or stand")


def player_victory_check(
    player_hand_value, dealer_hand_value, player_bust_status, dealer_bust_status
):
    if (
        player_hand_value > dealer_hand_value
        and player_bust_status != True
        or dealer_bust_status == True
    ):
        return True
    else:
        False


def draw_check(player_hand_value, dealer_hand_value):
    return True if player_hand_value == dealer_hand_value else False


def payout(player_win_status, draw_status, bet, player_money):
    if player_win_status:
        payout = bet * 1.5
    elif draw_status:
        payout = bet
    else:
        payout = 0
    player_money += payout
    db.money_writer(player_money)
    return player_money


def results_display(player_win_status, draw_status):
    if player_win_status:
        print("Player wins")
    elif draw_status:
        print("It was a draw")
    else:
        print("Player loses")

def buy_chips():
    while true:
        try:
            response = input("You have less than 5 chips, Would you like to buy some more? (y/n): ")
            if response == "y":
                money_response = input("You have less than 5 chips, Would you like to buy some more? (y/n): ")


def main():
    deck = deck_creator()
    player_money = db.money_reader()
    player_money = 200
    db.money_writer(player_money)
    bet, player_money = user_bet_input(player_money)
    print("Player money", player_money)
    print(deck)
    player_hand = []
    dealer_hand = []
    card_picker(deck, dealer_hand)
    dealer_hand_value = hand_value_tabulator(dealer_hand)
    print(f"DEALER'S SHOW CARD:\n{dealer_hand[0][1]} of {dealer_hand[0][2]}")
    card_picker(deck, player_hand)
    card_picker(deck, player_hand)
    card_display(player_hand, "YOUR")
    player_hand_value = hand_value_tabulator(player_hand)
    player_hand_value = ace_checker(player_hand, player_hand_value)
    print(player_hand_value)
    hit = hit_or_stand_declaration()
    player_bust = False
    dealer_bust = False
    while hit == True:
        card_picker(deck, player_hand)
        card_display(player_hand, "YOUR")
        player_hand_value = hand_value_tabulator(player_hand)
        player_hand_value = ace_checker(player_hand, player_hand_value)
        player_bust = bust_checker(player_hand_value)
        if player_bust:
            break
        else:
            hit = hit_or_stand_declaration()
    while dealer_hand_value < 17:
        if player_bust:
            break
        card_picker(deck, dealer_hand)
        card_display(dealer_hand, "DEALER'S")
        dealer_hand_value = hand_value_tabulator(dealer_hand)
        dealer_hand_value = dealer_ace_checker(dealer_hand, dealer_hand_value)
        dealer_bust = bust_checker(dealer_hand_value)
        if dealer_bust:
            break
    player_win = False
    draw = draw_check(player_hand_value, dealer_hand_value)
    if not draw:
        player_win = player_victory_check(
            player_hand_value, dealer_hand_value, player_bust, dealer_bust
        )
    payout(player_win, draw, bet, player_money)
    results_display(player_win, draw)


if __name__ == "__main__":
    main()
