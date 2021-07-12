import db
import deck

# Displays the title
def title():
    print("Welcome to blackjack")
    print()


# Accepts a hand and tabulates the value of it
def hand_value_tabulator(player_cards):
    value = 0
    for card in player_cards:
        value += card[0]
    return value


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
                    print("Please enter 1 or 11")
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
    return True if hand_value > 21 else False


# Accepts the user wager
def user_bet_input(player_money):
    while True:
        try:
            bet = float(input("Please enter an amount to bet between 5 and 1000: "))
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


# Initiates player turn cycle
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


# Accepts player and dealer states as arguments and returns a boolean indicating if the player won
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


# Returns a boolean to determine if the dealer and player draw
def draw_check(player_hand_value, dealer_hand_value):
    return True if player_hand_value == dealer_hand_value else False


# Calculates the payout for the
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


# Displays the results of the round
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
        if response == "y":
            try:
                money_response = int(
                    input(
                        f"How many chips would you like to buy? Enter a value between 5 and 1000 chips: "
                    )
                )
                print()
                if money_response < 5 or money_response > 1000:
                    print(
                        "Invalid entry, you need to purchase at least 5 chips and no more than 1000\n"
                    )
                else:
                    print(
                        f"Thank you for your purchase. You now have {player_chips + money_response} chips\n"
                    )
                    db.money_writer(player_chips + money_response)
                    return player_chips + money_response
            except ValueError:
                print("You must enter a valid integer\n")
        elif response == "n":
            print(
                """
                You've decided against purchasing anymore chips.
                You walk away from the casino in shame.\n """
            )
            quit()
        else:
            print("You must enter 'y' or 'n' to proceed")
            continue


def play_again():
    response = input("Play again? (y/n): ")
    return "y" if response == "y" else quit()


def main():
    title()
    while True:
        card_deck = deck.deck_creator()
        player_money = db.money_reader()

        # Option given to buy chips then bet
        if player_money < 5:
            player_money = buy_chips(player_money)
        bet, player_money = user_bet_input(player_money)
        print("Player chips:", player_money)
        print()

        # Initial setup of hands and bust status
        player_hand = []
        dealer_hand = []
        player_bust = False
        dealer_bust = False
        player_win = False

        # Card dealt to player
        deck.card_picker(card_deck, player_hand)
        deck.card_display(player_hand, "YOUR")
        deck.card_image_builder(player_hand)

        # Dealer reveals showcard
        deck.card_picker(card_deck, dealer_hand)
        dealer_hand_value = hand_value_tabulator(dealer_hand)
        deck.card_display(dealer_hand, "DEALER'S SHOW")
        deck.card_image_builder(dealer_hand)  # -----------------------------
        print("-" * 60)

        # Player receives second card, given option to choose ace value and hit or stand
        deck.card_picker(card_deck, player_hand)
        deck.card_display(player_hand, "YOUR")
        deck.card_image_builder(player_hand)  # -----------------------------
        player_hand_value = hand_value_tabulator(player_hand)
        player_hand_value = ace_checker(player_hand, player_hand_value)
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
            print()
            if player_bust:
                break
            else:
                hit = hit_or_stand_declaration()
                print()

        while dealer_hand_value < 17:
            if player_bust:
                break
            # Dealer receives cards until they reach 17 then stop or until they bust.
            deck.card_picker(card_deck, dealer_hand)
            deck.card_display(dealer_hand, "DEALER'S")
            deck.card_image_builder(dealer_hand)
            dealer_hand_value = hand_value_tabulator(dealer_hand)
            dealer_hand_value = dealer_ace_checker(dealer_hand, dealer_hand_value)
            dealer_bust = bust_checker(dealer_hand_value)
            print()
            if dealer_bust:
                break

        # Determines outcome, win, loss or draw for player
        draw = draw_check(player_hand_value, dealer_hand_value)
        if not draw:
            player_win = player_victory_check(
                player_hand_value, dealer_hand_value, player_bust, dealer_bust
            )

        # Cleanup by paying out the player and displaying the results
        payout(player_win, draw, bet, player_money)
        results_display(player_win, draw)

        play_again()


if __name__ == "__main__":
    main()
