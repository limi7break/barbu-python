from game.Game import Game

class NoQueens(Game):

    def __init__(self, players, first_player, trump_suit=None):
        super().__init__(players, first_player, trump_suit)

    def update_scores(self):
        for card in self.state.trick_cards:
            if card.value == 10:
                self.state.scores[self.state.current_player] -= 6

        if len([card for card in self.state.played_cards if card.value == 10]) == 4:
            self.state.terminal = True