import random, consts
from utils import int_input
from Card import Card

class Player():

    def __init__(self, name=""):
        self.name  = name
        self.hand  = []
        self.played_games = {game_num: False for game_num in range(consts.NUM_GAMES)}

    def get_next_game(self):
        raise NotImplementedError('[-] This needs to be implemented by your Player class!')

    def get_trump_suit(self):
        raise NotImplementedError('[-] This needs to be implemented by your Player class!')

    def get_starting_value(self):
        raise NotImplementedError('[-] This needs to be implemented by your Player class!')        

    def get_next_action(self, state):
        raise NotImplementedError('[-] This needs to be implemented by your Player class!')

class RandomPlayer(Player):
    '''
        A completely random player: always chooses all
        actions randomly.
    '''
    def get_next_game(self):
        return random.choice([game_num for game_num, played in self.played_games.items() if not played])

    def get_trump_suit(self):
        return random.choice(Card.suits)

    def get_starting_value(self):
        return random.choice(list(range(13)))

    def get_next_action(self, state):
        return random.choice(state.playable_actions)

class HeuristicPlayer(Player):
    '''
        A player that plays according to some expert-made
        heuristics. It implements a different action logic
        for every game.
    '''
    pass

class MCPlayer(Player):
    '''
        A player that makes use of MCTS (Monte Carlo Tree Search)
        and UCT (Upper Confidence Bound applied to Trees) algorithms
        for action selection.

    '''
    pass

class HumanCLIPlayer(Player):
    '''
        A human player that can play interactively
        and select actions via Command Line Interface.
    '''
    def get_next_game(self):
        available_games = [game_num for game_num, played in self.played_games.items() if not played]

        print('Games left:')
        [print('    {}: {}'.format(i, consts.GAMES[i].split('.')[1])) for i in available_games]
        print('Hand: {}'.format(self.hand))

        game = None
        while game is None or game not in available_games:
            game = int_input('Please insert the game number: ')

        return game

    def get_trump_suit(self):
        print('Suits: {}'.format(Card.suits))

        suit = None
        while suit is None or suit not in range(len(Card.suits)):
            suit = int_input('Please insert the trump suit: ')

        return Card.suits[suit]

    def get_starting_value(self):
        starting_value = None
        while starting_value is None or starting_value not in range(13):
            starting_value = int_input('Please insert the starting value (two: 0, ace: 12): ')

        return starting_value

    def get_next_action(self, state):
        hand = state.hands[state.current_player]

        if state.playable_actions != [-1]:
            playable_cards = [hand[i] for i in state.playable_actions]
        else:
            playable_cards = ['[PASS]']
        
        print('Hand: {}'.format(hand))
        
        if state.game == 'Domino':
            print('Played cards:')
            [print('    {}: {}'.format(suit, cards)) for suit, cards, in state.played_cards.items()]
        else:
            print('Cards played in last trick: {}'.format(state.trick_cards))
            print('Trump suit: {}'.format(state.trump_suit))
        
        print('Possible actions: {}'.format(playable_cards))
        s = '                   '
        for i in range(len(state.playable_actions)):
            s += '({})   '.format(i)
        print(s)

        action = None
        while action is None or action not in range(len(state.playable_actions)):
            action = int_input('Please insert the action number: ')

        return state.playable_actions[action]