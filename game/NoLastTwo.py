from game.Game import Game

class NoLastTwo(Game):

    def __init__(self, players, first_player, trump_suit=None):
        super().__init__(players, first_player, trump_suit)

    def update_scores(self):
        if len(self.state.played_cards) > 44:
            self.state.scores[self.state.current_player] -= 12