def card_stylizer(card_suit):
    card_styles = {"Spades": "♠", "Hearts": "♥", "Diamonds": "♦", "Clubs": "♣"}
    return card_styles[card_suit]


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
