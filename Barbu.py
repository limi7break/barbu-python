import random, importlib, consts
from operator import add
from utils import int_input, tell_everyone
from Card import Card, Deck
from player.Player import RandomPlayer
from player.HeuristicPlayer import HeuristicPlayer
from player.MCPlayer import MCPlayer
from player.CLIHumanPlayer import CLIHumanPlayer
from player.GUIHumanPlayer import GUIHumanPlayer

class Barbu():

    def __init__(self, players):
        assert len(players) == consts.NUM_PLAYERS, '[-] Please give a list of exactly {} players!'.format(consts.NUM_PLAYERS)
        self.players = players
        self.total_scores = [0 for _ in range(consts.NUM_PLAYERS)]

    def play(self):
        # Ask who should be the first dealer
        self.dealer_ID = None
        while self.dealer_ID is None or self.dealer_ID < -1 or self.dealer_ID >= consts.NUM_PLAYERS:
            self.dealer_ID = int_input('Please insert ID of first dealer (-1 for random): ')

        # Choose a random dealer
        if self.dealer_ID == -1:
            self.dealer_ID = random.randint(0, 3)
        
        # Tell players who is the first dealer
        tell_everyone(self.players, 'First dealer: {}'.format(self.dealer_ID))

        # Main loop (every game is played for every player)
        for _ in range(len(self.players)):
            for _ in range(consts.NUM_GAMES):
                # Empty players' hands
                for i in range(consts.NUM_PLAYERS):
                    self.players[i].hand = []

                # Create a new deck and distribute cards to players' hands
                self.deck = Deck()
                self.distribute_cards()
                assert self.deck.is_empty(), '[-] Not all cards have been distributed!'
                for player in self.players:
                    assert len(player.hand) == 13, '[-] Player {}\'s hand does not contain 13 cards!'.format(player.ID)

                # Ask dealer what should be the next game
                available_games = [game_num for game_num, played in self.players[self.dealer_ID].played_games.items() if not played]

                game_num = None
                while game_num not in available_games:
                    game_num = self.players[self.dealer_ID].get_next_game()
                
                # Mark the chosen game as played
                self.players[self.dealer_ID].played_games[game_num] = True

                # Tell players the chosen game
                tell_everyone(self.players, 'Player {} called {}!'.format(self.dealer_ID, consts.GAMES[game_num].split('.')[1]))

                # If the dealer chose Atout, ask them for a trump suit
                trump_suit = None
                if consts.GAMES[game_num] == 'game.Atout':
                    while trump_suit not in Card.suits:
                        trump_suit = self.players[self.dealer_ID].get_trump_suit()

                    tell_everyone(self.players, '(trump suit: {})'.format(trump_suit))

                # Initialize and play chosen game
                game = self.get_game(game_num, self.players, self.dealer_ID, trump_suit)
                game_scores = game.play()
                tell_everyone(self.players, 'Game scores: {}'.format(game_scores))

                # Update final scores
                self.total_scores = list(map(add, self.total_scores, game_scores))
                tell_everyone(self.players, 'Total scores: {}'.format(self.total_scores))

            # Check if the total scores sum to zero, pass dealer to next player
            assert sum(self.total_scores) == 0, 'The total scores do not sum to zero after a complete dealer!'
            self.dealer_ID = (self.dealer_ID + 1) % consts.NUM_PLAYERS

        return self.total_scores

    def distribute_cards(self):
        # Distribute cards
        for i in range(consts.DIFFERENT_CARDS):
            self.players[i % len(self.players)].hand += self.deck.draw()

        # Sort cards according to their integer representation (♥ ♦ ♣ ♠ ascending value)
        for i in range(len(self.players)):
            self.players[i].hand = list(map(Card.int_to_card, sorted(map(int, self.players[i].hand))))

    def get_game(self, game_num, players, first_player, trump_suit=None):
        '''
            Imports the module corresponding to the chosen game,
            creates the corresponding Game object, initializes it
            and returns it.
        '''
        module_name = consts.GAMES[game_num]
        class_name = module_name.split('.')[1]

        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)

        return class_(players, first_player, trump_suit)



def create_players():
    players = []

    print('Player types:')
    print('    0: RandomPlayer')
    print('    1: HeuristicPlayer')
    print('    2: MCPlayer')
    print('    3: CLIHumanPlayer')
    print('    4: GUIHumanPlayer')

    while len(players) != consts.NUM_PLAYERS:
        choice = int_input('Please insert the player type for player {}: '.format(len(players)))

        if choice == 0:
            players.append(RandomPlayer(ID=len(players)))
        elif choice == 1:
            print('[-] Not implemented yet!')
        elif choice == 2:
            print('[-] Not implemented yet!')
        elif choice == 3:
            players.append(CLIHumanPlayer(ID=len(players)))
        elif choice == 4:
            players.append(GUIHumanPlayer(ID=len(players)))

    return players

if __name__ == '__main__':
    print('Welcome to barbu-python 1.0!')
    players = create_players()
    barbu = Barbu(players)
    scores = barbu.play()
    tell_everyone(players, 'Game finished! Final scores: {}'.format(scores))
    print('Game finished! Final scores: {}'.format(scores))