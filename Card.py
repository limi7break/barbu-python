from random import shuffle

class Card():

    DIFFERENT_CARDS = 52
    suits  = ['♥', '♦', '♣', '♠']
    labels = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit, value):
        suit = Card.suit_to_symbol(suit)

        if not isinstance(value, int):
            try:
                value = Card.labels.index(value)
            except ValueError:
                raise ValueError('[-] Invalid Card value! (value: {})'.format(value))

        if value > 12 or value < 0:
            raise ValueError('[-] Invalid Card value! (value: {})'.format(value))
        
        if suit not in Card.suits:
            raise ValueError('[-] Invalid Card suit! (suit: {})'.format(suit))
        
        self.suit  = suit
        self.value = value

    def __str__(self):
        return '[{}{}]'.format(self.suit, Card.labels[self.value])

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.suit == other.suit and self.value == other.value

    def __int__(self):
        return Card.suits.index(self.suit)*13 + self.value

    @staticmethod
    def int_to_card(x):
        suit = Card.suits[x//13]
        value = x % 13
        return Card(suit, value)

    @staticmethod
    def suit_to_symbol(x):
        if x == 'Hearts':
            return '♥'
        if x == 'Diamonds':
            return '♦'
        if x == 'Clubs':
            return '♣'
        if x == 'Spades':
            return '♠'

        return x

class Deck():

    def __init__(self):
        # Add four suits with 1-13 cards.
        self.cards = [Card(suit, value) for suit in Card.suits for value in range(13)]
        shuffle(self.cards)

    def draw(self, num=1):
        '''
        Returns a list of the drawn cards from the deck.
        Removes the card from the deck.
        :param num: int Number of cards to draw.
        :return: list: Cards drawn
        '''
        return [self.cards.pop() for _ in range(num)]

    def is_empty(self):
        return len(self.cards) <= 0


def is_new_winner(new_card, winning_card, trump_suit=None):
    '''
    Returns True if the new_card wins, taking into account
    trump suit if possible.

    :param new_card: The new Card played.
    :param winning_card: Current winning Card.
    :param trump_suit: Trump suit if applicable. Default is None.
    :return: True if new_card wins, False otherwise.
    '''
    trump_suit = Card.suit_to_symbol(trump_suit)

    if new_card.suit == winning_card.suit:
        return new_card.value > winning_card.value
    elif new_card.suit == trump_suit:
        return True

    return False

def get_trick_winner(trick_cards, trump_suit=None):
    '''
        Returns an integer which is the index of the winning
        card in the trick, taking into account trump suit
        if possible.
    '''
    winning_card = trick_cards[0]

    for card in trick_cards[1:]:
        if is_new_winner(card, winning_card, trump_suit):
            winning_card = card

    return trick_cards.index(winning_card)