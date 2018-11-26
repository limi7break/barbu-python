import random, importlib, consts
from operator import add
from utils import int_input
from Card import Card, Deck
from Player import RandomPlayer, HumanCLIPlayer

class Barbu():

    def __init__(self):
        # For debugging. Only one Human CLI player vs. 3 random players.
        self.players = [RandomPlayer() for _ in range(consts.NUM_PLAYERS - 1)]
        self.players.append(HumanCLIPlayer())
        self.final_scores = [0 for _ in range(consts.NUM_PLAYERS)]

    def play(self):
        # Ask who should be the first dealer
        self.dealer = None
        while self.dealer is None or self.dealer < -1 or self.dealer >= consts.NUM_PLAYERS:
            self.dealer = int_input('Insert first dealer number (-1 for random): ')

        if self.dealer == -1:
            self.dealer = random.randint(0, 3)
            print('First dealer: {}'.format(self.dealer))

        for _ in range(len(self.players)):
            for _ in range(consts.NUM_GAMES):
                # Empty players' hands
                for i in range(consts.NUM_PLAYERS):
                    self.players[i].hand = []

                # Create a new deck and distribute cards to players
                self.deck = Deck()
                self.distribute_cards()
                assert self.deck.is_empty(), '[-] Not all cards have been distributed!'

                available_games = [game_num for game_num, played in self.players[self.dealer].played_games.items() if not played]

                game_num = None
                while game_num not in available_games:
                    # Ask what should be the next game
                    game_num = self.players[self.dealer].get_next_game()
                
                self.players[self.dealer].played_games[game_num] = True

                print('Player {} called {}!'.format(self.dealer, consts.GAMES[game_num].split('.')[1]))

                trump_suit = None
                if consts.GAMES[game_num] == 'game.Atout':
                    while trump_suit not in Card.suits:
                        trump_suit = self.players[self.dealer].get_trump_suit()

                    print('(trump suit: {})'.format(trump_suit))

                # Initialize and play game
                game = self.get_game(game_num, self.players, self.dealer, trump_suit)
                game_scores = game.play()
                print('Game scores: {}'.format(game_scores))

                # Update final scores
                self.final_scores = list(map(add, self.final_scores, game_scores))
                print('Total scores: {}'.format(self.final_scores))

            assert sum(self.final_scores) == 0, 'The final scores do not sum to zero after a complete dealer!'
            self.dealer = (self.dealer + 1) % consts.NUM_PLAYERS

        return self.final_scores

    def distribute_cards(self):
        for i in range(consts.DIFFERENT_CARDS):
            self.players[i % len(self.players)].hand += self.deck.draw()

        for i in range(len(self.players)):
            self.players[i].hand = list(map(Card.int_to_card, sorted(map(int, self.players[i].hand))))

    def get_game(self, game_num, players, first_player, trump_suit=None):
        module_name = consts.GAMES[game_num]
        class_name = module_name.split('.')[1]

        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)

        return class_(players, first_player, trump_suit)



if __name__ == '__main__':
    print('Welcome to barbu-python 1.0!')
    barbu = Barbu()
    scores = barbu.play()

    print('Game finished! Final scores: {}'.format(scores))