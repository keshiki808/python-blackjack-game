# Reads the money from a text file, creates a file if one doesn't exist. Player's betting money.
def money_reader():
    try:
        with open("money_store.txt") as file:
            for line in file:
                player_money = line
    except FileNotFoundError:
        print(
            "Player money inventory not found,"
            + "creating new inventory file and setting money to 100"
        )
        player_money = 100
        money_writer(player_money)
    return float(player_money)


# Writes/updates player money
def money_writer(player_money):
    with open("money_store.txt", "w") as file:
        file.write(str(player_money))
