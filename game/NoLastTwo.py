from game.Game import Game

class NoLastTwo(Game):

    def __init__(self, players, first_player, trump_suit=None):
        super().__init__(players, first_player, trump_suit)

    def get_playable_actions(self, hand, trick_cards):
        if not trick_cards:
            return [i for i in range(len(hand))]

        same_suit = [hand.index(card) for card in hand if card.suit == trick_cards[0].suit]

        if not same_suit:
            return [i for i in range(len(hand))]

        return same_suit

    def update_scores(self, state):
        if len(state.played_cards) > 44:
            state.scores[state.current_player] -= 12
        
        return state