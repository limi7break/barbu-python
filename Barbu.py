import os, sys, signal, random, importlib, getopt, datetime, consts
from operator import add
from utils import int_input, tell_everyone, create_plot
from Card import Card, Deck
from player.Player import HumanPlayer, RandomPlayer
from player.HeuristicPlayer import HeuristicPlayer
from player.MCPlayer import MCPlayer
from player.CLIHumanPlayer import CLIHumanPlayer
from player.GUIHumanPlayer import GUIHumanPlayer

class Barbu():

    def __init__(self, players):
        assert len(players) == consts.NUM_PLAYERS, '[-] Please give a list of exactly {} players!'.format(consts.NUM_PLAYERS)
        self.players = players
        self.total_scores = [0 for _ in range(consts.NUM_PLAYERS)]

    def play(self, dealer_ID=-1):
        # Reset players to default (empty hand, no played games)
        for player in self.players:
            player.reset()

        # Choose a random dealer if not previously specified
        if dealer_ID == -1:
            dealer_ID = random.randint(0, 3)
        
        # Tell players who is the first dealer
        tell_everyone(self.players, 'First dealer: {}'.format(dealer_ID))

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
                available_games = [game_num for game_num, played in self.players[dealer_ID].played_games.items() if not played]

                game_num = None
                while game_num not in available_games:
                    game_num = self.players[dealer_ID].get_next_game()
                
                # Mark the chosen game as played
                self.players[dealer_ID].played_games[game_num] = True

                # Tell players the chosen game
                tell_everyone(self.players, 'Player {} called {}!'.format(dealer_ID, consts.GAMES[game_num].split('.')[1]))

                # If the dealer chose Atout, ask them for a trump suit
                trump_suit = None
                if consts.GAMES[game_num] == 'game.Atout':
                    while trump_suit not in Card.suits:
                        trump_suit = self.players[dealer_ID].get_trump_suit()

                    tell_everyone(self.players, '(trump suit: {})'.format(trump_suit))

                # Initialize and play chosen game
                game = self.get_game(game_num, self.players, dealer_ID, trump_suit)
                game_scores = game.play()
                tell_everyone(self.players, 'Game scores: {}'.format(game_scores))

                # Update final scores
                self.total_scores = list(map(add, self.total_scores, game_scores))
                tell_everyone(self.players, 'Total scores: {}'.format(self.total_scores))

            # Check if the total scores sum to zero, pass dealer to next player
            assert sum(self.total_scores) == 0, 'The total scores do not sum to zero after a complete dealer!'
            dealer_ID = (dealer_ID + 1) % consts.NUM_PLAYERS

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



def create_players(simulate=False):
    players = []

    print('Player types:')
    print('    0: RandomPlayer')
    print('    1: HeuristicPlayer')
    print('    2: MCPlayer')
    if not simulate:
        print('    3: CLIHumanPlayer')
        print('    4: GUIHumanPlayer')

    while len(players) != consts.NUM_PLAYERS:
        choice = int_input('Please insert the player type for player {}: '.format(len(players)))

        if choice == 0:
            players.append(RandomPlayer(ID=len(players)))
        elif choice == 1:
            players.append(HeuristicPlayer(ID=len(players)))
        elif choice == 2:
            print('[-] Not implemented yet!')
        elif not simulate and choice == 3:
            if any([isinstance(player, CLIHumanPlayer) for player in players]):
                print('[-] Multiple CLIHumanPlayers are not implemented yet!')
            else:
                players.append(CLIHumanPlayer(ID=len(players)))
        elif not simulate and choice == 4:
            if any([isinstance(player, CLIHumanPlayer) for player in players]):
                print('[-] Multiple GUIHumanPlayers are not implemented yet!')
            else:
                players.append(GUIHumanPlayer(ID=len(players)))

    return players

def usage():
    print('barbu-python')
    print('    by Michele Ferri (@limi7break)')
    print()
    print('Python implementation of Barbu, a 4-player trick-taking card game.')
    print()
    print('The ambition of this project is to create an Artificial Intelligence for')
    print('the game, based on MCTS / UCT in addition to various heuristics.')
    print()
    print('usage:')
    print('    [-s]\tsimulation mode: play simulated games between computer')
    print('        \tplayers until stopped, collecting data about scores.')
    print('     -h\thelp')
    print()

    
    print('Press Ctrl+C')
    signal.pause()

if __name__ == '__main__':
    print('Welcome to barbu-python 1.0!')

    simulate = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],'sh')
    except getopt.GetoptError as e:
        print(colors.fail('Error: {}. Type -h for help'.format(str(e))))
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('-h','--help'):
            usage()
            sys.exit(0)
        elif opt in ('-s'):
            simulate = True
            all_scores = []
            
            # Define a signal handler to create plot before exiting
            def signal_handler(sig, frame):
                if not os.path.exists('plot/'):
                    os.makedirs('plot/')
                
                now = datetime.datetime.now()
                path = 'plot/{}{}{}_{}{}.png'.format(now.year, now.month, now.day, now.hour, now.minute)
                
                create_plot(all_scores, path)
                
                sys.exit(0)
    
            # Bind the handler to SIGINT (Ctrl-C)
            signal.signal(signal.SIGINT, signal_handler)

    players = create_players(simulate=simulate)

    while simulate:
        barbu = Barbu(players)
        all_scores.append(barbu.play())
        print('Simulated game {}.'.format(len(all_scores)))
    else:
        # Ask who should be the first dealer
        dealer_ID = None
        while dealer_ID is None or dealer_ID < -1 or dealer_ID >= consts.NUM_PLAYERS:
            dealer_ID = int_input('Please insert ID of first dealer (-1 for random): ')
        
        barbu = Barbu(players)
        scores = barbu.play(dealer_ID)
        tell_everyone(players, 'Game finished! Final scores: {}'.format(scores))
        if all([not isinstance(player, HumanPlayer) for player in players]):
            print('Game finished! Final scores: {}'.format(scores))