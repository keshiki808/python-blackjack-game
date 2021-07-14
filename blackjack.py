import db
import deck


def title():
    print("Welcome to blackjack")
    print()


def hand_value_tabulator(player_cards):
    value = 0
    for card in player_cards:
        value += card[0]
    return value


def blackjack_checker(hand_value):
    if hand_value == 21:
        print("Blackjack!")


# Determines if the player has any aces, allows them to choose 1 or 11 for the value
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
                    print("Error: Please enter 1 or 11")
            else:
                break
    return value


# Determines if the dealer has any aces, and chooses the appropriate value between 1 or 11 automatically
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


# Returns a boolean to determine if the player or dealer have gone over 21 and bust(lose)
def bust_checker(hand_value):
    return hand_value > 21


# Method that facilitates user betting, ensures the betting bounds are between 5 and 1000
def user_bet_input(player_money):
    while True:
        try:
            bet = round(
                float(input("Please enter an amount to bet between 5 and 1000: ")), 2
            )
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


# Returns a boolean to reinitate player turn cycle
def hit_or_stand_declaration():
    while True:
        try:
            user_response = input("Hit or Stand? (hit/stand): ").lower()
            if user_response.lower() == "hit" or user_response.lower() == "stand":
                return True if user_response == "hit" else False
            else:
                raise Exception
        except Exception:
            print("You must enter hit or stand")


def player_victory_check(
    player_hand_value, dealer_hand_value, player_bust, dealer_bust
):
    if player_hand_value > dealer_hand_value and not player_bust or dealer_bust:
        return True
    else:
        return False


def draw_check(player_hand_value, dealer_hand_value):
    return player_hand_value == dealer_hand_value


def payout(player_win_status, draw_status, bet, player_money):
    if player_win_status:
        payout = round(bet * 1.5, 2)
        print(
            f"You win a payout of {payout}, you now have a total of {player_money + payout}"
        )
    elif draw_status:
        payout = bet
        print(f"You get your bet back. You have {player_money + bet}")
    else:
        payout = 0
        print(f"You now have {player_money}.")
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


# Gives the player the option to purchase more chips or refuse (and quit the game)
def buy_chips(player_chips):
    while True:
        response = input(
            "You have less than 5 chips, Would you like to buy some more? (y/n): "
        )
        if response.lower() == "y":
            try:
                money_response = round(
                    float(
                        input(
                            f"How many chips would you like to buy? "
                            f"Enter a value between 5 and 1000 chips: "
                        )
                    ),
                    2,
                )
                print()
                if money_response < 5 or money_response > 1000:
                    print(
                        "Invalid entry, you can only purchase at least 5 chips and no more than 1000\n"
                    )
                else:
                    new_total = player_chips + money_response
                    print(
                        f"Thank you for your purchase. You now have {new_total} chips\n"
                    )
                    db.money_writer(new_total)
                    return new_total
            except ValueError:
                print("You must enter a valid integer or float\n")
        elif response.lower() == "n":
            print(
                """
                You've decided against purchasing anymore chips.
                You walk away from the casino in shame.\n """
            )
            quit()
        else:
            print("You must enter 'y' or 'n' to proceed")


def play_again():
    while True:
        response = input("Play again? (y/n): ")
        if response.lower() == "y":
            break
        elif response.lower() == "n":
            print("See ya")
            quit()
        else:
            print("Please enter 'y' to play again or 'n' to quit")


def main():
    title()
    while True:
        card_deck = deck.deck_creator()
        player_money = db.money_reader()
        print("Current player money: " f"{player_money}")

        # Option given to buy chips if less than 5 then bet
        if player_money < 5:
            player_money = buy_chips(player_money)
        bet, player_money = user_bet_input(player_money)
        print()

        # Initial setup of hands and bust status
        player_hand = []
        dealer_hand = []
        player_bust = False
        dealer_bust = False
        player_win = False

        # Card dealt to player, listed and illustrated
        deck.card_picker(card_deck, player_hand)
        deck.card_display(player_hand, "YOUR")
        deck.card_image_builder(player_hand)

        print("-" * 60)

        # Dealer reveals showcard, listed and illustrated
        deck.card_picker(card_deck, dealer_hand)
        dealer_hand_value = hand_value_tabulator(dealer_hand)
        deck.card_display(dealer_hand, "DEALER'S SHOW")
        deck.card_image_builder(dealer_hand)

        print("-" * 60)

        # Player receives second card, given option to choose ace value and hit or stand
        deck.card_picker(card_deck, player_hand)
        deck.card_display(player_hand, "YOUR")
        deck.card_image_builder(player_hand)
        player_hand_value = hand_value_tabulator(player_hand)
        player_hand_value = ace_checker(player_hand, player_hand_value)
        blackjack_checker(player_hand_value)
        hit = hit_or_stand_declaration()
        print()

        while hit == True:
            # Player receives cards until they stand or bust
            deck.card_picker(card_deck, player_hand)
            deck.card_display(player_hand, "YOUR")
            deck.card_image_builder(player_hand)
            player_hand_value = hand_value_tabulator(player_hand)
            player_hand_value = ace_checker(player_hand, player_hand_value)
            player_bust = bust_checker(player_hand_value)
            blackjack_checker(player_hand_value)
            print()
            if player_bust:
                print("Player busts")
                break
            else:
                hit = hit_or_stand_declaration()
                print()

        while dealer_hand_value < 17:
            if player_bust:
                break

            # Creates a line to distinguish when Dealer begins drawing after player turn loop
            if len(dealer_hand) == 1:
                print("-" * 60)

            # Dealer receives cards until they reach 17 then stop or until they bust.
            deck.card_picker(card_deck, dealer_hand)
            deck.card_display(dealer_hand, "DEALER'S")
            deck.card_image_builder(dealer_hand)
            dealer_hand_value = hand_value_tabulator(dealer_hand)
            dealer_hand_value = dealer_ace_checker(dealer_hand, dealer_hand_value)
            dealer_bust = bust_checker(dealer_hand_value)
            blackjack_checker(dealer_hand_value)
            print()
            if dealer_bust:
                print("Dealer busts")
                break

        # Determines outcome, win, loss or draw for player
        draw = draw_check(player_hand_value, dealer_hand_value)
        if not draw:
            player_win = player_victory_check(
                player_hand_value, dealer_hand_value, player_bust, dealer_bust
            )

        # Cleanup by paying out the player and displaying the results
        results_display(player_win, draw)
        payout(player_win, draw, bet, player_money)

        play_again()
        print()


if __name__ == "__main__":
    main()
