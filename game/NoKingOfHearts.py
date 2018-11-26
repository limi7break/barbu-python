from game.Game import Game

class NoKingOfHearts(Game):

    def __init__(self, players, first_player, trump_suit=None):
        super().__init__(players, first_player, trump_suit)

    def get_playable_actions(self, hand, trick_cards):
        if not trick_cards:
            hearts = [card for card in hand if card.suit == '♥']
            if len(hearts) == len(hand):
                return [i for i in range(len(hand))]
            else:
                hearts_idx = [hand.index(card) for card in hearts]
                return [i for i in range(len(hand)) if i not in hearts_idx]

        same_suit = [hand.index(card) for card in hand if card.suit == trick_cards[0].suit]

        if not same_suit:
            return [i for i in range(len(hand))]

        return same_suit

    def update_scores(self, state):
        for card in state.trick_cards:
            if card.suit == '♥' and card.value == 11:
                state.scores[state.current_player] -= 20
                state.terminal = True
        
        return state