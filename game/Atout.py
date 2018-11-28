from game.Game import Game

class Atout(Game):

    def __init__(self, players, first_player, trump_suit=None):
        super().__init__(players, first_player, trump_suit)

    def update_scores(self):
        self.state.scores[self.state.current_player] += 5